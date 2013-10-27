import os
import sys
import string
import subprocess
import searchMethodUI
from PyQt4 import QtCore, QtGui

sys.path.insert(0, '/Users/sanjeevkumar/Development/python/listFilter/python/')
import filterList

class SearchMethod(object):
	"""	SearchMethod class contains methods to
		filter the list of methods to match the 
		starting prefix.
		Args:
			modules(List): List of all the modules
			prefix(string): prefix to filter the list
			path(string): path of the module not in sys.path
	"""
	def __init__(self, modules, prefix, path="", terminal=False):
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

	def filterMethods(self):
		"""	Filters the items in a list of methods
			Returns:
				filteredDict(Dict): returns the dictionary of
				module name as key and filtered methods of a list
				as value.
		"""
		moduleMethds = self.lookInside(self._module)
		filteredDict = {}
		flObj = filterList.FilterList(self._prefix)
		if moduleMethds:
			for keymod, valmeths in moduleMethds.iteritems():
				value = flObj.filterList(valmeths)
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
				print "Module: %s has %s %s" % (key, methStr, value)
		return newLst

	def printMethodHelp(self):
		if not self.searchResults():
			print "No matching method found of prefix you supplied."
		# This is done becuase methods help could be large and user may have to scroll up/down.
		viewHelp = raw_input("Print help on methods found? Enter yes or y to print.\n>> ")
		if viewHelp == "yes" or viewHelp == "y":
			for module, methods in self.filterMethods().iteritems():
				for method in methods:
					proc = subprocess.Popen(prepExecData(module, method, self._path),  shell=True, stdout=subprocess.PIPE)
					print proc.stdout.read()


class SearchMethodUI(QtGui.QWidget, searchMethodUI.Ui_searchMethodMainWidget):
	"""docstring for SearchMethodUI"""
	def __init__(self, parent=None):
		super(SearchMethodUI, self).__init__(parent)
		self.setupUi(self)
		self._connections()
		self.pathAdded = None

	def main(self):
		self.show()

	def _connections(self):
		self.searchBtn.clicked.connect(self._populateResults)
		self.searchListView.clicked.connect(self._populateMethodsList)
		self.methodListView.clicked.connect(self.outputHelp)
		self.browseBtn.clicked.connect(self._browseModulePath)

	def keyPressEvent(self, keyevent):
		"""	Capture key to execute and exit 
			on Enter and Escape respectively.
		"""
		if (self.lookInsideEdit.text() and self.lineEdit.text()):
			if keyevent.key() == QtCore.Qt.Key_Enter-1:
				self._populateResults()
		if keyevent.key() == QtCore.Qt.Key_Escape:
			self.close()


	def _browseModulePath(self):
		"""	This module launches the directory browser
			to locate the module as set the path.
		"""
		selectedDir=str(QtGui.QFileDialog.getExistingDirectory(self,"Browse"))
		if selectedDir:
			self.addPathEdit.setText(selectedDir)
			self.pathAdded = selectedDir
		
	def outputHelp(self):
		module = ""
		items = self.searchListView.selectedIndexes()
		for item in items:
			module = str(item.data().toString()).split(":")[0]
		method = ""
		items = self.methodListView.selectedIndexes()
		for selItem in items:
			method = str(selItem.data().toString())


		data = prepExecData(module, method, self.pathAdded)

		output = os.popen(data).read()

		self.helpOnSelMethodTxtEdit.setText(output)
		# if something is in output it means data resulted of execution of os.popen succeded
		if output:
			return True

	def _populateMethodsList(self):
		methodList = []
		items = self.searchListView.selectedIndexes()
		for item in items:
			methodList = str(item.data().toString()).split(":")[-1]
		methodList = methodList.translate( None, string.whitespace ).split(",")
		model = MyListModel(methodList, self)
		self.methodListView.setModel(model)
		self.methodListView.selectionModel().selectionChanged.connect(self.outputHelp)
		return methodList


	def _populateResults(self):
		lookinlst = str(self.lookInsideEdit.text()).split(",")
		searchMethObj = SearchMethod(modules=lookinlst, prefix=str(self.lineEdit.text()),path = "")
		founds = searchMethObj.searchResults()
		self.lm = MyListModel(founds, self)
		self.searchListView.setModel(self.lm)
		self.searchListView.selectionModel().selectionChanged.connect(self._populateMethodsList)


class MyListModel(QtCore.QAbstractListModel):
	def __init__(self, datain, parent=None, *args):
		""" datain: a list where each item is a row
		"""
		QtCore.QAbstractTableModel.__init__(self, parent, *args)
		self.listdata = datain

	def rowCount(self, parent=QtCore.QModelIndex()):
		return len(self.listdata)

	def data(self, index, role):
		if index.isValid() and role == QtCore.Qt.DisplayRole:
			return QtCore.QVariant(self.listdata[index.row()])
		else:
			return QtCore.QVariant()

def prepExecData(module, method, path=""):
	"""	Prepares data to fetch help of found methods of the
		modules.
		Args:
			module(str): module to import
			method(str): method whose help needs to be printed.
			path(str): location of the module not in sys.path
		Return:
			data(str): returns a string
	"""
	# when path added is not in sys.path by default
	if path:
		data = 'python -c "import sys; sys.path.insert(0,\''+path+'\'); import '+module+'; help('+module+'.'+method+')"'
	else:
		data = 'python -c "import '+module+'; help('+module+'.'+method+')"'
	return data

def main():
	app = QtGui.QApplication(sys.argv)
	smObj = SearchMethodUI()
	smObj.main()
	app.exec_()
	
if __name__ == '__main__':
	main()


