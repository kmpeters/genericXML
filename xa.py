#!/usr/bin/env python


def showHelp():
	print "showHelp()"

def printStuff():
	print "printStuff()"

def listStuff():
	print "listStuff()"

def correct():
	print "correct()"

commands = { 
		"help":showHelp,
		"h":showHelp,  
		"print":printStuff,
		"p":printStuff,
		"list":listStuff,
		"l":listStuff,
		"c":correct
	   }

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
			print cmnd, cmndKey, commands.keys()
			if cmndKey in commands.keys():
				print commands[cmndKey]
				commands[cmndKey]()

if __name__ == "__main__":
	main()

