#!/usr/bin/env python

class genXml:
	def __init__(self):
		self.userDefinitions()

		# Open the log file
		self.xmlLog = self.openLogFile()

	def userDefinitions(self):
		self.commands = { 
				 "help": self.dummy,
				    "h": self.dummy,  
				"print": self.printStuff,
				    "p": self.printStuff,
				 "list": self.dummy,
				    "l": self.dummy,
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
		return True

	def showHelp(self, *args):
		#print "showHelp()"
		print "showHelp(", args, ")"
		return True

	def listStuff(self, *args):
		#print "listStuff()"
		print "listStuff(", args, ")"
		return True

	def correct(self, *args):
		#print "correct()"
		print "correct(", args, ")"
		return True
	# End dummy functions

	def printStuff(self, *args):
		#print "printStuff()"
		print "printStuff(", args, ")"
		print self.xmlEntryDef
		self.recursivePrintList(self.xmlEntryDef)
	
		return True

	def recursivePrintList(self, arg):
		for i in arg:
			if type(i) is str:
				print i, "is a string"
			elif type(i) is list:
				print i, "is a list"
				self.recursivePrintList(i)
			elif type(i) is dict:
				# by design dictionary will only have one key
				key = i.keys()[0]
				print i, "is a dictionary"
				self.recursivePrintList(i[key])
			else:
				print type(i)

	def quit(self, *args):
		print "Exiting..."
		return False

	def save(self, *args):
		self.xmlLog.saveXML()
		return True

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
			elif type(labels[i]) is list:
				print "OMG!!! THIS IS A LIST!!!"
				array.append([])
				self.recursivePromptEntry(labels[i], array[i], level+1)
			elif type(labels[i]) is dict:
				array.append([])
				# by design dictionary will only have one key
				key = labels[i].keys()[0]
				print "  " * level + "[%s]" % key
				self.recursivePromptEntry(labels[i][key], array[i], level+1)
	
		if level == 0:
			#!print array
			pass

	def recursiveAddEntry(self, labels, entries, level=0):
		for i in range(len(labels)):
			if type(labels[i]) is str:
				print labels[i], "->",entries[i]
			if type(labels[i]) is dict:
				# by design dictionary will only have one key
				key = labels[i].keys()[0]
				print "*%s" % key
				self.recursiveAddEntry(labels[i][key], entries[i], level+1)

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

		# This code could be cleaner if xml definition stuff was moved
		self.xmlLog.addEntry(self.xmlEntry, self.xmlEntryDef, userEntries)
	
		return True

	def openLogFile(self):
		# Allow the user to specify an xml file when running the script
		if len(sys.argv) > 1:
			filename = sys.argv[1]
		else:
			filename = "%s/%s" % (os.getcwd(), self.xmlFilename)
			# Alternately could use the script location (sys.argv[0]), but that seems like a bad decision

		#
		return kmpXMLoo.kmpXML(filename, self.xmlRoot) 

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
	import sys
	import os
	import kmpXMLoo

	ui = genXml()			
	ui.main()
