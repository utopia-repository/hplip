# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/homes/dwelch/lnx/Projects/hplups/ui/form1.ui'
#
# Created: Mon Nov 3 14:44:17 2003
#      by: The PyQt User Interface Compiler (pyuic) 3.6
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class Form1(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("Form1")


        Form1Layout = QGridLayout(self,1,1,11,6,"Form1Layout")

        self.pushButton1 = QPushButton(self,"pushButton1")

        Form1Layout.addWidget(self.pushButton1,0,0)

        self.languageChange()

        self.resize(QSize(124,53).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton1,SIGNAL("clicked()"),self,SLOT("close()"))


    def languageChange(self):
        self.setCaption(self.tr("hpguid"))
        self.pushButton1.setText(self.tr("Close"))


if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = Form1()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
