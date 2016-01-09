# -*- coding: utf-8 -*-
#
# (c) Copyright 2003-2007 Hewlett-Packard Development Company, L.P.
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

# StdLib

# Local
from base.g import *
from ui_utils import *

# Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Main window
from fabwindow_base import Ui_MainWindow

fax_avail = True
try:
    from fax import fax
except ImportError:
    # This can fail on Python < 2.3 due to the datetime module
    log.error("Fax address book disabled - Python 2.3+ required.")
    #sys.exit(1)
    fax_avail = False



class FABWindow(QMainWindow,  Ui_MainWindow):
    def __init__(self, parent):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.group = u'All' # current group
        self.name = None # current name
        self.updating_group = False
        self.updating_name = False
        
        self.initDB()
        self.initUi()
        
        QTimer.singleShot(0, self.updateUi)
    
    
    def initDB(self):
        self.db =  fax.FaxAddressBook()
        
        # Fixup data from old-style database
        data = self.db.get_all_records()
        for d in data:
            if u'All' not in data[d]['groups']:
                data[d]['groups'].append(u'All')
    
        if not data:
            self.db.set('__' + utils.gen_random_uuid(), '', '', '', '', [u'All'], '')
            
    
    def initUi(self):
        # Application icon
        self.setWindowIcon(QIcon(load_pixmap('prog', '48x48')))
        #self.setWindowTitle(self.__tr("HP Device Manager - Fax Address Book"))
        
        self.NewGroupAction.setIcon(QIcon(load_pixmap('new_group', '24x24')))
        self.NewGroupFromSelectionAction.setIcon(QIcon(load_pixmap('new_group_from_selection', '24x24')))
        self.RenameGroupAction.setIcon(QIcon(load_pixmap('rename_group', '24x24')))
        self.RemoveGroupAction.setIcon(QIcon(load_pixmap('remove_group', '24x24')))
        self.NewNameAction.setIcon(QIcon(load_pixmap('new_user', '24x24')))
        self.RemoveNameAction.setIcon(QIcon(load_pixmap('remove_user', '24x24')))
        self.AddToGroupAction.setIcon(QIcon(load_pixmap('add_to_group', '24x24')))
        self.RemoveFromGroupAction.setIcon(QIcon(load_pixmap('remove_from_group', '24x24')))
        
        self.connect(self.QuitAction, SIGNAL("triggered()"), self.close)
        self.connect(self.NewGroupAction, SIGNAL("triggered()"), self.NewGroupAction_triggered)
        self.connect(self.NewGroupFromSelectionAction, SIGNAL("triggered()"), self.NewGroupFromSelectionAction_triggered)
        self.connect(self.RenameGroupAction, SIGNAL("triggered()"), self.RenameGroupAction_triggered)
        self.connect(self.RemoveGroupAction, SIGNAL("triggered()"), self.RemoveGroupAction_triggered)
        self.connect(self.NewNameAction, SIGNAL("triggered()"), self.NewNameAction_triggered)
        self.connect(self.RemoveNameAction, SIGNAL("triggered()"), self.RemoveNameAction_triggered)
        
        self.connect(self.RemoveFromGroupAction, SIGNAL("triggered()"), self.RemoveFromGroupAction_triggered)
        self.connect(self.AddToGroupAction, SIGNAL("triggered()"), self.AddToGroupAction_triggered)
        
        self.GroupTableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.NameTableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.connect(self.Splitter, SIGNAL("splitterMoved(int, int)"), self.Splitter_splitterMoved)
        self.Splitter.setChildrenCollapsible(False)
        self.Splitter.setHandleWidth(self.Splitter.handleWidth()+2)
        
        self.GroupTableWidget.verticalHeader().hide()
        self.GroupTableWidget.setShowGrid(False)
        self.GroupTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.NameTableWidget.verticalHeader().hide()
        self.NameTableWidget.setShowGrid(False)
        
        self.NameTableWidget.setDragEnabled(True)
        self.GroupTableWidget.setAcceptDrops(True)
        self.GroupTableWidget.setDropIndicatorShown(True)
        
        self.connect(self.GroupTableWidget, SIGNAL("itemSelectionChanged()"), self.GroupTableWidget_itemSelectionChanged)
        self.connect(self.NameTableWidget, SIGNAL("itemSelectionChanged()"), self.NameTableWidget_itemSelectionChanged)
        self.connect(self.NameLineEdit, SIGNAL("editingFinished()"), self.NameLineEdit_editingFinished)
        self.connect(self.FaxNumberLineEdit, SIGNAL("editingFinished()"), self.FaxNumberLineEdit_editingFinished)
        self.connect(self.NotesTextEdit, SIGNAL("textChanged()"), self.NotesTextEdit_textChanged)
        self.connect(self.GroupTableWidget, SIGNAL("namesAddedToGroup"), self.GroupTableWidget_namesAddedToGroup)
        
        self.GroupTableWidget.setDatabase(self.db)
        
        
    def updateUi(self):
        if not fax_avail:
            FailureUI(self, self.__tr("<b>Fax support disabled.</b><p>Fax support requires Python 2.3."))
            self.close()
            return 
                      
        self.updateGroupList()
        self.updateNameList()
        self.updateDetailsFrame()
        
        
    def Splitter_splitterMoved(self, pos, index):
        self.GroupTableWidget.setColumnWidth(0, self.GroupTableWidget.width())
        self.NameTableWidget.setColumnWidth(0, self.NameTableWidget.width())
        
        
    def updateGroupList(self):
        #print "update group list", repr(self.group)
        self.updating_group = True
        all, k = None, None
        try:
            headerItem = QTableWidgetItem()
            headerItem.setText(self.__tr("Group"))
            self.GroupTableWidget.clear()
            self.GroupTableWidget.setColumnCount(1)
            self.GroupTableWidget.setHorizontalHeaderItem(0, headerItem)
            self.GroupTableWidget.setColumnWidth(0, self.GroupTableWidget.width())
            
            groups = self.db.get_all_groups()
            groups.sort()
            self.GroupTableWidget.setRowCount(len(groups))
            
            # Force All group to top of table
            all = QTableWidgetItem(self.__tr("All"))
            all.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.GroupTableWidget.setItem(0, 0, all)
            
            j = 1
            for g in groups:
                #print g, self.group
                if g == u'All':
                    continue

                i = QTableWidgetItem(QString(g))

                if g == self.group:
                    #print "found", g
                    k = i
                
                i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDropEnabled)
                self.GroupTableWidget.setItem(j, 0, i)
                j += 1
                
        
        finally:
            self.updating_group = False
            
            if k is not None:
                k.setSelected(True)
            
            elif all is not None:
                all.setSelected(True)

        
        
    def GroupTableWidget_itemSelectionChanged(self):
        #print "GroupTableWidget_itemSelectionChanged:", self.updating_group
        if not self.updating_group:
            selected_items = self.GroupTableWidget.selectedItems()
            if selected_items:
                self.group = unicode(selected_items[0].text())
                self.RemoveGroupAction.setEnabled(self.group != u'All')
                self.RenameGroupAction.setEnabled(self.group != u'All')
            else: # shouldn't happen?!
                self.RemoveGroupAction.setEnabled(False)
                self.RenameGroupAction.setEnabled(False)
                self.group = None
                
            self.updateNameList()
        
        
    def NameTableWidget_itemSelectionChanged(self):
        #print "NameTableWidget_itemSelectionChanged:", self.updating_name
        if not self.updating_name:
            selected_items = self.NameTableWidget.selectedItems()
            num_selected_items = len(selected_items)
            
            if num_selected_items == 0:
                self.name = None
                self.RemoveNameAction.setEnabled(False)
                self.NewGroupFromSelectionAction.setEnabled(False)
                self.RemoveFromGroupAction.setEnabled(False)
                self.AddToGroupAction.setEnabled(False)
                
            elif num_selected_items == 1:
                self.name = unicode(selected_items[0].text())
                self.RemoveNameAction.setEnabled(True)
                self.NewGroupFromSelectionAction.setEnabled(True)
                
                self.RemoveFromGroupAction.setEnabled(self.group != u'All')
                self.AddToGroupAction.setEnabled(True) #self.group != u'All')
            
            else: # > 1
                self.RemoveNameAction.setEnabled(True)
                self.NewGroupFromSelectionAction.setEnabled(True)
                self.RemoveFromGroupAction.setEnabled(self.group != u'All')
                self.AddToGroupAction.setEnabled(True) #self.group != u'All')
                self.name = None
            
            self.updateDetailsFrame()
        
        
    def updateNameList(self):
        #print "update name list:", repr(self.name)
        self.updating_name = True
        m, k = None, None
        try:
            headerItem = QTableWidgetItem()
            headerItem.setText(self.__tr("Name"))
            self.NameTableWidget.clear()
            self.NameTableWidget.setColumnCount(1)
            self.NameTableWidget.setHorizontalHeaderItem(0,headerItem)
            self.NameTableWidget.setColumnWidth(0, self.NameTableWidget.width())
            
            names = self.db.group_members(self.group)
            filtered_names = [n for n in names if not n.startswith('__')]
            filtered_names.sort()
            self.NameTableWidget.setRowCount(len(filtered_names))
            
            for j, n in enumerate(filtered_names):
                i = QTableWidgetItem(QString(n))
                i.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)
                self.NameTableWidget.setItem(j, 0, i)
                
                if n == self.name:
                    m = i
                
                if j == 0:
                    k = i            
        
        finally:
            self.updating_name = False
        
            if m is not None:
                m.setSelected(True)
            
            elif k is not None:
                k.setSelected(True)
                
            else: # no names, disable name frame and name actions
                self.name = None
                self.RemoveNameAction.setEnabled(False)
                self.NewGroupFromSelectionAction.setEnabled(False)
                self.RemoveFromGroupAction.setEnabled(False)
                self.AddToGroupAction.setEnabled(False)
                self.updateDetailsFrame()


    def updateDetailsFrame(self):
        #print "update details frame", repr(self.name)
        if self.name is None:
            self.NameFrame.setEnabled(False)
            self.NameLineEdit.setText(QString())
            self.FaxNumberLineEdit.setText(QString())
            self.NotesTextEdit.setText(QString())
            
        else:
            self.NameFrame.setEnabled(True)
            data = self.db.get(self.name)
            self.NameLineEdit.setText(self.name)
            self.FaxNumberLineEdit.setText(data['fax'])
            self.NotesTextEdit.setText(data['notes'])
            
            
    def NameLineEdit_editingFinished(self):
        if self.name is not None:
            new_name = unicode(self.NameLineEdit.text())
            if new_name != self.name:
                if QMessageBox.question(self, self.__tr("Rename?"), self.__tr("Rename '%1' to '%2'?").arg(self.name).arg(new_name), \
                                        QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                    
                    self.db.rename(self.name, new_name)
                    self.updateNameList()
                else:
                    self.NameLineEdit.setText(self.name)
        
        
    def FaxNumberLineEdit_editingFinished(self):
        if self.name is not None:
            self.db.set_key_value(self.name, 'fax', unicode(self.FaxNumberLineEdit.text()))
        
        
    def NotesTextEdit_textChanged(self):
        if self.name is not None:
            self.db.set_key_value(self.name, 'notes', unicode(self.NotesTextEdit.document().toPlainText()))


    def NewGroupAction_triggered(self):
        ok = False
        g, ok = QInputDialog.getText(self, self.__tr("Enter New Group Name"), self.__tr("Name for New Group:"))
        g = unicode(g)
        
        if g == u'All':
            FailureUI(self, self.__tr("<b>Sorry, the group name cannot be 'All'.</b><p>Please choose a different name."))
            ok = False
        
        if ok:
            self.db.set('__' + utils.gen_random_uuid(), '', '', '', '', [u'All', g], '')
            self.group = g
            
            self.updateGroupList()
        
        
    def NewGroupFromSelectionAction_triggered(self):
        selected_names = [unicode(n.text()) for n in self.NameTableWidget.selectedItems()]
        if selected_names:
            ok = False
            g, ok = QInputDialog.getText(self, self.__tr("Enter New Group Name"), self.__tr("Name for New Group:"))
            g = unicode(g)

            groups = self.db.get_all_groups()
            
            if g in groups:
                FailureUI(self, self.__tr("<b>Sorry, the group name cannot be the same as an existing group (or 'All').</b><p>Please choose a different name."))
                ok = False
                
            
            if ok:
                self.db.update_groups(g, selected_names)
                self.group = g
                self.updateGroupList()
        
        
        
        
    def RenameGroupAction_triggered(self):
        selected_items = self.GroupTableWidget.selectedItems()
        if selected_items:
            old_group = unicode(selected_items[0].text())
            ok = False
            new_group, ok = QInputDialog.getText(self, self.__tr("Rename Group"), self.__tr("New Name for Group '%1':").arg(old_group))
            new_group = unicode(new_group)
            groups = self.db.get_all_groups()
            
            if new_group in groups:
                FailureUI(self, self.__tr("<b>Sorry, the group name cannot be the same as an existing group (or 'All').</b><p>Please choose a different name."))
                ok = False

            if ok:
                self.db.rename_group(old_group, new_group)
                self.group = new_group
                self.updateGroupList()
            
        
        
    def RemoveGroupAction_triggered(self):
        self.db.delete_group(self.group)
        self.group = None
        self.updateGroupList()
        
        
    def NewNameAction_triggered(self):
        ok = False
        t, ok = QInputDialog.getText(self, self.__tr("Enter New Name"), self.__tr("New Name:"))
        if ok:
            t = unicode(t)
            # All names are members of 'All' group
            if self.group == u'All':
                g = [u'All']
            else:
                g = [u'All', self.group]
                
            self.db.set(t, '', '', '', '', g, '')
            self.name = t
            self.updateNameList()
            
        
    def RemoveNameAction_triggered(self):
        selected_names = [unicode(n.text()) for n in self.NameTableWidget.selectedItems()]
        if selected_names:
            for n in selected_names:
                self.db.delete(n)
                
            self.name = None
            self.updateNameList()
    
    
    def RemoveFromGroupAction_triggered(self):
        selected_names = [unicode(n.text()) for n in self.NameTableWidget.selectedItems()]
        if selected_names:
            self.db.remove_from_group(self.group, selected_names)
            self.name = None
            self.updateGroupList()
        

    def GroupTableWidget_namesAddedToGroup(self, row, items): # drag n' drop handler
        self.group = unicode(self.GroupTableWidget.item(row, 0).text())
        self.db.add_to_group(self.group, items)
        self.updateGroupList()
        
        
    def AddToGroupAction_triggered(self):
        selected_names = [unicode(n.text()) for n in self.NameTableWidget.selectedItems()]
        if selected_names:
            ok = False
            all_groups = self.db.get_all_groups()
            #print "all groups:", all_groups
            
            if all_groups:
                all_groups = [g for g in all_groups if g != u'All']
                all_groups.sort()
                
                dlg = JoinDialog(self, all_groups)
                
                if dlg.exec_() == QDialog.Accepted:
                    group = dlg.group
                    if group:
                        self.db.add_to_group(group, selected_names)
                        self.group = group
                        self.updateGroupList()
            
            else:
                FailureUI(self, self.__tr("<b>There are no groups to join.</b><p>Use <i>New Group from Selection</i> to create a new group using these name(s)."))
                
    
    
    def __tr(self,s,c = None):
        return qApp.translate("FABWindow",s,c)

    
    
    
class JoinDialog(QDialog):
    def __init__(self, parent, groups):
        QDialog.__init__(self, parent)
        self.group = ''
        self.setupUi(groups)


    def setupUi(self, groups):
        self.setObjectName("Dialog")
        self.resize(QSize(QRect(0,0,271,107).size()).expandedTo(self.minimumSizeHint()))

        self.gridlayout = QGridLayout(self)
        self.gridlayout.setObjectName("gridlayout")

        self.hboxlayout = QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.label = QLabel(self)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)

        self.GroupJoinComboBox = QComboBox(self)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GroupJoinComboBox.sizePolicy().hasHeightForWidth())
        self.GroupJoinComboBox.setSizePolicy(sizePolicy)
        self.GroupJoinComboBox.setObjectName("comboBox")
        self.hboxlayout.addWidget(self.GroupJoinComboBox)
        self.gridlayout.addLayout(self.hboxlayout,0,0,1,3)

        spacerItem = QSpacerItem(20,40,QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem,1,0,1,1)

        spacerItem1 = QSpacerItem(231,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,2,0,1,1)

        self.JoinButton = QPushButton(self)
        self.JoinButton.setObjectName("pushButton_2")
        self.gridlayout.addWidget(self.JoinButton,2,1,1,1)

        self.CancelButton = QPushButton(self)
        self.CancelButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.CancelButton,2,2,1,1)

        self.connect(self.GroupJoinComboBox, SIGNAL("currentIndexChanged(int)"), 
            self.GroupJoinComboBox_currentIndexChanged)

        for i, g in enumerate(groups):
            if i == 0: 
                self.group = g
            self.GroupJoinComboBox.insertItem(i, g)
            
        self.connect(self.JoinButton, SIGNAL("clicked()"), self.accept)
        self.connect(self.CancelButton, SIGNAL("clicked()"), self.reject)
        
            
        self.retranslateUi()
        #QMetaObject.connectSlotsByName(Dialog)
        
        
    def GroupJoinComboBox_currentIndexChanged(self, i):
        self.group = unicode(self.GroupJoinComboBox.currentText())
        

    def retranslateUi(self):
        self.setWindowTitle(QApplication.translate("Dialog", "Join Group", None, QApplication.UnicodeUTF8))
        self.label.setText(QApplication.translate("Dialog", "Group to Join:", None, QApplication.UnicodeUTF8))
        self.JoinButton.setText(QApplication.translate("Dialog", "Join", None, QApplication.UnicodeUTF8))
        self.CancelButton.setText(QApplication.translate("Dialog", "Cancel", None, QApplication.UnicodeUTF8))
