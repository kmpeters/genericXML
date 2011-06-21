#!/usr/bin/env python

# Begin dummy functions
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

def quit(*args):
	print "Exiting..."
	return False

def printStuff(*args):
	#print "printStuff()"
	print "printStuff(", args, ")"
	print xmlDef
	recursivePrintList(xmlDef)

def recursivePrintList(arg):
	for i in arg:
		if type(i) is str:
			print i, "is a string"
		elif type(i) is list:
			print i, "is a list"
			recursivePrintList(i)
		else:
			print type(e)

def recursivePromptEntry(labels, array, level):
	for i in range(len(labels)):
		if type(labels[i]) is str:
			promptStr = "  " * level + "%s: " % labels[i]
			#response = raw_input("%s: " % labels[i])
			response = raw_input(promptStr)
			array.append(response)
		elif type(labels[i]) is list:
			array.append([])
			recursivePromptEntry(labels[i], array[i], level+1)

def getUserInput():
	# At this point in time there is no helpful printing of existing entries or autocomplete
	userInput = []
	recursivePromptEntry(xmlDef, userInput, 0)

def addData(*args):
	print "addData(", args, ")"
	
	print
	userEntries = getUserInput()
	print
	
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
	return (True, tree, log)

def main():
	# Open the log file
	run, tree, log = openLogFile()

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
			print cmnd, cmndKey, commands.keys()
			if cmndKey in commands.keys():
				print commands[cmndKey]
				run = commands[cmndKey](*args)

if __name__ == "__main__":
	import sys
	import os
	import kmpXML

	commands = { 
			 "help":  showHelp,
			    "h":  showHelp,  
			"print":  printStuff,
			    "p":  printStuff,
			 "list":  listStuff,
			    "l":  listStuff,
			    "c":  correct,
			  "add":  addData,
			    "a":  addData,
			 "quit":  quit
		   }

	xmlFilename = "generic_log.xml"
	xmlRoot = "log"

	xmlDef = [ 
			"date",
			"author",
			"remark",
			[
				"title",
				"subject",
				"entry",
				"effort"
			]
		]
				
	main()

