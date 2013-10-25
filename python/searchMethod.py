import os
import sys
from PyQt4 import QtCore, QtGui
sys.path.insert(0, '/Users/sanjeevkumar/Development/python/listFilter/python/')
import searchMethodUI
import filterList


class SearchMethod(object):
	"""docstring for SearchMethod"""
	def __init__(self, module, prefix, path=None):
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
		if path:			
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
				if flObj.filterList(valmeths):
					filteredDict[keymod] = flObj.filterList(valmeths)
		return filteredDict


class SearchMethodUI(QtGui.QWidget, searchMethodUI.Ui_searchMethodMainWidget):
	"""docstring for SearchMethodUI"""
	def __init__(self, parent=None):
		super(SearchMethodUI, self).__init__(parent)
		self.setupUi(self)
		self._connections()

	def main(self):
		self.show()

	def _connections(self):
		self.searchBtn.clicked.connect(self._populateResults)
		pass

	def _searchResults(self):
		lookinlst = str(self.lookInsideEdit.text()).split(",")
		searchMethObj = SearchMethod(lookinlst, str(self.lineEdit.text()))
		newLst = []
		for key, value in  searchMethObj.filterMethods().iteritems():
			newLst.append("%s: %s" % (key, ", ".join(value)))
		return newLst

	def _populateResults(self):
		founds = self._searchResults()
		lm = MyListModel(founds, self)
		self.searchListView.setModel(lm)


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


