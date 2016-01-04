# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui4/printdialog_base.ui'
#
# Created: Tue Feb 17 11:36:14 2009
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,700,500).size()).expandedTo(Dialog.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(Dialog)
        self.gridlayout.setObjectName("gridlayout")

        self.StackedWidget = QtGui.QStackedWidget(Dialog)
        self.StackedWidget.setObjectName("StackedWidget")

        self.page = QtGui.QWidget()
        self.page.setObjectName("page")

        self.gridlayout1 = QtGui.QGridLayout(self.page)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label_2 = QtGui.QLabel(self.page)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,0,0,1,1)

        self.line = QtGui.QFrame(self.page)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout1.addWidget(self.line,1,0,1,1)

        self.Files = FileTable(self.page)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Files.sizePolicy().hasHeightForWidth())
        self.Files.setSizePolicy(sizePolicy)
        self.Files.setObjectName("Files")
        self.gridlayout1.addWidget(self.Files,2,0,1,1)
        self.StackedWidget.addWidget(self.page)

        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")

        self.gridlayout2 = QtGui.QGridLayout(self.page_2)
        self.gridlayout2.setObjectName("gridlayout2")

        self.label_3 = QtGui.QLabel(self.page_2)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridlayout2.addWidget(self.label_3,0,0,1,1)

        self.line_2 = QtGui.QFrame(self.page_2)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridlayout2.addWidget(self.line_2,1,0,1,1)

        self.PrinterName = PrinterNameComboBox(self.page_2)
        self.PrinterName.setObjectName("PrinterName")
        self.gridlayout2.addWidget(self.PrinterName,2,0,1,1)

        self.OptionsToolBox = PrintSettingsToolbox(self.page_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OptionsToolBox.sizePolicy().hasHeightForWidth())
        self.OptionsToolBox.setSizePolicy(sizePolicy)
        self.OptionsToolBox.setObjectName("OptionsToolBox")
        self.gridlayout2.addWidget(self.OptionsToolBox,3,0,1,1)
        self.StackedWidget.addWidget(self.page_2)
        self.gridlayout.addWidget(self.StackedWidget,0,0,1,5)

        self.line_3 = QtGui.QFrame(Dialog)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridlayout.addWidget(self.line_3,1,0,1,5)

        self.StepText = QtGui.QLabel(Dialog)
        self.StepText.setObjectName("StepText")
        self.gridlayout.addWidget(self.StepText,2,0,1,1)

        spacerItem = QtGui.QSpacerItem(251,28,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,2,1,1,1)

        self.BackButton = QtGui.QPushButton(Dialog)
        self.BackButton.setObjectName("BackButton")
        self.gridlayout.addWidget(self.BackButton,2,2,1,1)

        self.NextButton = QtGui.QPushButton(Dialog)
        self.NextButton.setObjectName("NextButton")
        self.gridlayout.addWidget(self.NextButton,2,3,1,1)

        self.CancelButton = QtGui.QPushButton(Dialog)
        self.CancelButton.setObjectName("CancelButton")
        self.gridlayout.addWidget(self.CancelButton,2,4,1,1)

        self.retranslateUi(Dialog)
        self.StackedWidget.setCurrentIndex(1)
        self.OptionsToolBox.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "HP Device Manager - Print", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Select Files to Print", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Select Printer and Options", None, QtGui.QApplication.UnicodeUTF8))
        self.StepText.setText(QtGui.QApplication.translate("Dialog", "Step %1 of %2", None, QtGui.QApplication.UnicodeUTF8))
        self.BackButton.setText(QtGui.QApplication.translate("Dialog", "< Back", None, QtGui.QApplication.UnicodeUTF8))
        self.NextButton.setText(QtGui.QApplication.translate("Dialog", "Next >", None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

from printsettingstoolbox import PrintSettingsToolbox
from printernamecombobox import PrinterNameComboBox
from filetable import FileTable
