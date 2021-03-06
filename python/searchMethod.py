import os
import sys
import string
import subprocess
import searchMethodUI

from PyQt4 import QtCore, QtGui
from autoComplete import TagsCompleter

import pkgutil
from PyQt4.Qt import Qt, QObject, SIGNAL, SLOT
import utils



class SearchMethod(object):
	"""	SearchMethod class contains methods to
		filter the list of methods to match the 
		starting prefix.
		Args:
			modules(List): List of all the modules
			prefix(string): prefix to filter the list
			path(string): path of the module not in sys.path
	"""
	def __init__(self, modules, prefix="", path="", terminal=False):
		super(SearchMethod, self).__init__()
		self._module = modules
		self._prefix = prefix
		self._terminalmode = terminal
		self._path = path

	def _listOfMethods(self, lookinside):
		"""	Performs an import of the argument and retuns a list of all methods in it.
			Args:
				lookinside(string): module name as string to import.
			Returns(List): a list of methods in the module passed as argument
		"""
		try:
			if lookinside:
				return dir(__import__(lookinside, globals={}, locals={}, fromlist=[], level=-1))
		except ImportError:
			return []

	def lookInside(self, lookin=None):
		""" looks inside the method passed in argument
			Args:
				lookin(List): a list of modules to look as string
			Returns:
				lookinsideDict(Dict): a dictionary of module name as key
				and list of methods as value.
		"""
		lookinsideDict = {}
		if lookin:		
			for each in lookin:
				if self._listOfMethods(each) != []:
					lookinsideDict[each]=self._listOfMethods(each)
		return lookinsideDict

	def filterList(self, lst):
		"""	Filter the list with the prefix.
		"""
		filteredList = []
		for eachItem in lst:
			if eachItem.startswith(self._prefix):
				filteredList.append(eachItem)
		if filteredList == []:
			print (" This module/package doesn't have any method starting with letter '%s'." % self._prefix)
			return []
		return filteredList

	def filterMethods(self):
		"""	Filters the items in a list of methods
			Returns:
				filteredDict(Dict): returns the dictionary of
				module name as key and filtered methods of a list
				as value.
		"""
		moduleMethds = self.lookInside(self._module)
		filteredDict = {}
		if moduleMethds:
			for keymod, valmeths in moduleMethds.iteritems():
				if self._prefix:
					value = self.filterList(valmeths)
				else:
					value = valmeths
				# if no method for value is found do not 
				# add to dictionary
				if value:
					filteredDict[keymod] = value
		return filteredDict

	def searchResults(self):
		newLst = []
		for key, value in  self.filterMethods().iteritems():
			newLst.append("%s: %s" % (key, ", ".join(value)))
			if self._terminalmode:
				methStr = "methods" if len(value)> 1 else "method" 
				print("Module: %s has %s %s" % (key, methStr, value))
		return newLst

	def printMethodHelp(self):
		if not self.searchResults():
			print "No matching method found of prefix you supplied."
		# This is done becuase methods help could be large and user may have to scroll up/down.
		viewHelp = raw_input("Print help on methods found? Enter yes or y to print.\n>> ")
		if viewHelp == "yes" or viewHelp == "y":
			for module, methods in self.filterMethods().iteritems():
				for method in methods:
					proc = subprocess.Popen(utils.prepExecData(module, method, self._path),  shell=True, stdout=subprocess.PIPE)
					print(proc.stdout.read())


