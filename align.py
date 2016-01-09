#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) Copyright 2003-2008 Hewlett-Packard Development Company, L.P.
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

__version__ = '5.0'
__title__ = 'Printer Cartridge Alignment Utility'
__mod__ = 'hp-align'
__doc__ = "Cartridge alignment utility for HPLIP supported inkjet printers. (Note: Not all printers require the use of this utility)."

# Std Lib
import sys
import re
import getopt
import operator
import os

# Local
from base.g import *
from base import device, status, utils, maint, tui, module
from prnt import cups


def enterAlignmentNumber(letter, hortvert, colors, line_count, maximum):
    ok, value = tui.enter_range("Enter the best aligned value for line %s (1-%d): " % 
                        (letter, maximum),
                        1,
                        maximum)
    if not ok:
        sys.exit(0)

    return ok, value


def enterPaperEdge(maximum):
    ok, value = tui.enter_range("Enter numbered arrow that is best aligned with the paper edge (1-%d): " 
                        % maximum,
                        1,
                        maximum)
    if not ok:
        sys.exit(0)

    return ok, value


def colorAdj(line, maximum):
    ok, value = tui.enter_range("Enter the numbered box on line %s that is best color matched to the background color (1-%d): " % 
                        (line, maximum),
                        1,
                        maximum)
    if not ok:
        sys.exit(0)

    return ok, value


def bothPensRequired():
    log.error("Cannot perform alignment with 0 or 1 cartridges installed.\nPlease install both cartridges and try again.")


def invalidPen():
    log.error("Invalid cartridge(s) installed.\nPlease install valid cartridges and try again.")


def invalidPen2():
    log.error("Invalid cartridge(s) installed. Cannot align with only the photo cartridge installed.\nPlease install other cartridges and try again.")


def aioUI1():
    log.info("To perform alignment, you will need the alignment page that is automatically\nprinted after you install a print cartridge.")
    log.info("\np\t\tPrint the alignment page and continue.")
    log.info("n\t\tDo Not print the alignment page (you already have one) and continue.")
    log.info("q\t\tQuit.\n")

    ok, choice = tui.enter_choice("Choice (p=print page*, n=do not print page, q=quit) ? ", ['p', 'n', 'q'], 'p')

    if choice == 'q':
        sys.exit(0)

    return choice == 'y'


def type10and11Align(pattern, align_type):
    controls = maint.align10and11Controls(pattern, align_type)
    values = []
    s_controls = controls.keys()
    s_controls.sort()

    for line in s_controls:
        if not controls[line][0]:
            values.append(0)
        else:
            ok, value = tui.enter_range("Enter the numbered box on line %s where the inner lines best line up with the outer lines (1-%d): " 
                % (line, controls[line][1]),  1, controls[line][1])
            values.append(value)

            if not ok:
                sys.exit(0)

    return values


def aioUI2():
    log.info("")
    log.info(log.bold("Follow these steps to complete the alignment:"))
    log.info("1. Place the alignment page, with the printed side facing down, ")
    log.info("   in the scanner.")
    log.info("2. Press the Enter or Scan button on the printer.")
    log.info('3. "Alignment Complete" will be displayed when the process is finished (on some models).')




try:    
    mod = module.Module(__mod__, __title__, __version__, __doc__, None, 
                        (INTERACTIVE_MODE, GUI_MODE), (UI_TOOLKIT_QT4,))
                        
    mod.setUsage(module.USAGE_FLAG_DEVICE_ARGS,
                 see_also_list=['hp-clean', 'hp-colorcal', 'hp-linefeedcal',
                                'hp-pqdiag'])

    opts, device_uri, printer_name, mode, ui_toolkit, lang = \
        mod.parseStdOpts()

    device_uri = mod.getDeviceUri(device_uri, printer_name, 
        filter={'align-type': (operator.gt, 0)})
        
    if mode == GUI_MODE:
        if not utils.canEnterGUIMode4():
            log.error("%s -u/--gui requires Qt4 GUI support. Entering interactive mode." % __mod__)
            mode = INTERACTIVE_MODE        

    if mode == INTERACTIVE_MODE:
        try:
            d = device.Device(device_uri, printer_name)
        except Error, e:
            log.error("Unable to open device: %s" % e.msg)
            sys.exit(0)

        try:
            try:
                d.open()
            except Error:
                log.error("Device is busy or in an error state. Please check device and try again.")
                sys.exit(1)

            if d.isIdleAndNoError():
                align_type = d.mq.get('align-type', 0)
                log.debug("Alignment type=%d" % align_type)
                d.close()

                if align_type == ALIGN_TYPE_NONE:
                    log.error("Alignment not supported or required by device.")
                    sys.exit(0)

                if align_type == ALIGN_TYPE_AUTO:
                    maint.AlignType1PML(d, tui.load_paper_prompt)

                elif align_type == ALIGN_TYPE_AIO:
                    maint.AlignType13(d, tui.load_paper_prompt, tui.load_scanner_for_align_prompt)

                elif align_type == ALIGN_TYPE_8XX:
                    maint.AlignType2(d, tui.load_paper_prompt, enterAlignmentNumber,
                                      bothPensRequired)

                elif align_type in (ALIGN_TYPE_9XX,ALIGN_TYPE_9XX_NO_EDGE_ALIGN):
                    maint.AlignType3(d, tui.load_paper_prompt, enterAlignmentNumber,
                                      enterPaperEdge, update_spinner)

                elif align_type == ALIGN_TYPE_LIDIL_AIO:
                    maint.AlignType6(d, aioUI1, aioUI2, tui.load_paper_prompt)

                elif align_type == ALIGN_TYPE_DESKJET_450:
                    maint.AlignType8(d, tui.load_paper_prompt, enterAlignmentNumber)

                elif align_type in (ALIGN_TYPE_LIDIL_0_3_8, ALIGN_TYPE_LIDIL_0_4_3, ALIGN_TYPE_LIDIL_VIP):

                    maint.AlignxBow(d, align_type, tui.load_paper_prompt, enterAlignmentNumber, enterPaperEdge,
                                     invalidPen, colorAdj)

                elif align_type  == ALIGN_TYPE_LBOW:
                    maint.AlignType10(d, tui.load_paper_prompt, type10and11Align)

                elif align_type == ALIGN_TYPE_LIDIL_0_5_4:
                    maint.AlignType11(d, tui.load_paper_prompt, type10and11Align, invalidPen2)

                elif align_type == ALIGN_TYPE_OJ_PRO:
                    maint.AlignType12(d, tui.load_paper_prompt)

                else:
                    log.error("Invalid alignment type.")

            else:
                log.error("Device is busy or in an error state. Please check device and try again.")

        finally:
            d.close()

    else: # GUI_MODE (qt4)
        try:
            from PyQt4.QtGui import QApplication
            from ui4.aligndialog import AlignDialog
        except ImportError:
            log.error("Unable to load Qt4 support. Is it installed?")
            sys.exit(1)        
            

        #try:
        if 1:
            app = QApplication(sys.argv)

            dlg = AlignDialog(None, device_uri)
            dlg.show()
            try:
                log.debug("Starting GUI loop...")
                app.exec_()
            except KeyboardInterrupt:
                sys.exit(0)

        #finally:
        if 1:
            sys.exit(0)

except KeyboardInterrupt:
    log.error("User exit")


log.info("")
log.info('Done.')
