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
		self.xmlLog = self._openLogFile()

	def userDefinitions(self):
		self.commands = { 
				 "help": self.dummy,
				    "h": self.dummy,  
				  "def": self.printXmlDef,
				    "d": self.printXmlDef,
				"print": self.printXmlLog,
				    "p": self.printXmlLog,
			      "correct": self.correctEntry,
				    "c": self.correctEntry,
				  "add": self.addData,
				    "a": self.addData,
				 "quit": self.quit,
				 "save": self.save,
				    "s": self.save,
				 "dump": self.dump
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
	# End dummy functions

	def dump(self, *args):
		self.xmlLog.dumpTest(self.xmlLog.root)
		return True

	def printXmlDef(self, *args):
		#!print "printStuff(", args, ")"
		#!print self.xmlEntryDef
		self._recursivePrintList(self.xmlEntryDef)
		return True

	def _recursivePrintList(self, arg, level=0):
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
				self._recursivePrintList(i[key], level+1)
			else:
				print "Error: ", type(i)

	def _recursiveDisplayXmlEntry(self, labels, index, entry, level=0):
		if level == 0:
			print "index:\t\t%s" % index

		for i in range(len(labels)):
			if type(labels[i]) is str:
				if ( len(labels[i]) < 7 ):
					print "%s:\t\t%s" % (labels[i], entry[i])
				else:
					print "%s:\t%s" % (labels[i], entry[i])
			elif type(labels[i]) is dict:
				# by design dictionary will only have one key
				key = labels[i].keys()[0]
				# index doesn't really need to be passed to the lower levels, maybe make it optional
				self._recursiveDisplayXmlEntry(labels[i][key], index, entry[i], level+1)

		if level == 0:
			print

	def _displayXmlLog(self, contentArray):
		print
		for i in range(len(contentArray)):
			index = i + 1
			self._recursiveDisplayXmlEntry(self.xmlEntryDef, index, contentArray[i])

	def printXmlLog(self, *args):
		contentArray = self.xmlLog.getPrintLogArray()
		#!print contentArray
		self._displayXmlLog(contentArray)

		return True

	def quit(self, *args):
		if self.xmlLog.dirty == False:
			print "Exiting..."
			return False
		else:
			try:
				raw_ack = raw_input("You have unsaved changes, are you sure you want to quit without saving? ")
			except KeyboardInterrupt:
				print
				raw_ack = "No"
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

	def _recursivePromptEntry(self, labels, array, level=0):
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
				self._recursivePromptEntry(labels[i][key], array[i], level+1)
			else:
				print "--> Unhandled prompt entry type: ", type(labels[i])
	
		if level == 0:
			#!print array
			#!self.recursivePrintEntries(self.xmlEntryDef, array)
			pass

	def _getUserInput(self):
		# At this point in time there is no helpful printing of existing entries or autocomplete
		userInput = []
		self._recursivePromptEntry(self.xmlEntryDef, userInput)
		return userInput[:]

	def addData(self, *args):
		print "addData(", args, ")"
	
		print
		userEntries = self._getUserInput()
		print

		self.xmlLog.addEntry(userEntries)
	
		return True

	def correctEntry(self, *args):
		#!print "correctEntry(", args, ")"

		lastEntryIndex = len(self.xmlLog.root)

		# Determine desired entry
		if len(args) > 0:
			try:
				rawEntryIndex = int(args[0])
				if rawEntryIndex < 1:
					entryIndex = 1
				elif rawEntryIndex > lastEntryIndex:
					entryIndex = lastEntryIndex
				else:
					entryIndex = rawEntryIndex
			except ValueError:
				print "\"%s\" is not an integer. Try again." % args[0]
				return True
		else:
			# No argument was specified
			entryIndex = lastEntryIndex

		# Entry indices are number from one
		arrayIndex = entryIndex - 1

		# Get the desired entry
		entryArray = self.xmlLog.getPrintElemArray(arrayIndex)

		# Print the desired entry
		print ""
		print "Editing Entry #%s" % entryIndex
		print ""
		self._recursiveDisplayXmlEntry(self.xmlEntryDef, entryIndex, entryArray)

		# Prompt user for changes
		# Correct entry
		return True

	def _openLogFile(self):
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

