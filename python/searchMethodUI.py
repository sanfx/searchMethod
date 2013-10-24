# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/searchMethod.ui'
#
# Created: Wed Oct 23 20:34:23 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_searchMethodMainWidget(object):
    def setupUi(self, searchMethodMainWidget):
        searchMethodMainWidget.setObjectName("searchMethodMainWidget")
        searchMethodMainWidget.resize(553, 414)
        self.gridLayout_2 = QtGui.QGridLayout(searchMethodMainWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.searchBtn = QtGui.QPushButton(searchMethodMainWidget)
        self.searchBtn.setObjectName("searchBtn")
        self.gridLayout.addWidget(self.searchBtn, 0, 2, 1, 1)
        self.addPathlbl = QtGui.QLabel(searchMethodMainWidget)
        self.addPathlbl.setObjectName("addPathlbl")
        self.gridLayout.addWidget(self.addPathlbl, 2, 0, 1, 1)
        self.lookInsideLbl = QtGui.QLabel(searchMethodMainWidget)
        self.lookInsideLbl.setObjectName("lookInsideLbl")
        self.gridLayout.addWidget(self.lookInsideLbl, 0, 0, 1, 1)
        self.browseBtn = QtGui.QPushButton(searchMethodMainWidget)
        self.browseBtn.setObjectName("browseBtn")
        self.gridLayout.addWidget(self.browseBtn, 2, 2, 1, 1)
        self.addPathEdit = QtGui.QLineEdit(searchMethodMainWidget)
        self.addPathEdit.setObjectName("addPathEdit")
        self.gridLayout.addWidget(self.addPathEdit, 2, 1, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lookInsideEdit = QtGui.QLineEdit(searchMethodMainWidget)
        self.lookInsideEdit.setObjectName("lookInsideEdit")
        self.horizontalLayout_3.addWidget(self.lookInsideEdit)
        self.label = QtGui.QLabel(searchMethodMainWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(searchMethodMainWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.searchListView = QtGui.QListView(searchMethodMainWidget)
        self.searchListView.setObjectName("searchListView")
        self.verticalLayout.addWidget(self.searchListView)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.methodListView = QtGui.QListView(searchMethodMainWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.methodListView.sizePolicy().hasHeightForWidth())
        self.methodListView.setSizePolicy(sizePolicy)
        self.methodListView.setObjectName("methodListView")
        self.horizontalLayout_2.addWidget(self.methodListView)
        self.helpOnSelMethodTxtEdit = QtGui.QTextEdit(searchMethodMainWidget)
        self.helpOnSelMethodTxtEdit.setFrameShape(QtGui.QFrame.StyledPanel)
        self.helpOnSelMethodTxtEdit.setFrameShadow(QtGui.QFrame.Raised)
        self.helpOnSelMethodTxtEdit.setObjectName("helpOnSelMethodTxtEdit")
        self.horizontalLayout_2.addWidget(self.helpOnSelMethodTxtEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(searchMethodMainWidget)
        QtCore.QMetaObject.connectSlotsByName(searchMethodMainWidget)

    def retranslateUi(self, searchMethodMainWidget):
        searchMethodMainWidget.setWindowTitle(QtGui.QApplication.translate("searchMethodMainWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.searchBtn.setText(QtGui.QApplication.translate("searchMethodMainWidget", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.addPathlbl.setText(QtGui.QApplication.translate("searchMethodMainWidget", "Add Path", None, QtGui.QApplication.UnicodeUTF8))
        self.lookInsideLbl.setText(QtGui.QApplication.translate("searchMethodMainWidget", "Look Inside", None, QtGui.QApplication.UnicodeUTF8))
        self.browseBtn.setText(QtGui.QApplication.translate("searchMethodMainWidget", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("searchMethodMainWidget", "Prefix", None, QtGui.QApplication.UnicodeUTF8))

