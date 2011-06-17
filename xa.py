#!/usr/bin/env python


def showHelp(*args):
	#print "showHelp()"
	print "showHelp(", args, ")"

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

def listStuff(*args):
	#print "listStuff()"
	print "listStuff(", args, ")"

def correct(*args):
	#print "correct()"
	print "correct(", args, ")"

def addData(*args):
	print "addData(", args, ")"

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
			tree = etree.ElementTree()
			log = etree.Element(xmlRoot)
			# Add a comment so an empty xml file can be properly read
			comment = etree.Comment("This is an empty file")
			log.append(comment)
			indent(log)
			tree._setroot(log)
			tree.write(filename)
		else:
			print "Exiting"
			return (False, None, None)

	# Read the file
	print "Reading %s" % filename
	tree = etree.parse(filename)
	log = tree.getroot()
	return (True, tree, log)

# Should probably move this to XML-specific file
def indent(elem, level=0):
	i = "\n" + level*"  "
	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + "  "
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
		for elem in elem:
			indent(elem, level+1)
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
	else:
		if level and (not elem.tail or not elem.tail.strip()):
			elem.tail = i

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
				commands[cmndKey](*args)

if __name__ == "__main__":
	import sys
	import os
	import xml.etree.ElementTree as etree

	commands = { 
			 "help":  showHelp,
			    "h":  showHelp,  
			"print":  printStuff,
			    "p":  printStuff,
			 "list":  listStuff,
			    "l":  listStuff,
			    "c":  correct,
			  "add":  addData,
			    "a":  addData
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

