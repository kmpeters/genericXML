#!/usr/bin/env python


def showHelp(args):
	#print "showHelp()"
	print "showHelp(", args, ")"

def printStuff(args):
	#print "printStuff()"
	print "printStuff(", args, ")"
	print xmlDef
	#!for e in xmlDef:
	#!	if type(e) is str:
	#!		print e, "is a string"
	#!	elif type(e) is list:
	#!		print e, "is a list"
	#!	else:
	#!		print type(e)
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

def listStuff(args):
	#print "listStuff()"
	print "listStuff(", args, ")"

def correct(args):
	#print "correct()"
	print "correct(", args, ")"

def main():
	while ( True ):
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
				commands[cmndKey](args)

if __name__ == "__main__":

	commands = { 
			 "help":  showHelp,
			    "h":  showHelp,  
			"print":  printStuff,
			    "p":  printStuff,
			 "list":  listStuff,
			    "l":  listStuff,
			    "c":  correct
		   }

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

