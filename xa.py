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
import readline

import xmlLog

class xmlCli:
	def __init__(self):
		self.userDefinitions()
		# Flag to continue prompting for commands
		self.run = True
		# Flag to abort when keyboard interrupt
		self.broken = False
		# Flag to switch input auto-correct behavior
		self.correcting = False

		# Open the log file
		self.filename = self._getLogFilename()

		if self.run == True:
			print "Reading %s" % self.filename
			self.xmlLog = xmlLog.xmlLog(self.filename, self.xmlRoot, self.xmlEntry, self.xmlEntryDef[:])
		else:
			# This probably isn't necessary
			self.xmlLog = None

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
	def prePromptHook(self, label, array):
		return True

	def postPromptHook(self, lable, array, response):
		return True

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
			if self.broken == True:
				break
			if type(labels[i]) is str:
				# Allow for printing auto-complete suggestions or skipping entry of elements (customizing prompt requires more args)
				stillDoPrompt = self.prePromptHook(labels[i], array)

				if stillDoPrompt == True:
					# Generic promptStr
					promptStr = "  " * level + "%s: " % labels[i]
					# Will it be possible to validate response?

					# Catch KeyboardInterrupt to all the user to exit the entry process
					try:
						response = raw_input(promptStr)

						# Allow correction of response or insertion of default value of current or previously skipped field
						stillAppendResponse = self.postPromptHook(labels[i], array, response)

						if stillAppendResponse == True:
							array.append(response)
						else:
							# post prompt hook must have appended to the array
							pass

						print "array = ", array

						# Remove entry items from command history
						if response != '':
							pos = readline.get_current_history_length() - 1
							readline.remove_history_item(pos)

					except KeyboardInterrupt:
						self.broken = True
						print ""
						print "Aborting..."
						break

				else:
					# pre prompt hook must have appended to the array, or let it be handled by post prompt hook
					continue

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
		#!print "addData(", args, ")"
	
		print ""
		userEntries = self._getUserInput()
		print ""

		# Only add the entry if the user didn't Ctrl+c out of it
		if self.broken == False:
			self.xmlLog.addEntry(userEntries)
		else:
			self.broken = False
	
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
		self.correcting = True
		userCorrections = self._getUserInput()
		self.correcting = False
		print ""

		# Correct entry if the user didn't Ctrl+c out of it
		if self.broken == False:
			self.xmlLog.correctEntry(arrayIndex, userCorrections)
		else:
			self.broken = False

		return True

	def _getLogFilename(self):
		# Allow the user to specify an xml file when running the script
		if len(sys.argv) > 1:
			filename = sys.argv[1]
		else:
			filename = "%s/%s" % (os.getcwd(), self.xmlFilename)
			# Alternately could use the script location (sys.argv[0]), but that seems like a bad decision

		# Check to see if the file exists
		if not os.path.isfile(filename):
			print filename, "DOES NOT EXIST!"

			# Ask the user if the file should be created
			try:
				decision = raw_input("Would you like to create it? (y/n) ")
			except KeyboardInterrupt:
				print
				decision = "No"

			if decision in ("Yes", "yes", "Y", "y"):
				# Create the file
				print "Creating %s" % filename
			else:
				self.run = False

		return filename

	def main(self):
		# Enter command interpreter mode
		while ( self.run ):
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
					self.run = self.commands[cmndKey](*args)

if __name__ == "__main__":
	cli = xmlCli()			
	cli.main()

