import os
import sys
import string
from PyQt4 import QtCore, QtGui
from tempfile import TemporaryFile
sys.path.insert(0, '/Users/sanjeevkumar/Development/python/listFilter/python/')
import searchMethodUI
import filterList


class SearchMethod(object):
	"""docstring for SearchMethod"""
	def __init__(self, module, prefix, path=""):
		super(SearchMethod, self).__init__()
		self._module = module
		self._prefix = prefix
		self._addPath(path)

	def _addPath(self, path):
		"""	adds path to sys paths to import a
			custom or module that is not in sys paths.
			Args:
				path(string): path to add to sys.path
		"""
		if path != "":			
			if os.path.isdir(path):
				sys.path.insert(0, path)


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

		t = TemporaryFile()
		# when path added is not in sys.path by default
		if self.pathAdded:
			data = 'python -c "import sys; sys.path.insert(0,\''+self.pathAdded+'\'); import '+module+'; help('+module+'.'+method+')"'
		else:
			data = 'python -c "import '+module+'; help('+module+'.'+method+')"'

		t.write(data)
		t.seek(0)
		output = os.popen(t.read()).read()
		t.closed
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

	def _searchResults(self):
		lookinlst = str(self.lookInsideEdit.text()).split(",")
		searchMethObj = SearchMethod(module=lookinlst, prefix=str(self.lineEdit.text()),path = "")
		newLst = []
		for key, value in  searchMethObj.filterMethods().iteritems():
			newLst.append("%s: %s" % (key, ", ".join(value)))
		return newLst

	def _populateResults(self):
		founds = self._searchResults()
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


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	smObj = SearchMethodUI()
	smObj.main()
	app.exec_()


