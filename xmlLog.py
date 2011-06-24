#!/usr/bin/env python
#
# xmlLog module
#

import xml.etree.ElementTree as etree
import shutil
import os.path

class xmlLog:
	def __init__(self, filename, xmlRoot, xmlEntry, xmlEntryDef):
		# access directly from cli: run, dirty, root
		self.run = True
		self.dirty = False
		self.filename = filename

		# Split filename into dir and name
		self.directory = os.path.split(filename)[0]
		self.logfilename = os.path.split(filename)[1]
		# Handle empty directories when file is in cwd
		if self.directory == '':
			self.directory = "."

		self.xmlRoot = xmlRoot
		self.xmlEntry = xmlEntry
		self.xmlEntryDef = xmlEntryDef

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
				self._createEmptyXML(filename, xmlRoot)
			else:
				self.run = False

		if self.run == True:
			# Read the file
			print "Reading %s" % filename
			self.tree, self.root = self.readXML(filename)

	def dumpTest(self, elem):
		# In python 2.7 getiterator() is replaced with iter()
		for i in elem.getiterator():
			print i
			# In later versions tostring will accept a method arg to change output
			print etree.tostring(i)

	def _recursiveGetElemContent(self, elem, array, level=0):
		for e in elem:
			if len(e) == 0:
				if e.text == None:
					text = ""
				else:
					text = e.text
				#!print "    " * level + e.tag + "\t" + text
				array.append(text)
			else:
				#!print "    " * level + e.tag
				array.append([])
				self._recursiveGetElemContent(e, array[len(array)-1], level+1)

		if level == 0:
			return array[:]

	def getPrintLogArray(self):
		logArray = []
		for elem in self.root:
			#!print elem
			elemArray = []
			if elem.tag == self.xmlEntry:
				array = self._recursiveGetElemContent(elem, elemArray)
				#!print array, len(array)
				logArray.append( array )
		return logArray[:]

	def _recursiveAddElem(self, labels, entries, elem, level=0):
		for i in range(len(labels)):
			if type(labels[i]) is str:
				e = etree.SubElement(elem, labels[i])
				e.text = entries[i]
			if type(labels[i]) is dict:
				key = labels[i].keys()[0]
				e = etree.SubElement(elem, key)
				self._recursiveAddElem(labels[i][key], entries[i], e, level+1)

		if level == 0:
			pass

	def _appendEntry(self, root, entryStr):
		length = len(root) + 1
		entry = etree.SubElement(root, entryStr, index="%i" % length)
		return entry

	def addEntry(self, entries):
		# Add an entry to the root
		entry = self._appendEntry(self.root, self.xmlEntry)
		# Populate the entry with the users input
		self._recursiveAddElem(self.xmlEntryDef, entries, entry)
		# Set the dirty flag
		self.dirty = True

	def _indent(self, elem, level=0):
		i = "\n" + level*"  "
		if len(elem):
			if not elem.text or not elem.text.strip():
				elem.text = i + "  "
			if not elem.tail or not elem.tail.strip():
				elem.tail = i
			for elem in elem:
				self._indent(elem, level+1)
			if not elem.tail or not elem.tail.strip():
				elem.tail = i
		else:
			if level and (not elem.tail or not elem.tail.strip()):
				elem.tail = i

	def _createEmptyXML(self, filename, xmlRoot):
		tree = etree.ElementTree()
		root = etree.Element(xmlRoot)
		# Add a comment so an empty xml file can be properly read
		comment = etree.Comment("This is an empty file")
		root.append(comment)
		self._indent(root)
		tree._setroot(root)
		tree.write(filename)

	def readXML(self, filename):
		# Protection is done at a higher level
		tree = etree.parse(filename)
		root = tree.getroot()
		return tree, root

	def saveXML(self):
		# Move current file to backup
		newfilename = "%s.bup" % self.filename
		shutil.move(self.filename, newfilename)
		# Make tree presentable
		self._indent(self.root)
		# Write file
		self.tree.write(self.filename)
		# Clear the dirty flag
		self.dirty = False
