#!/usr/bin/env python
#
# xmlLog's command-line interface
#

# Stuff to add:
# 0. help
# 1. tab completion skeleton
# 2. correct entry function with appropriate hooks for tab completion and option printing

import sys
import os
import string
import xmlLog

class xmlCli:
	def __init__(self):
		self.userDefinitions()

		# Open the log file
		self.xmlLog = self.openLogFile()

	def userDefinitions(self):
		self.commands = { 
				 "help": self.dummy,
				    "h": self.dummy,  
				  "def": self.printXmlDef,
				    "d": self.printXmlDef,
				"print": self.printXmlLog,
				    "p": self.printXmlLog,
				    "c": self.dummy,
				  "add": self.addData,
				    "a": self.addData,
				 "quit": self.quit,
				 "save": self.save,
				    "s": self.save
			   }

		self.xmlFilename = "generic_log.xml"
		self.xmlRoot = "log"
		self.xmlEntry = "entry"

		self.xmlEntryDef = [
				"date",
				"author",
				{"remark":
				[
					"title",
					"subject",
					{"subremark":
					[
						"subtitle",
						"subsubject"
					]},
					"index",
					"effort"
				]},
				"note"
			]

	### Functions to customize (and maybe move to a different file)
	def prePromptHook(self, arg):
		return

	# Begin dummy functions
	def dummy(self, *args):
		#!print "dummy(", args, ")"
		return True

	def showHelp(self, *args):
		print "showHelp(", args, ")"
		return True

	def correct(self, *args):
		print "correct(", args, ")"
		return True
	# End dummy functions

	def printXmlDef(self, *args):
		#!print "printStuff(", args, ")"
		#!print self.xmlEntryDef
		self.recursivePrintList(self.xmlEntryDef)
	
		return True

	def recursivePrintList(self, arg, level=0):
		indentStr = "    "
		for i in arg:
			if type(i) is str:
				#!print i, "is a string"
				print indentStr * level + i
			elif type(i) is dict:
				# by design dictionary will only have one key
				key = i.keys()[0]
				#!print i, "is a dictionary"
				print indentStr * level + key
				self.recursivePrintList(i[key], level+1)
			else:
				print "Error: ", type(i)

	def printXmlLog(self, *args):
		contentArray = self.xmlLog.getPrintLogArray()
		print contentArray

		return True

	def quit(self, *args):
		if self.xmlLog.dirty == False:
			print "Exiting..."
			return False
		else:
			raw_ack = raw_input("You have unsaved changes, are you sure you want to quit without saving? ")
			ack = string.strip(raw_ack)
			if ack in ("Yes", "yes", 'Y', 'y'):
				print "Discarding changes and exiting..."
				return False
			else:
				print "Excellent choice!"
				return True

	def save(self, *args):
		self.xmlLog.saveXML()
		return True

	# Diagnostic function which at the moment isn't particularly useful. May help for correct functionality.
	def recursivePrintEntries(self, labels, entries, level=0):
		for i in range(len(labels)):
			if type(labels[i]) is str:
				print labels[i], "->",entries[i]
			if type(labels[i]) is dict:
				# by design dictionary will only have one key
				key = labels[i].keys()[0]
				print "*%s" % key
				self.recursivePrintEntries(labels[i][key], entries[i], level+1)
		if level == 0:
			pass

	def recursivePromptEntry(self, labels, array, level=0):
		for i in range(len(labels)):
			if type(labels[i]) is str:
				# Allow for printing auto-complete suggestions or customizing prompt
				self.prePromptHook(labels[i])
				# Generic promptStr
				promptStr = "  " * level + "%s: " % labels[i]
				# Will it be possible to validate response?
				response = raw_input(promptStr)
				array.append(response)
			elif type(labels[i]) is dict:
				array.append([])
				# by design dictionary will only have one key
				key = labels[i].keys()[0]
				print "  " * level + "[%s]" % key
				self.recursivePromptEntry(labels[i][key], array[i], level+1)
			else:
				print "--> Unhandled prompt entry type: ", type(labels[i])
	
		if level == 0:
			#!print array
			#!self.recursivePrintEntries(self.xmlEntryDef, array)
			pass

	def getUserInput(self):
		# At this point in time there is no helpful printing of existing entries or autocomplete
		userInput = []
		self.recursivePromptEntry(self.xmlEntryDef, userInput)
		return userInput[:]

	def addData(self, *args):
		print "addData(", args, ")"
	
		print
		userEntries = self.getUserInput()
		print

		self.xmlLog.addEntry(userEntries)
	
		return True

	def openLogFile(self):
		# Allow the user to specify an xml file when running the script
		if len(sys.argv) > 1:
			filename = sys.argv[1]
		else:
			filename = "%s/%s" % (os.getcwd(), self.xmlFilename)
			# Alternately could use the script location (sys.argv[0]), but that seems like a bad decision

		#
		return xmlLog.xmlLog(filename, self.xmlRoot, self.xmlEntry, self.xmlEntryDef[:]) 

	def main(self):
		run = self.xmlLog.run

		# Enter command interpreter mode
		while ( run ):
			try:
				cmnd = raw_input(" > ")
			except KeyboardInterrupt:
				print ""
				print "Exiting..."
				break

			if len(cmnd) > 0:
				cmndKey = cmnd.split(" ")[0]
				args = cmnd.split(" ")[1:]
				#!print cmnd, cmndKey, commands.keys()
				if cmndKey in self.commands.keys():
					#!print commands[cmndKey]
					run = self.commands[cmndKey](*args)

if __name__ == "__main__":
	cli = xmlCli()			
	cli.main()

