from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree
import os
from PyQt4.Qt import Qt, QObject, QLineEdit
from PyQt4 import QtCore, QtGui

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
	def __init__(self):
		super(ReadWriteCustomPathsToDisk, self).__init__()
		self.modulePath = ''

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
		

	def _entryExist(self, path):
		if path in self.xmlData().values():
			return True
		else:
			self.modulePath = path
			return False

	def addEntry(self):
		path = self.modulePath
		if self._entryExist(path):
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
		print "Adding newly added module to quick access."
		tree.write(open(self._xmlFileLocation(),'w'))


class MyListModel(QtCore.QAbstractListModel):
	def __init__(self, datain, parent=None, *args):
		""" datain: a list where each item is a row
		"""
		QtCore.QAbstractListModel.__init__(self, parent, *args)
		self.listdata = datain

	def rowCount(self, parent=QtCore.QModelIndex()):
		return len(self.listdata)

	def data(self, index, role):
		if index.isValid() and role == QtCore.Qt.DisplayRole:
			return QtCore.QVariant(self.listdata[index.row()])
		else:
			return QtCore.QVariant()

class AddPathLineEdit(QLineEdit, QtCore.QObject):

	"""	docstring for AddPathLineEdit
	"""
	def __init__(self, arg):
		super(AddPathLineEdit, self).__init__()
		self.fileSystemCompleter()
		self.xmlDataObj = ReadWriteCustomPathsToDisk()
		self.defaultList = self.xmlDataObj.xmlData().values()
		self._pathsListCompleter()
		self.textEdited.connect(self._switchCompleter)

	def focusInEvent(self, event):
		self._switchCompleter()
		QtGui.QLineEdit.focusInEvent(self, event)
		self.setModified(False)
		self.completer().complete()

	def fileSystemCompleter(self):
		self._model = QtGui.QFileSystemModel(self)
		self._model.setRootPath(QtCore.QDir.currentPath())
		self._model.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot)
		self._model.setNameFilterDisables(0)
		# Initiate completer for FileSystemModel
		self._fileCompleter = QtGui.QCompleter(self._model)
		self._fileCompleter.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
		self._fileCompleter.setModel(self._model)

	def _pathsListCompleter(self):
		self._completerList = QtCore.QStringList(self.defaultList)
		# Initiates Completer for List we are getting from XML
		self._lineEditCompleter = QtGui.QCompleter(self._completerList)
		self._lineEditCompleter.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
		self.setCompleter(self._lineEditCompleter)

	def _switchCompleter(self):
		if len(self.text()) == 0:
			self.setCompleter(self._lineEditCompleter)
			self.completer().complete()
		else:
			self.setCompleter(self._fileCompleter)
		