# -*- coding: utf-8 -*-
#
# (c) Copyright 2001-2009 Hewlett-Packard Development Company, L.P.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# Author: Don Welch
#

# Local
from base.g import *
from base.codes import *
from ui_utils import *

# Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class SystrayFrame(QFrame):
    def __init__(self, parent):
        QFrame.__init__(self, parent)


    def initUi(self, systray_visible, polling, polling_interval, device_list, systray_messages):
        self.systray_visible = systray_visible
        self.polling = polling
        self.polling_interval = polling_interval
        self.device_list = device_list
        self.systray_messages = systray_messages

        self.gridlayout = QGridLayout(self)

        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.gridlayout1 = QGridLayout(self.frame)

        self.groupBox_2 = QGroupBox(self.frame)

        self.gridlayout2 = QGridLayout(self.groupBox_2)

        self.ShowAlwaysRadioButton = QRadioButton(self.groupBox_2)
        self.gridlayout2.addWidget(self.ShowAlwaysRadioButton,0,0,1,1)

        self.HideWhenInactiveRadioButton = QRadioButton(self.groupBox_2)
        self.gridlayout2.addWidget(self.HideWhenInactiveRadioButton,1,0,1,1)

        self.HideAlwaysRadioButton = QRadioButton(self.groupBox_2)
        self.gridlayout2.addWidget(self.HideAlwaysRadioButton,2,0,1,1)

        self.gridlayout1.addWidget(self.groupBox_2,0,0,1,1)

        self.groupBox_3 = QGroupBox(self.frame)

        self.gridlayout3 = QGridLayout(self.groupBox_3)

        self.label_2 = QLabel(self.groupBox_3)
        self.gridlayout3.addWidget(self.label_2,0,0,1,1)

        self.MessageShowComboBox = QComboBox(self.groupBox_3)
        self.gridlayout3.addWidget(self.MessageShowComboBox,1,0,1,1)

        self.MessageShowComboBox.addItem(self.__tr("All"), QVariant(SYSTRAY_MESSAGES_SHOW_ALL))
        self.MessageShowComboBox.addItem(self.__tr("Errors and Warnings"), QVariant(SYSTRAY_MESSAGES_SHOW_ERRORS_AND_WARNINGS))
        self.MessageShowComboBox.addItem(self.__tr("Errors Only"), QVariant(SYSTRAY_MESSAGES_SHOW_ERRORS_ONLY))
        self.MessageShowComboBox.addItem(self.__tr("None"), QVariant(SYSTRAY_MESSAGES_SHOW_NONE))

        spacerItem = QSpacerItem(20,40,QSizePolicy.Minimum,QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem,2,0,1,1)
        self.gridlayout1.addWidget(self.groupBox_3,0,1,1,1)

        self.MonitorGroupBox = QGroupBox(self.frame)
        self.MonitorGroupBox.setCheckable(True)

        self.MonitorGroupBox.setEnabled(False)

        self.gridlayout4 = QGridLayout(self.MonitorGroupBox)

        self.label = QLabel(self.MonitorGroupBox)
        self.gridlayout4.addWidget(self.label,0,0,1,1)

        self.listWidget = QListWidget(self.MonitorGroupBox)
        self.gridlayout4.addWidget(self.listWidget,1,0,1,1)
        self.gridlayout1.addWidget(self.MonitorGroupBox,1,0,1,2)
        self.gridlayout.addWidget(self.frame,0,0,1,1)

        self.setWindowTitle(QApplication.translate("self", "self", None, QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QApplication.translate("self", "System tray icon visibility", None, QApplication.UnicodeUTF8))
        self.ShowAlwaysRadioButton.setText(QApplication.translate("self", "Always show", None, QApplication.UnicodeUTF8))
        self.HideWhenInactiveRadioButton.setText(QApplication.translate("self", "Hide when inactive", None, QApplication.UnicodeUTF8))
        self.HideAlwaysRadioButton.setText(QApplication.translate("self", "Always hide", None, QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QApplication.translate("self", "System tray icon messages", None, QApplication.UnicodeUTF8))
        self.label_2.setText(QApplication.translate("self", "Messages to show:", None, QApplication.UnicodeUTF8))
        self.MonitorGroupBox.setTitle(QApplication.translate("self", "Monitor button presses on devices", None, QApplication.UnicodeUTF8))
        self.label.setText(QApplication.translate("self", "Devices to monitor:", None, QApplication.UnicodeUTF8))

        self.connect(self.ShowAlwaysRadioButton, SIGNAL("clicked(bool)"), self.ShowAlwaysRadioButton_clicked)
        self.connect(self.HideWhenInactiveRadioButton, SIGNAL("clicked(bool)"), self.HideWhenInactiveRadioButton_clicked)
        self.connect(self.HideAlwaysRadioButton, SIGNAL("clicked(bool)"), self.HideAlwaysRadioButton_clicked)
        self.connect(self.MessageShowComboBox, SIGNAL("activated(int)"), self.MessageShowComboBox_activated)


    def updateUi(self):
        self.updateVisibility()
        self.updateMessages()
        self.updateDeviceList()


    def updateVisibility(self):
        if self.systray_visible == SYSTRAY_VISIBLE_SHOW_ALWAYS:
            self.ShowAlwaysRadioButton.setChecked(True)

        elif self.systray_visible == SYSTRAY_VISIBLE_HIDE_WHEN_INACTIVE:
            self.HideWhenInactiveRadioButton.setChecked(True)

        else: # SYSTRAY_VISIBLE_HIDE_ALWAYS
            self.HideAlwaysRadioButton.setChecked(True)


    def ShowAlwaysRadioButton_clicked(self, b):
        if b: self.systray_visible = SYSTRAY_VISIBLE_SHOW_ALWAYS


    def HideWhenInactiveRadioButton_clicked(self, b):
        if b: self.systray_visible = SYSTRAY_VISIBLE_HIDE_WHEN_INACTIVE


    def HideAlwaysRadioButton_clicked(self, b):
        if b: self.systray_visible = SYSTRAY_VISIBLE_HIDE_ALWAYS


    def updateMessages(self):
        i = self.MessageShowComboBox.findData(QVariant(self.systray_messages))
        if i != -1:
            self.MessageShowComboBox.setCurrentIndex(i)


    def MessageShowComboBox_activated(self, i):
        sender = self.sender()
        mode, ok = sender.itemData(i).toInt()
        if ok:
            self.systray_messages = mode


    def updateDeviceList(self):
        pass


    def __tr(self, s, c=None):
        return QApplication.translate("SystrayFrame", s, c, QApplication.UnicodeUTF8)

