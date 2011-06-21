#!/usr/bin/env python
#
# Kevin's XML module
#

import xml.etree.ElementTree as etree
import shutil
import os.path

class kmpXML:
	def __init__(self, filename):
		self.run = True
		self.dirty = False
		self.filename = filename
		# Split filename into dir and name
		self.directory = os.path.split(filename)[0]
		self.logfilename = os.path.split(filename)[1]
		# Handle empty directories when file is in cwd
		if self.directory == '':
			self.directory = "."

		# Check to see if the file exists
		if not os.path.isfile(filename):
			print filename, "DOES NOT EXIST!"

			# Ask the user if the file should be created
			decision = raw_input("Would you like to create it? (y/n) ")
			if decision in ("Yes", "yes", "Y", "y"):
				# Create the file
				print "Creating %s" % filename
				self.createEmptyXML(filename, xmlRoot)
			else:
				self.run = False

		if self.run == True:
			# Read the file
			print "Reading %s" % filename
			self.tree, self.root = kmpXML.readXML(filename)

	def recursiveAddElem(self, labels, entries, elem, level=0):
		for i in range(len(labels)):
			if type(labels[i]) is str:
				e = etree.SubElement(elem, labels[i])
				e.text = entries[i]
			if type(labels[i]) is dict:
				key = labels[i].keys()[0]
				e = etree.SubElement(elem, key)
				self.recursiveAddElem(labels[i][key], entries[i], e, level+1)

		if level == 0:
			pass

	def appendEntry(self, root, entryStr):
		length = len(root) + 1
		entry = etree.SubElement(root, entryStr, index="%i" % length)
		return entry

	def addEntry(self, xmlEntry, labels, entries):
		# Add an entry to the root
		entry = self.appendEntry(self.root, xmlEntry)
		# Populate the entry with the users input
		self.recursiveAddElem(labels, entries, entry)
		# Set the dirty flag
		self.dirty = True

	def indent(self, elem, level=0):
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

	def createEmptyXML(self, filename, xmlRoot):
		tree = etree.ElementTree()
		root = etree.Element(xmlRoot)
		# Add a comment so an empty xml file can be properly read
		comment = etree.Comment("This is an empty file")
		root.append(comment)
		indent(root)
		tree._setroot(root)
		tree.write(filename)

	def readXML(self, filename):
		# Protection is done at a higher level
		tree = etree.parse(filename)
		root = tree.getroot()
		return tree, root

	def saveXML(self):
		# Move current file to backup
		newfilename = "%s.bup" % filename
		shutil.move(filename, newfilename)
		# Make tree presentable
		indent(self.root)
		# Write file
		self.tree.write(self.filename)
		# Clear the dirty flag
		self.dirty = False
