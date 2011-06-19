#!/usr/bin/env python
#
# Kevin's XML module
#

import xml.etree.ElementTree as etree

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

