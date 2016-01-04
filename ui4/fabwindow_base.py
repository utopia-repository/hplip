# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui4/fabwindow_base.ui'
#
# Created: Mon Dec 15 16:58:59 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,700,440).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setObjectName("gridlayout")

        self.Splitter = QtGui.QSplitter(self.centralwidget)
        self.Splitter.setOrientation(QtCore.Qt.Horizontal)
        self.Splitter.setObjectName("Splitter")

        self.GroupTableWidget = FABGroupTable(self.Splitter)
        self.GroupTableWidget.setAlternatingRowColors(True)
        self.GroupTableWidget.setObjectName("GroupTableWidget")

        self.NameTableWidget = FABNameTable(self.Splitter)
        self.NameTableWidget.setAlternatingRowColors(True)
        self.NameTableWidget.setObjectName("NameTableWidget")

        self.NameFrame = QtGui.QFrame(self.Splitter)
        self.NameFrame.setEnabled(False)
        self.NameFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.NameFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.NameFrame.setObjectName("NameFrame")

        self.gridlayout1 = QtGui.QGridLayout(self.NameFrame)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label = QtGui.QLabel(self.NameFrame)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,1)

        self.NameLineEdit = QtGui.QLineEdit(self.NameFrame)
        self.NameLineEdit.setObjectName("NameLineEdit")
        self.gridlayout1.addWidget(self.NameLineEdit,0,1,1,1)

        self.label_2 = QtGui.QLabel(self.NameFrame)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,1,0,1,1)

        self.FaxNumberLineEdit = QtGui.QLineEdit(self.NameFrame)
        self.FaxNumberLineEdit.setObjectName("FaxNumberLineEdit")
        self.gridlayout1.addWidget(self.FaxNumberLineEdit,1,1,1,1)

        self.label_3 = QtGui.QLabel(self.NameFrame)
        self.label_3.setObjectName("label_3")
        self.gridlayout1.addWidget(self.label_3,2,0,1,1)

        self.NotesTextEdit = QtGui.QTextEdit(self.NameFrame)
        self.NotesTextEdit.setObjectName("NotesTextEdit")
        self.gridlayout1.addWidget(self.NotesTextEdit,3,0,1,2)
        self.gridlayout.addWidget(self.Splitter,0,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,700,27))
        self.menubar.setObjectName("menubar")

        self.menuGroup = QtGui.QMenu(self.menubar)
        self.menuGroup.setObjectName("menuGroup")

        self.menuName = QtGui.QMenu(self.menubar)
        self.menuName.setObjectName("menuName")

        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea,self.toolBar)

        self.NewGroupAction = QtGui.QAction(MainWindow)
        self.NewGroupAction.setObjectName("NewGroupAction")

        self.NewNameAction = QtGui.QAction(MainWindow)
        self.NewNameAction.setObjectName("NewNameAction")

        self.RemoveGroupAction = QtGui.QAction(MainWindow)
        self.RemoveGroupAction.setEnabled(False)
        self.RemoveGroupAction.setObjectName("RemoveGroupAction")

        self.QuitAction = QtGui.QAction(MainWindow)
        self.QuitAction.setObjectName("QuitAction")

        self.RemoveNameAction = QtGui.QAction(MainWindow)
        self.RemoveNameAction.setEnabled(False)
        self.RemoveNameAction.setObjectName("RemoveNameAction")

        self.NewGroupFromSelectionAction = QtGui.QAction(MainWindow)
        self.NewGroupFromSelectionAction.setEnabled(False)
        self.NewGroupFromSelectionAction.setObjectName("NewGroupFromSelectionAction")

        self.ImportAction = QtGui.QAction(MainWindow)
        self.ImportAction.setObjectName("ImportAction")

        self.RenameGroupAction = QtGui.QAction(MainWindow)
        self.RenameGroupAction.setEnabled(False)
        self.RenameGroupAction.setObjectName("RenameGroupAction")

        self.RemoveFromGroupAction = QtGui.QAction(MainWindow)
        self.RemoveFromGroupAction.setEnabled(False)
        self.RemoveFromGroupAction.setObjectName("RemoveFromGroupAction")

        self.AddToGroupAction = QtGui.QAction(MainWindow)
        self.AddToGroupAction.setEnabled(False)
        self.AddToGroupAction.setObjectName("AddToGroupAction")
        self.menuGroup.addAction(self.NewGroupAction)
        self.menuGroup.addAction(self.NewGroupFromSelectionAction)
        self.menuGroup.addAction(self.RenameGroupAction)
        self.menuGroup.addSeparator()
        self.menuGroup.addAction(self.RemoveGroupAction)
        self.menuName.addAction(self.NewNameAction)
        self.menuName.addSeparator()
        self.menuName.addAction(self.AddToGroupAction)
        self.menuName.addAction(self.RemoveFromGroupAction)
        self.menuName.addSeparator()
        self.menuName.addAction(self.RemoveNameAction)
        self.menuFile.addAction(self.ImportAction)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.QuitAction)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuGroup.menuAction())
        self.menubar.addAction(self.menuName.menuAction())
        self.toolBar.addAction(self.NewGroupAction)
        self.toolBar.addAction(self.NewGroupFromSelectionAction)
        self.toolBar.addAction(self.RenameGroupAction)
        self.toolBar.addAction(self.RemoveGroupAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.NewNameAction)
        self.toolBar.addAction(self.AddToGroupAction)
        self.toolBar.addAction(self.RemoveFromGroupAction)
        self.toolBar.addAction(self.RemoveNameAction)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "HP Device Manager - Fax Address Book", None, QtGui.QApplication.UnicodeUTF8))
        self.GroupTableWidget.clear()
        self.GroupTableWidget.setColumnCount(1)
        self.GroupTableWidget.setRowCount(0)

        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText(QtGui.QApplication.translate("MainWindow", "Group", None, QtGui.QApplication.UnicodeUTF8))
        self.GroupTableWidget.setHorizontalHeaderItem(0,headerItem)
        self.NameTableWidget.clear()
        self.NameTableWidget.setColumnCount(1)
        self.NameTableWidget.setRowCount(0)

        headerItem1 = QtGui.QTableWidgetItem()
        headerItem1.setText(QtGui.QApplication.translate("MainWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.NameTableWidget.setHorizontalHeaderItem(0,headerItem1)
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Fax Number:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Notes:", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGroup.setTitle(QtGui.QApplication.translate("MainWindow", "Group", None, QtGui.QApplication.UnicodeUTF8))
        self.menuName.setTitle(QtGui.QApplication.translate("MainWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.NewGroupAction.setText(QtGui.QApplication.translate("MainWindow", "New Group...", None, QtGui.QApplication.UnicodeUTF8))
        self.NewNameAction.setText(QtGui.QApplication.translate("MainWindow", "New Name...", None, QtGui.QApplication.UnicodeUTF8))
        self.RemoveGroupAction.setText(QtGui.QApplication.translate("MainWindow", "Delete Group...", None, QtGui.QApplication.UnicodeUTF8))
        self.QuitAction.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.RemoveNameAction.setText(QtGui.QApplication.translate("MainWindow", "Delete Name...", None, QtGui.QApplication.UnicodeUTF8))
        self.NewGroupFromSelectionAction.setText(QtGui.QApplication.translate("MainWindow", "New Group From Selection...", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportAction.setText(QtGui.QApplication.translate("MainWindow", "Import...", None, QtGui.QApplication.UnicodeUTF8))
        self.RenameGroupAction.setText(QtGui.QApplication.translate("MainWindow", "Rename Group...", None, QtGui.QApplication.UnicodeUTF8))
        self.RemoveFromGroupAction.setText(QtGui.QApplication.translate("MainWindow", "Leave Group", None, QtGui.QApplication.UnicodeUTF8))
        self.AddToGroupAction.setText(QtGui.QApplication.translate("MainWindow", "Join Group...", None, QtGui.QApplication.UnicodeUTF8))

from fabgrouptable import FABGroupTable
from fabnametable import FABNameTable
