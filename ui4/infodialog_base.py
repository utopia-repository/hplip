# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui4/infodialog_base.ui'
#
# Created: Thu Apr  9 13:51:53 2009
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,700,500).size()).expandedTo(Dialog.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(Dialog)
        self.gridlayout.setObjectName("gridlayout")

        self.label = QtGui.QLabel(Dialog)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout.addWidget(self.line,1,0,1,2)

        self.DeviceComboBox = DeviceUriComboBox(Dialog)
        self.DeviceComboBox.setObjectName("DeviceComboBox")
        self.gridlayout.addWidget(self.DeviceComboBox,2,0,1,2)

        self.TabWidget = QtGui.QTabWidget(Dialog)
        self.TabWidget.setObjectName("TabWidget")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout1 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout1.setObjectName("gridlayout1")

        self.StaticTableWidget = QtGui.QTableWidget(self.tab_2)
        self.StaticTableWidget.setAlternatingRowColors(True)
        self.StaticTableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.StaticTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.StaticTableWidget.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerItem)
        self.StaticTableWidget.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.StaticTableWidget.setGridStyle(QtCore.Qt.DotLine)
        self.StaticTableWidget.setObjectName("StaticTableWidget")
        self.gridlayout1.addWidget(self.StaticTableWidget,0,0,1,1)
        self.TabWidget.addTab(self.tab_2,"")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.gridlayout2 = QtGui.QGridLayout(self.tab)
        self.gridlayout2.setObjectName("gridlayout2")

        self.DynamicTableWidget = QtGui.QTableWidget(self.tab)
        self.DynamicTableWidget.setAlternatingRowColors(True)
        self.DynamicTableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.DynamicTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.DynamicTableWidget.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerItem)
        self.DynamicTableWidget.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.DynamicTableWidget.setGridStyle(QtCore.Qt.DotLine)
        self.DynamicTableWidget.setObjectName("DynamicTableWidget")
        self.gridlayout2.addWidget(self.DynamicTableWidget,0,0,1,1)
        self.TabWidget.addTab(self.tab,"")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.gridlayout3 = QtGui.QGridLayout(self.tab_3)
        self.gridlayout3.setObjectName("gridlayout3")

        self.HistoryTableWidget = QtGui.QTableWidget(self.tab_3)
        self.HistoryTableWidget.setAlternatingRowColors(True)
        self.HistoryTableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.HistoryTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.HistoryTableWidget.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.HistoryTableWidget.setGridStyle(QtCore.Qt.DotLine)
        self.HistoryTableWidget.setSortingEnabled(False)
        self.HistoryTableWidget.setObjectName("HistoryTableWidget")
        self.gridlayout3.addWidget(self.HistoryTableWidget,0,0,1,1)
        self.TabWidget.addTab(self.tab_3,"")
        self.gridlayout.addWidget(self.TabWidget,3,0,1,2)

        spacerItem = QtGui.QSpacerItem(470,31,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Maximum)
        self.gridlayout.addItem(spacerItem,4,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(361,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,5,0,1,1)

        self.CancelButton = QtGui.QPushButton(Dialog)
        self.CancelButton.setObjectName("CancelButton")
        self.gridlayout.addWidget(self.CancelButton,5,1,1,1)

        self.retranslateUi(Dialog)
        self.TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "HP Device Manager - Device Information", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Device Information", None, QtGui.QApplication.UnicodeUTF8))
        self.StaticTableWidget.clear()
        self.StaticTableWidget.setColumnCount(0)
        self.StaticTableWidget.setRowCount(0)
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Dialog", "Model Data (Static)", None, QtGui.QApplication.UnicodeUTF8))
        self.DynamicTableWidget.clear()
        self.DynamicTableWidget.setColumnCount(0)
        self.DynamicTableWidget.setRowCount(0)
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.tab), QtGui.QApplication.translate("Dialog", "Status Data (Dynamic)", None, QtGui.QApplication.UnicodeUTF8))
        self.HistoryTableWidget.clear()
        self.HistoryTableWidget.setColumnCount(0)
        self.HistoryTableWidget.setRowCount(0)
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("Dialog", "Status History", None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

from deviceuricombobox import DeviceUriComboBox
