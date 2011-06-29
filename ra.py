#!/usr/bin/env python
#
# report append, based on generic xa.py
#

import xa

class raCli(xa.xmlCli):
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

		self.xmlFilename = "work_log.xml"
		self.xmlRoot = "log"
		self.xmlEntry = "entry"

		self.xmlEntryDef = [
				"date",
				"duration",
				"category",
				"keyword",
				"description",
				"resolution"
			]

if __name__ == "__main__":
	cli = raCli()
	cli.main()