class SearchMethodUI(QtGui.QWidget, searchMethodUI.Ui_searchMethodMainWidget):
	"""	This class defines methods for GUI and
		the methods that update or change the content of UI.
	"""
	def __init__(self, parent=None):
		super(SearchMethodUI, self).__init__(parent)
		self.setupUi(self)
		self._connections()
		self.pathAdded = None
		self.xmlDataObj = utils.ReadWriteCustomPathsToDisk()
		self.__moduleCompleter()

	def main(self):
		self.show()

	def _connections(self):
		self.searchBtn.clicked.connect(self._populateResults)
		self.searchListView.clicked.connect(self._populateMethodsList)
		self.browseBtn.clicked.connect(self._browseModulePath)

	def keyPressEvent(self, keyevent):
		"""	Capture key to execute and exit 
			on Enter and Escape respectively.
		"""
		if str(self.lookInsideEdit.text()):
			if keyevent.key() == QtCore.Qt.Key_Enter-1:
				self._populateResults()
		if keyevent.key() == QtCore.Qt.Key_Escape:
			self.close()

	def __listAllModules(self):
		"""	This method returns all the modules installed in python
			including the built in ones.
		"""
		allmodules = list(sys.builtin_module_names)
		allmodules += list(t[1] for t in pkgutil.iter_modules())
		allmodules = sorted(allmodules)
		return allmodules

	def __moduleCompleter(self):
		"""	Auto completes module names in self.lookInsideEdit
		"""
		completer = TagsCompleter(self.lookInsideEdit, self.__listAllModules())
		completer.setCaseSensitivity(Qt.CaseInsensitive)
		QObject.connect(self.lookInsideEdit, 
			SIGNAL('text_changed(PyQt_PyObject, PyQt_PyObject)'), 
			completer.update)
		QObject.connect(completer, SIGNAL('activated(QString)'),
			self.lookInsideEdit.complete_text)
 		completer.setWidget(self.addPathEdit)
		completer.setWidget(self.lookInsideEdit)

	def _browseModulePath(self):
		"""	This module launches the directory browser
			to locate the module as set the path.
		"""
		selectedDir = str(QtGui.QFileDialog.getExistingDirectory(self,"Browse"))
		if selectedDir:
			writObj = utils.ReadWriteCustomPathsToDisk()
			if not writObj._entryExist(selectedDir):
				writObj.updateXml()
			self.addPathEdit.setText(selectedDir)
			self.lookInsideEdit.setText(os.path.split(selectedDir)[-1])
			self.pathAdded = selectedDir
		
	def outputHelp(self):
		"""	This methods outputs help on the self.helpOnSelMethodTxtEdit
		"""
		module = ""
		items = self.searchListView.selectedIndexes()
		if items:

			for item in items:
				module = str(item.data().toString()).split(":")[0]
			method = ""
			items = self.methodListView.selectedIndexes()
			for selItem in items:
				method = str(selItem.data().toString())
			data = utils.prepExecData(module, method, self.pathAdded)

			output = os.popen(data).read()
			self.helpOnSelMethodTxtEdit.setText(output)
			# if something is in output it means data resulted of execution of 
			# os.popen succeded
			if output:
				return True
		else:
			QtGui.QMessageBox.about(self, "Select the Module/Package first !!!", \
				"Please select an item from search search above.")

	def _populateMethodsList(self):
		"""	Populates the self.methodListView with all methods shown
			in the search result
			Returns:
				methodList(List): list of methods
		"""
		methodList = []
		items = self.searchListView.selectedIndexes()
		for item in items:
			methodList = str(item.data().toString()).split(":")[-1]
		methodList = methodList.translate( None, string.whitespace ).split(",")
		model = utils.MyListModel(methodList, self)
		self.methodListView.setModel(model)
		self.methodListView.selectionModel().selectionChanged.connect(self.outputHelp)
		return methodList


	def _populateResults(self):
		"""	Populates the self.searchListView with the result
			of all methods when no prefix is entered or module's
			methods with matching prefix
		"""
		lookinlst = str(self.lookInsideEdit.text()).split(",")
		searchMethObj = SearchMethod(modules=lookinlst, prefix=str(self.lineEdit.text()), path="")
		founds = searchMethObj.searchResults()
		self.lm = utils.MyListModel(founds, self)
		self.searchListView.setModel(self.lm)
		self.searchListView.selectionModel().selectionChanged.connect(self._populateMethodsList)


def main():
	app = QtGui.QApplication(sys.argv)
	smObj = SearchMethodUI()
	smObj.main()
	app.exec_()
	
if __name__ == '__main__':
	main()
