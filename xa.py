#!/usr/bin/env python


def showHelp(args):
	#print "showHelp()"
	print "showHelp(", args, ")"

def printStuff(args):
	#print "printStuff()"
	print "printStuff(", args, ")"

def listStuff(args):
	#print "listStuff()"
	print "listStuff(", args, ")"

def correct(args):
	#print "correct()"
	print "correct(", args, ")"

commands = { 
		 "help":  showHelp,
		    "h":  showHelp,  
		"print":  printStuff,
		    "p":  printStuff,
		 "list":  listStuff,
		    "l":  listStuff,
		    "c":  correct
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
			args = cmnd.split(" ")[1:]
			print cmnd, cmndKey, commands.keys()
			if cmndKey in commands.keys():
				print commands[cmndKey]
				commands[cmndKey](args)

if __name__ == "__main__":
	main()

