#!/usr/bin/env python

### Functions to customize (and maybe move to a different file)
def prePromptHook(arg):
	return

# Begin dummy functions
def dummy(*args):
	return True

def showHelp(*args):
	#print "showHelp()"
	print "showHelp(", args, ")"
	return True

def listStuff(*args):
	#print "listStuff()"
	print "listStuff(", args, ")"
	return True

def correct(*args):
	#print "correct()"
	print "correct(", args, ")"
	return True
# End dummy functions

def printStuff(*args):
	#print "printStuff()"
	print "printStuff(", args, ")"
	print xmlEntryDef
	recursivePrintList(xmlEntryDef)
	
	return True

def recursivePrintList(arg):
	for i in arg:
		if type(i) is str:
			print i, "is a string"
		elif type(i) is list:
			print i, "is a list"
			recursivePrintList(i)
		elif type(i) is dict:
			# by design dictionary will only have one key
			key = i.keys()[0]
			print i, "is a dictionary"
			recursivePrintList(i[key])
		else:
			print type(i)

def quit(*args):
	print "Exiting..."
	return False

def save(*args):
	global filename
	#!print tree, log, filename
	kmpXML.saveXML(tree, log, filename)
	return True

def recursivePromptEntry(labels, array, level=0):
	for i in range(len(labels)):
		if type(labels[i]) is str:
			# Allow for printing auto-complete suggestions or customizing prompt
			prePromptHook(labels[i])
			# Generic promptStr
			promptStr = "  " * level + "%s: " % labels[i]
			# Will it be possible to validate response?
			response = raw_input(promptStr)
			array.append(response)
		elif type(labels[i]) is list:
			print "OMG!!! THIS IS A LIST!!!"
			array.append([])
			recursivePromptEntry(labels[i], array[i], level+1)
		elif type(labels[i]) is dict:
			array.append([])
			# by design dictionary will only have one key
			key = labels[i].keys()[0]
			print "  " * level + "[%s]" % key
			recursivePromptEntry(labels[i][key], array[i], level+1)
	
	if level == 0:
		#!print array
		pass

def recursiveAddEntry(labels, entries, level=0):
	for i in range(len(labels)):
		if type(labels[i]) is str:
			print labels[i], "->",entries[i]
		if type(labels[i]) is dict:
			# by design dictionary will only have one key
			key = labels[i].keys()[0]
			print "*%s" % key
			recursiveAddEntry(labels[i][key], entries[i], level+1)

def getUserInput():
	# At this point in time there is no helpful printing of existing entries or autocomplete
	userInput = []
	recursivePromptEntry(xmlEntryDef, userInput)
	return userInput[:]

def addData(*args):
	print "addData(", args, ")"
	
	print
	userEntries = getUserInput()
	print

	# This code could be cleaner if xml definition stuff was moved
	kmpXML.addEntry(log, xmlEntry, xmlEntryDef, userEntries)
	
	return True

def openLogFile():
	# Allow the user to specify an xml file when running the script
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = "%s/%s" % (os.getcwd(), xmlFilename)
		# Alternately could use the script location (sys.argv[0]), but that seems like a bad decision

	# turn the filename into something useful (why was this needed in other code?)
	directory = os.path.split(filename)[0]
	logfilename = os.path.split(filename)[1]

	# Handle empty directories when file is in current dir
	if directory == '':
		directory = "."
	#print "%s/%s" % (directory, logfilename)

	# Check to see if the file exists
	if not os.path.isfile(filename):
		print filename, "DOES NOT EXIST!"

		# Ask the user if the file should be created
		decision = raw_input("Would you like to create it? (y/n) ")
		if decision in ("Yes", "yes", "Y", "y"):
			# Create the file
			print "Creating %s" % filename
			kmpXML.createEmptyXML(filename, xmlRoot)
		else:
			print "Exiting"
			return (False, None, None)

	# Read the file
	print "Reading %s" % filename
	tree, log = kmpXML.readXML(filename)
	return (True, tree, log, filename)

def main():
	global tree, log, filename
	# Open the log file
	run, tree, log, filename = openLogFile()

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
			if cmndKey in commands.keys():
				#!print commands[cmndKey]
				run = commands[cmndKey](*args)

if __name__ == "__main__":
	import sys
	import os
	import kmpXML

	commands = { 
			 "help":  dummy,
			    "h":  dummy,  
			"print":  printStuff,
			    "p":  printStuff,
			 "list":  dummy,
			    "l":  dummy,
			    "c":  dummy,
			  "add":  addData,
			    "a":  addData,
			 "quit":  quit,
			 "save":  save,
			    "s":  save
		   }

	xmlFilename = "generic_log.xml"
	xmlRoot = "log"
	xmlEntry = "entry"

	xmlEntryDef = [
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

	filename = ""
	tree = None
	log = None
				
	main()

