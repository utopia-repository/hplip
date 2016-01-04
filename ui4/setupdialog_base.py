# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui4/setupdialog_base.ui'
#
# Created: Mon Dec 15 16:59:01 2008
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

        self.DiscoveryPage = QtGui.QWidget()
        self.DiscoveryPage.setObjectName("DiscoveryPage")

        self.gridlayout1 = QtGui.QGridLayout(self.DiscoveryPage)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label = QtGui.QLabel(self.DiscoveryPage)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,2)

        self.line = QtGui.QFrame(self.DiscoveryPage)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout1.addWidget(self.line,1,0,1,2)

        self.groupBox = QtGui.QGroupBox(self.DiscoveryPage)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout2 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout2.setObjectName("gridlayout2")

        self.UsbRadioButton = QtGui.QRadioButton(self.groupBox)
        self.UsbRadioButton.setChecked(True)
        self.UsbRadioButton.setObjectName("UsbRadioButton")
        self.gridlayout2.addWidget(self.UsbRadioButton,0,0,1,1)

        self.NetworkRadioButton = QtGui.QRadioButton(self.groupBox)
        self.NetworkRadioButton.setObjectName("NetworkRadioButton")
        self.gridlayout2.addWidget(self.NetworkRadioButton,1,0,1,1)

        self.ParallelRadioButton = QtGui.QRadioButton(self.groupBox)
        self.ParallelRadioButton.setEnabled(True)
        self.ParallelRadioButton.setObjectName("ParallelRadioButton")
        self.gridlayout2.addWidget(self.ParallelRadioButton,2,0,1,1)
        self.gridlayout1.addWidget(self.groupBox,2,0,1,2)

        self.AdvancedButton = QtGui.QPushButton(self.DiscoveryPage)
        self.AdvancedButton.setObjectName("AdvancedButton")
        self.gridlayout1.addWidget(self.AdvancedButton,3,0,1,1)

        spacerItem = QtGui.QSpacerItem(381,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,3,1,1,1)

        self.AdvancedStackedWidget = QtGui.QStackedWidget(self.DiscoveryPage)
        self.AdvancedStackedWidget.setObjectName("AdvancedStackedWidget")

        self.page = QtGui.QWidget()
        self.page.setObjectName("page")

        self.gridlayout3 = QtGui.QGridLayout(self.page)
        self.gridlayout3.setObjectName("gridlayout3")

        self.DiscoveryOptionsGroupBox = QtGui.QGroupBox(self.page)
        self.DiscoveryOptionsGroupBox.setObjectName("DiscoveryOptionsGroupBox")

        self.gridlayout4 = QtGui.QGridLayout(self.DiscoveryOptionsGroupBox)
        self.gridlayout4.setObjectName("gridlayout4")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.label_2 = QtGui.QLabel(self.DiscoveryOptionsGroupBox)
        self.label_2.setObjectName("label_2")
        self.hboxlayout.addWidget(self.label_2)

        self.SearchLineEdit = QtGui.QLineEdit(self.DiscoveryOptionsGroupBox)
        self.SearchLineEdit.setObjectName("SearchLineEdit")
        self.hboxlayout.addWidget(self.SearchLineEdit)
        self.gridlayout4.addLayout(self.hboxlayout,0,0,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.label_14 = QtGui.QLabel(self.DiscoveryOptionsGroupBox)
        self.label_14.setObjectName("label_14")
        self.hboxlayout1.addWidget(self.label_14)

        self.DeviceTypeComboBox = QtGui.QComboBox(self.DiscoveryOptionsGroupBox)
        self.DeviceTypeComboBox.setObjectName("DeviceTypeComboBox")
        self.hboxlayout1.addWidget(self.DeviceTypeComboBox)
        self.gridlayout4.addLayout(self.hboxlayout1,0,1,1,2)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.NetworkDiscoveryMethodLabel = QtGui.QLabel(self.DiscoveryOptionsGroupBox)
        self.NetworkDiscoveryMethodLabel.setObjectName("NetworkDiscoveryMethodLabel")
        self.hboxlayout2.addWidget(self.NetworkDiscoveryMethodLabel)

        self.NetworkDiscoveryMethodComboBox = QtGui.QComboBox(self.DiscoveryOptionsGroupBox)
        self.NetworkDiscoveryMethodComboBox.setObjectName("NetworkDiscoveryMethodComboBox")
        self.hboxlayout2.addWidget(self.NetworkDiscoveryMethodComboBox)
        self.gridlayout4.addLayout(self.hboxlayout2,1,0,1,1)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.NetworkTimeoutLabel = QtGui.QLabel(self.DiscoveryOptionsGroupBox)
        self.NetworkTimeoutLabel.setObjectName("NetworkTimeoutLabel")
        self.hboxlayout3.addWidget(self.NetworkTimeoutLabel)

        self.NetworkTimeoutSpinBox = QtGui.QSpinBox(self.DiscoveryOptionsGroupBox)
        self.NetworkTimeoutSpinBox.setMinimum(1)
        self.NetworkTimeoutSpinBox.setMaximum(90)
        self.NetworkTimeoutSpinBox.setProperty("value",QtCore.QVariant(5))
        self.NetworkTimeoutSpinBox.setObjectName("NetworkTimeoutSpinBox")
        self.hboxlayout3.addWidget(self.NetworkTimeoutSpinBox)
        self.gridlayout4.addLayout(self.hboxlayout3,1,1,1,1)

        self.hboxlayout4 = QtGui.QHBoxLayout()
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.NetworkTTLLabel = QtGui.QLabel(self.DiscoveryOptionsGroupBox)
        self.NetworkTTLLabel.setObjectName("NetworkTTLLabel")
        self.hboxlayout4.addWidget(self.NetworkTTLLabel)

        self.NetworkTTLSpinBox = QtGui.QSpinBox(self.DiscoveryOptionsGroupBox)
        self.NetworkTTLSpinBox.setMinimum(1)
        self.NetworkTTLSpinBox.setMaximum(8)
        self.NetworkTTLSpinBox.setProperty("value",QtCore.QVariant(4))
        self.NetworkTTLSpinBox.setObjectName("NetworkTTLSpinBox")
        self.hboxlayout4.addWidget(self.NetworkTTLSpinBox)
        self.gridlayout4.addLayout(self.hboxlayout4,1,2,1,1)
        self.gridlayout3.addWidget(self.DiscoveryOptionsGroupBox,0,0,1,1)

        self.ManualGroupBox = QtGui.QGroupBox(self.page)
        self.ManualGroupBox.setCheckable(True)
        self.ManualGroupBox.setObjectName("ManualGroupBox")

        self.gridlayout5 = QtGui.QGridLayout(self.ManualGroupBox)
        self.gridlayout5.setObjectName("gridlayout5")

        self.ManualParamLabel = QtGui.QLabel(self.ManualGroupBox)
        self.ManualParamLabel.setObjectName("ManualParamLabel")
        self.gridlayout5.addWidget(self.ManualParamLabel,0,0,1,1)

        self.ManualParamLineEdit = QtGui.QLineEdit(self.ManualGroupBox)
        self.ManualParamLineEdit.setObjectName("ManualParamLineEdit")
        self.gridlayout5.addWidget(self.ManualParamLineEdit,0,1,1,1)

        self.JetDirectLabel = QtGui.QLabel(self.ManualGroupBox)
        self.JetDirectLabel.setObjectName("JetDirectLabel")
        self.gridlayout5.addWidget(self.JetDirectLabel,0,2,1,1)

        self.JetDirectSpinBox = QtGui.QSpinBox(self.ManualGroupBox)
        self.JetDirectSpinBox.setMinimum(1)
        self.JetDirectSpinBox.setMaximum(3)
        self.JetDirectSpinBox.setObjectName("JetDirectSpinBox")
        self.gridlayout5.addWidget(self.JetDirectSpinBox,0,3,1,1)
        self.gridlayout3.addWidget(self.ManualGroupBox,1,0,1,1)
        self.AdvancedStackedWidget.addWidget(self.page)

        self.page_4 = QtGui.QWidget()
        self.page_4.setObjectName("page_4")
        self.AdvancedStackedWidget.addWidget(self.page_4)
        self.gridlayout1.addWidget(self.AdvancedStackedWidget,4,0,1,2)

        spacerItem1 = QtGui.QSpacerItem(478,20,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem1,5,0,1,2)
        self.StackedWidget.addWidget(self.DiscoveryPage)

        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")

        self.gridlayout6 = QtGui.QGridLayout(self.page_2)
        self.gridlayout6.setObjectName("gridlayout6")

        self.label_4 = QtGui.QLabel(self.page_2)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridlayout6.addWidget(self.label_4,0,0,1,2)

        self.line_2 = QtGui.QFrame(self.page_2)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridlayout6.addWidget(self.line_2,1,0,1,3)

        self.DevicesTableWidget = QtGui.QTableWidget(self.page_2)
        self.DevicesTableWidget.setAlternatingRowColors(True)
        self.DevicesTableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.DevicesTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.DevicesTableWidget.setSortingEnabled(False)
        self.DevicesTableWidget.setObjectName("DevicesTableWidget")
        self.gridlayout6.addWidget(self.DevicesTableWidget,2,0,1,3)

        self.hboxlayout5 = QtGui.QHBoxLayout()
        self.hboxlayout5.setObjectName("hboxlayout5")

        self.DevicesFoundIcon = QtGui.QLabel(self.page_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DevicesFoundIcon.sizePolicy().hasHeightForWidth())
        self.DevicesFoundIcon.setSizePolicy(sizePolicy)
        self.DevicesFoundIcon.setMinimumSize(QtCore.QSize(16,16))
        self.DevicesFoundIcon.setMaximumSize(QtCore.QSize(16,16))
        self.DevicesFoundIcon.setFrameShape(QtGui.QFrame.NoFrame)
        self.DevicesFoundIcon.setObjectName("DevicesFoundIcon")
        self.hboxlayout5.addWidget(self.DevicesFoundIcon)

        self.DevicesFoundLabel = QtGui.QLabel(self.page_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DevicesFoundLabel.sizePolicy().hasHeightForWidth())
        self.DevicesFoundLabel.setSizePolicy(sizePolicy)
        self.DevicesFoundLabel.setWordWrap(True)
        self.DevicesFoundLabel.setObjectName("DevicesFoundLabel")
        self.hboxlayout5.addWidget(self.DevicesFoundLabel)
        self.gridlayout6.addLayout(self.hboxlayout5,3,0,1,1)

        spacerItem2 = QtGui.QSpacerItem(21,28,QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Minimum)
        self.gridlayout6.addItem(spacerItem2,3,1,1,1)

        self.RefreshButton = QtGui.QPushButton(self.page_2)
        self.RefreshButton.setObjectName("RefreshButton")
        self.gridlayout6.addWidget(self.RefreshButton,3,2,1,1)
        self.StackedWidget.addWidget(self.page_2)

        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName("page_3")

        self.gridlayout7 = QtGui.QGridLayout(self.page_3)
        self.gridlayout7.setObjectName("gridlayout7")

        self.label_5 = QtGui.QLabel(self.page_3)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridlayout7.addWidget(self.label_5,0,0,1,1)

        self.line_3 = QtGui.QFrame(self.page_3)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridlayout7.addWidget(self.line_3,1,0,1,1)

        self.groupBox_3 = QtGui.QGroupBox(self.page_3)
        self.groupBox_3.setObjectName("groupBox_3")

        self.gridlayout8 = QtGui.QGridLayout(self.groupBox_3)
        self.gridlayout8.setObjectName("gridlayout8")

        self.label_6 = QtGui.QLabel(self.groupBox_3)
        self.label_6.setObjectName("label_6")
        self.gridlayout8.addWidget(self.label_6,0,0,1,1)

        self.PrinterNameLineEdit = QtGui.QLineEdit(self.groupBox_3)
        self.PrinterNameLineEdit.setObjectName("PrinterNameLineEdit")
        self.gridlayout8.addWidget(self.PrinterNameLineEdit,0,1,1,2)

        self.label_7 = QtGui.QLabel(self.groupBox_3)
        self.label_7.setObjectName("label_7")
        self.gridlayout8.addWidget(self.label_7,1,0,1,1)

        self.PrinterDescriptionLineEdit = QtGui.QLineEdit(self.groupBox_3)
        self.PrinterDescriptionLineEdit.setObjectName("PrinterDescriptionLineEdit")
        self.gridlayout8.addWidget(self.PrinterDescriptionLineEdit,1,1,1,2)

        self.label_8 = QtGui.QLabel(self.groupBox_3)
        self.label_8.setObjectName("label_8")
        self.gridlayout8.addWidget(self.label_8,2,0,1,1)

        self.PrinterLocationLineEdit = QtGui.QLineEdit(self.groupBox_3)
        self.PrinterLocationLineEdit.setObjectName("PrinterLocationLineEdit")
        self.gridlayout8.addWidget(self.PrinterLocationLineEdit,2,1,1,2)

        self.label_3 = QtGui.QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.gridlayout8.addWidget(self.label_3,3,0,1,1)

        self.PPDFileLineEdit = QtGui.QLineEdit(self.groupBox_3)
        self.PPDFileLineEdit.setReadOnly(True)
        self.PPDFileLineEdit.setObjectName("PPDFileLineEdit")
        self.gridlayout8.addWidget(self.PPDFileLineEdit,3,1,1,1)

        self.OtherPPDButton = QtGui.QToolButton(self.groupBox_3)
        self.OtherPPDButton.setObjectName("OtherPPDButton")
        self.gridlayout8.addWidget(self.OtherPPDButton,3,2,1,1)
        self.gridlayout7.addWidget(self.groupBox_3,2,0,1,1)

        self.SetupFaxGroupBox = QtGui.QGroupBox(self.page_3)
        self.SetupFaxGroupBox.setCheckable(True)
        self.SetupFaxGroupBox.setObjectName("SetupFaxGroupBox")

        self.gridlayout9 = QtGui.QGridLayout(self.SetupFaxGroupBox)
        self.gridlayout9.setObjectName("gridlayout9")

        self.label_9 = QtGui.QLabel(self.SetupFaxGroupBox)
        self.label_9.setObjectName("label_9")
        self.gridlayout9.addWidget(self.label_9,0,0,1,1)

        self.FaxNameLineEdit = QtGui.QLineEdit(self.SetupFaxGroupBox)
        self.FaxNameLineEdit.setObjectName("FaxNameLineEdit")
        self.gridlayout9.addWidget(self.FaxNameLineEdit,0,1,1,3)

        self.label_10 = QtGui.QLabel(self.SetupFaxGroupBox)
        self.label_10.setObjectName("label_10")
        self.gridlayout9.addWidget(self.label_10,1,0,1,1)

        self.FaxNumberLineEdit = QtGui.QLineEdit(self.SetupFaxGroupBox)
        self.FaxNumberLineEdit.setObjectName("FaxNumberLineEdit")
        self.gridlayout9.addWidget(self.FaxNumberLineEdit,1,1,1,1)

        self.label_11 = QtGui.QLabel(self.SetupFaxGroupBox)
        self.label_11.setObjectName("label_11")
        self.gridlayout9.addWidget(self.label_11,1,2,1,1)

        self.NameCompanyLineEdit = QtGui.QLineEdit(self.SetupFaxGroupBox)
        self.NameCompanyLineEdit.setObjectName("NameCompanyLineEdit")
        self.gridlayout9.addWidget(self.NameCompanyLineEdit,1,3,1,1)

        self.label_12 = QtGui.QLabel(self.SetupFaxGroupBox)
        self.label_12.setObjectName("label_12")
        self.gridlayout9.addWidget(self.label_12,2,0,1,1)

        self.FaxDescriptionLineEdit = QtGui.QLineEdit(self.SetupFaxGroupBox)
        self.FaxDescriptionLineEdit.setObjectName("FaxDescriptionLineEdit")
        self.gridlayout9.addWidget(self.FaxDescriptionLineEdit,2,1,1,3)

        self.label_13 = QtGui.QLabel(self.SetupFaxGroupBox)
        self.label_13.setObjectName("label_13")
        self.gridlayout9.addWidget(self.label_13,3,0,1,1)

        self.FaxLocationLineEdit = QtGui.QLineEdit(self.SetupFaxGroupBox)
        self.FaxLocationLineEdit.setObjectName("FaxLocationLineEdit")
        self.gridlayout9.addWidget(self.FaxLocationLineEdit,3,1,1,3)
        self.gridlayout7.addWidget(self.SetupFaxGroupBox,3,0,1,1)

        spacerItem3 = QtGui.QSpacerItem(341,16,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout7.addItem(spacerItem3,4,0,1,1)

        self.SendTestPageCheckBox = QtGui.QCheckBox(self.page_3)
        self.SendTestPageCheckBox.setObjectName("SendTestPageCheckBox")
        self.gridlayout7.addWidget(self.SendTestPageCheckBox,5,0,1,1)
        self.StackedWidget.addWidget(self.page_3)
        self.gridlayout.addWidget(self.StackedWidget,0,0,1,5)

        self.StepText = QtGui.QLabel(Dialog)
        self.StepText.setObjectName("StepText")
        self.gridlayout.addWidget(self.StepText,1,0,1,1)

        spacerItem4 = QtGui.QSpacerItem(181,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem4,1,1,1,1)

        self.BackButton = QtGui.QPushButton(Dialog)
        self.BackButton.setObjectName("BackButton")
        self.gridlayout.addWidget(self.BackButton,1,2,1,1)

        self.NextButton = QtGui.QPushButton(Dialog)
        self.NextButton.setObjectName("NextButton")
        self.gridlayout.addWidget(self.NextButton,1,3,1,1)

        self.CancelButton = QtGui.QPushButton(Dialog)
        self.CancelButton.setObjectName("CancelButton")
        self.gridlayout.addWidget(self.CancelButton,1,4,1,1)

        self.retranslateUi(Dialog)
        self.StackedWidget.setCurrentIndex(0)
        self.AdvancedStackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "HP Device Manager - Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Device Discovery", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Connection (I/O) Type", None, QtGui.QApplication.UnicodeUTF8))
        self.UsbRadioButton.setText(QtGui.QApplication.translate("Dialog", "Universal Serial Bus (USB)", None, QtGui.QApplication.UnicodeUTF8))
        self.NetworkRadioButton.setText(QtGui.QApplication.translate("Dialog", "Network/Ethernet/Wireless network (direct connection or JetDirect)", None, QtGui.QApplication.UnicodeUTF8))
        self.ParallelRadioButton.setText(QtGui.QApplication.translate("Dialog", "Parallel Port (LPT)", None, QtGui.QApplication.UnicodeUTF8))
        self.DiscoveryOptionsGroupBox.setTitle(QtGui.QApplication.translate("Dialog", "Discovery Options", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Search term:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("Dialog", "Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.NetworkDiscoveryMethodLabel.setText(QtGui.QApplication.translate("Dialog", "Network discovery method:", None, QtGui.QApplication.UnicodeUTF8))
        self.NetworkDiscoveryMethodComboBox.addItem(QtGui.QApplication.translate("Dialog", "SLP", None, QtGui.QApplication.UnicodeUTF8))
        self.NetworkDiscoveryMethodComboBox.addItem(QtGui.QApplication.translate("Dialog", "mDNS/Bonjour", None, QtGui.QApplication.UnicodeUTF8))
        self.NetworkTimeoutLabel.setText(QtGui.QApplication.translate("Dialog", "Timeout:", None, QtGui.QApplication.UnicodeUTF8))
        self.NetworkTimeoutSpinBox.setSuffix(QtGui.QApplication.translate("Dialog", "sec", None, QtGui.QApplication.UnicodeUTF8))
        self.NetworkTTLLabel.setText(QtGui.QApplication.translate("Dialog", "TTL:", None, QtGui.QApplication.UnicodeUTF8))
        self.ManualGroupBox.setTitle(QtGui.QApplication.translate("Dialog", "Manual Discovery", None, QtGui.QApplication.UnicodeUTF8))
        self.ManualParamLabel.setText(QtGui.QApplication.translate("Dialog", "Parameter:", None, QtGui.QApplication.UnicodeUTF8))
        self.JetDirectLabel.setText(QtGui.QApplication.translate("Dialog", "Jetdirect port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Select From Discovered Devices", None, QtGui.QApplication.UnicodeUTF8))
        self.DevicesTableWidget.clear()
        self.DevicesTableWidget.setColumnCount(0)
        self.DevicesTableWidget.setRowCount(0)
        self.DevicesFoundLabel.setText(QtGui.QApplication.translate("Dialog", "Found %1 devices on the %1 bus.", None, QtGui.QApplication.UnicodeUTF8))
        self.RefreshButton.setText(QtGui.QApplication.translate("Dialog", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Setup Device", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("Dialog", "Printer Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "Printer name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "Description:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "Location:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "PPD file:", None, QtGui.QApplication.UnicodeUTF8))
        self.SetupFaxGroupBox.setTitle(QtGui.QApplication.translate("Dialog", "Fax Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Dialog", "Fax name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("Dialog", "Fax number:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("Dialog", "Name/company:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("Dialog", "Description:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("Dialog", "Location:", None, QtGui.QApplication.UnicodeUTF8))
        self.SendTestPageCheckBox.setText(QtGui.QApplication.translate("Dialog", "Send test page to printer", None, QtGui.QApplication.UnicodeUTF8))
        self.StepText.setText(QtGui.QApplication.translate("Dialog", "Step %1 of %2", None, QtGui.QApplication.UnicodeUTF8))
        self.BackButton.setText(QtGui.QApplication.translate("Dialog", "< Back", None, QtGui.QApplication.UnicodeUTF8))
        self.NextButton.setText(QtGui.QApplication.translate("Dialog", "Next >", None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

