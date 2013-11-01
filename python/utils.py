from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree
import os

def prepExecData(module, method, path=""):
	"""	Prepares data to fetch help of found methods of the
		modules.
		Args:
			module(str): module to import
			method(str): method whose help needs to be printed.
			path(str): location of the module not in sys.path
		Return:
				returns a concatenated command as a string 
	"""
	if path:
		return 'python -c "import sys; sys.path.insert(0,\''+path+'\'); import '+module+'; help('+module+'.'+method+')'""
	else:
		if module.find(".") == -1:
			return 'python -c "from '+module+' import '+method+'; help('+method+')"'
		else:
			impMod = module.split(".")[0]
			return 'python -c """import '+impMod+';\nif \''+method+'\' in dir('+module+'):\n\thelp('+module+'.'+method+')\nelse:\n\tfrom '+impMod+' import '+method+'\n\thelp('+method+')"""'


class ReadWriteCustomPathsToDisk(object):
	"""	Reads and writes the XML file using ElementTree
	"""
	def __init__(self, modulePath):
		super(ReadWriteCustomPathsToDisk, self).__init__()
		self.modulePath = modulePath

	def _xmlFileLocation(self):
		xmlFileLocation =  os.path.join(os.path.expanduser("~"), "Documents","searchMethod","modules.xml")
		if os.path.exists(xmlFileLocation):
			return xmlFileLocation

	def readXml(self):
		xmlFile = self._xmlFileLocation()
		root = etree.parse(xmlFile).getroot()
		return root

	def xmlData(self):
		modPath = {}
		lst = self.readXml().getchildren()
		for module in lst:
			modPath[module.attrib['name']] = module.text
		return modPath
		

	def _entryExist(self):
		if self.modulePath in self.xmlData().values():
			return True
		else:
			return False

	def addEntry(self):
		path = self.modulePath
		if self._entryExist():
			return
		else:
			root = self.readXml() if self._xmlFileLocation else Element("modules")

		tree = ElementTree(root)
		childPath = Element("module")
		childPath.set("name", os.path.basename(path))
		root.append(childPath)
		childPath.text = path
		return tree

	def updateXml(self):
		tree = self.addEntry()
		print "Saving to %s " % self._xmlFileLocation()
		tree.write(open(self._xmlFileLocation(),'w'))


xmlFile = ""
xmlLocation =  os.path.join(os.path.expanduser("~"), "Documents","searchMethod")
xmlFile = os.path.join(xmlLocation,"module.xml")
def makeXml(path):
	root = Element("modules")
	tree = ElementTree(root)
	childPath = Element("module")
	childPath.set("name", os.path.basename(path))
	root.append(childPath)
	childPath.text = path
	# print etree.tostring(root)
	tree.write(open(xmlFile,'w'))

# makeXml("/Desktop/filterList")
root = etree.parse(xmlFile).getroot()
lst = root.getchildren()
print lst
for each in lst:
	print each.text ,each.tag, each.attrib['name']
	# print each.findtext('module')
	# if each.findtext("/Desktop/filterList"):
	# 	print "Yippe"

# makeXml("~/Documens/sorter.mod")

# xmlRWObj = ReadWriteCustomPathsToDisk("~/Documens/sorter.mod")
# xmlRWObj.readXml()