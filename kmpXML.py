#!/usr/bin/env python
#
# Kevin's XML module
#

import xml.etree.ElementTree as etree
import shutil

def recursiveAddElem(labels, entries, elem, level=0):
	for i in range(len(labels)):
		if type(labels[i]) is str:
			e = etree.SubElement(elem, labels[i])
			e.text = entries[i]
		if type(labels[i]) is dict:
			key = labels[i].keys()[0]
			e = etree.SubElement(elem, key)
			recursiveAddElem(labels[i][key], entries[i], e, level+1)

	if level == 0:
		pass

def appendEntry(root, entryStr):
	length = len(root) + 1
	entry = etree.SubElement(root, entryStr, index="%i" % length)
	return entry

def addEntry(root, xmlEntry, labels, entries):
	# Add an entry to the root
	entry = appendEntry(root, xmlEntry)
	# Populate the entry with the users input
	recursiveAddElem(labels, entries, entry)

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

def createEmptyXML(filename, xmlRoot):
	tree = etree.ElementTree()
	root = etree.Element(xmlRoot)
	# Add a comment so an empty xml file can be properly read
	comment = etree.Comment("This is an empty file")
	root.append(comment)
	indent(root)
	tree._setroot(root)
	tree.write(filename)

def readXML(filename):
	# Protection is done at a higher level
	tree = etree.parse(filename)
	root = tree.getroot()
	return tree, root

def saveXML(tree, root, filename):
	# Move current file to backup
	newfilename = "%s.bup" % filename
	shutil.move(filename, newfilename)
	# Make tree presentable
	indent(root)
	# Write file
	tree.write(filename)
	# How to handle dirty flag?
