# -*- coding: utf-8 -*-
#
# (c) Copyright 2002-2008 Hewlett-Packard Development Company, L.P.
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
# Authors: Doug Deprenger, Don Welch
#

# Std Lib
import sys, thread, syslog, traceback, string, os

identity = string.maketrans('','')
unprintable = identity.translate(identity, string.printable)

def printable(s):
    return s.translate(identity, unprintable)

DEFAULT_LOG_LEVEL = 'info'

class Logger(object):
    LOG_LEVEL_NONE = 99
    LOG_LEVEL_FATAL = 40
    LOG_LEVEL_ERROR = 30
    LOG_LEVEL_WARN = 20
    LOG_LEVEL_INFO = 10
    LOG_LEVEL_DEBUG3 = 3
    LOG_LEVEL_DBG3 = 3
    LOG_LEVEL_DEBUG2 = 2
    LOG_LEVEL_DBG2 = 2
    LOG_LEVEL_DEBUG = 1
    LOG_LEVEL_DBG = 1

    logging_levels = {'none' : LOG_LEVEL_NONE,
                       'fata' : LOG_LEVEL_FATAL,
                       'fatal' : LOG_LEVEL_FATAL,
                       'erro' : LOG_LEVEL_ERROR,
                       'error' : LOG_LEVEL_ERROR,
                       'warn' : LOG_LEVEL_WARN,
                       'info' : LOG_LEVEL_INFO,
                       'debug' : LOG_LEVEL_DEBUG,
                       'dbg'  : LOG_LEVEL_DEBUG,
                       'debug2' : LOG_LEVEL_DEBUG2,
                       'dbg2' : LOG_LEVEL_DEBUG2,
                       'debug3' : LOG_LEVEL_DEBUG3,
                       'dbg3' : LOG_LEVEL_DEBUG3,
                       }

    LOG_TO_DEV_NULL = 0
    LOG_TO_CONSOLE = 1
    LOG_TO_SCREEN = 1
    LOG_TO_FILE = 2
    LOG_TO_CONSOLE_AND_FILE = 3
    LOG_TO_BOTH = 3

    # Copied from Gentoo Portage output.py
    # Copyright 1998-2003 Daniel Robbins, Gentoo Technologies, Inc.
    # Distributed under the GNU Public License v2
    codes={}
    codes["reset"]="\x1b[0m"
    codes["bold"]="\x1b[01m"

    codes["teal"]="\x1b[36;06m"
    codes["turquoise"]="\x1b[36;01m"

    codes["fuscia"]="\x1b[35;01m"
    codes["purple"]="\x1b[35;06m"

    codes["blue"]="\x1b[34;01m"
    codes["darkblue"]="\x1b[34;06m"

    codes["green"]="\x1b[32;01m"
    codes["darkgreen"]="\x1b[32;06m"

    codes["yellow"]="\x1b[33;01m"
    codes["brown"]="\x1b[33;06m"

    codes["red"]="\x1b[31;01m"
    codes["darkred"]="\x1b[31;06m"


    def __init__(self, module='', level=LOG_LEVEL_INFO, where=LOG_TO_CONSOLE_AND_FILE,
                 log_datetime=False, log_file=None):
        self.set_level(level)
        self._where = where
        self._log_file = log_file
        self._log_file_f = None
        self._log_datetime = log_datetime
        self._lock = thread.allocate_lock()
        self.module = module
        self.pid = os.getpid()
        self.fmt = True

    def set_level(self, level):
        if isinstance(level,str):
            level = level.lower()
            if level in Logger.logging_levels.keys():
                self._level = Logger.logging_levels.get(level, Logger.LOG_LEVEL_INFO)
                return True
            else:
                self.error("Invalid logging level: %s" % level)
                return False

        elif isinstance(level,int):
            if Logger.LOG_LEVEL_DEBUG3 <= level <= Logger.LOG_LEVEL_FATAL:
                self._level = level
            else:
                self.error("Invalid logging level: %d" % level)
                return False

        else:
            return False

    def set_module(self, module):
        self.module = module
        self.pid = os.getpid()
        
    def no_formatting(self):
        self.fmt = False

    def set_logfile(self, log_file):
        self._log_file = log_file
        try:
            self._log_file_f = file(self._log_file, 'w')
        except IOError:
            self._log_file = None
            self._log_file_f = None
            self._where = Logger.LOG_TO_SCREEN
            
    def get_logfile(self):
        return self._log_file

    def set_where(self, where):
        self._where = where

    def get_level(self):
        return self._level

    def is_debug(self):
        return self._level <= Logger.LOG_LEVEL_DEBUG3

    level = property(get_level, set_level)

    def log(self, message, level):
        if self._where in (Logger.LOG_TO_CONSOLE, Logger.LOG_TO_CONSOLE_AND_FILE):
            try:
                self._lock.acquire()
                if level >= Logger.LOG_LEVEL_WARN:
                    out = sys.stderr
                else:
                    out = sys.stdout
                try:
                    out.write(message)
                except UnicodeEncodeError:
                    out.write(message.encode("utf-8"))

                out.write('\n')
            finally:
                self._lock.release()

    def log_to_file(self, message):
        if self._log_file_f is not None:
            try:
                self._lock.acquire()
                self._log_file_f.write(message.replace('\x1b', ''))
                self._log_file_f.write('\n')

            finally:
                self._lock.release()

    def stderr(self, message):
        try:
            self._lock.acquire()
            sys.stderr.write("%s: %s\n" % (self.module, message))
        finally:
            self._lock.release()

    def debug(self, message): 
        if self._level <= Logger.LOG_LEVEL_DEBUG:
            txt = "%s[%d]: debug: %s" % (self.module, self.pid, message)
            self.log(self.color(txt, 'blue'), Logger.LOG_LEVEL_DEBUG)

            if self._log_file is not None and \
                self._where in (Logger.LOG_TO_FILE, Logger.LOG_TO_CONSOLE_AND_FILE):
                self.log_to_file(txt)

    dbg = debug

    def debug2(self, message): 
        if self._level <= Logger.LOG_LEVEL_DEBUG2:
            txt = "%s[%d]: debug2: %s" % (self.module, self.pid, message)
            self.log(self.color(txt, 'blue'), Logger.LOG_LEVEL_DEBUG2)

            if self._log_file is not None and \
                self._where in (Logger.LOG_TO_FILE, Logger.LOG_TO_CONSOLE_AND_FILE):
                self.log_to_file(txt)
    dbg2 = debug2

    def debug3(self, message): 
        if self._level <= Logger.LOG_LEVEL_DEBUG3:
            txt = "%s[%d]: debug3: %s" % (self.module, self.pid, message)
            self.log(self.color(txt, 'blue'), Logger.LOG_LEVEL_DEBUG3)

            if self._log_file is not None and \
                self._where in (Logger.LOG_TO_FILE, Logger.LOG_TO_CONSOLE_AND_FILE):
                self.log_to_file(txt)
    dbg3 = debug3


    def debug_block(self, title, block):
        if self._level <= Logger.LOG_LEVEL_DEBUG:
            line = "%s[%d]: debug: %s:" % (self.module,  self.pid, title)
            self.log(self.color(line, 'blue'), Logger.LOG_LEVEL_DEBUG)
            self.log(self.color(block, 'blue'), Logger.LOG_LEVEL_DEBUG)

            if self._log_file is not None and \
                self._where in (Logger.LOG_TO_FILE, Logger.LOG_TO_CONSOLE_AND_FILE):

                self.log_to_file(line % (self.module, self.pid, title))
                self.log_to_file(block)


    printable = """ !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~  """

    def log_data(self, data, width=16): 
        if self._level <= Logger.LOG_LEVEL_DEBUG:
            if data:
                index, line = 0, data[0:width]
                while line:
                    txt = ' '.join(['%04x: ' % index, ' '.join(['%02x' % ord(d) for d in line]), 
                        ' '*(width*3-3*len(line)), ''.join([('.', i)[i in Logger.printable] for i in line])])
    
                    self.log(self.color("%s[%d]: debug: %s" % (self.module,  self.pid, txt), 'blue'), 
                        Logger.LOG_LEVEL_DEBUG)
    
                    index += width
                    line = data[index:index+width]
            else:
                self.log(self.color("%s[%d]: debug: %s" % (self.module,  self.pid, "0000: (no data)"), 'blue'), 
                        Logger.LOG_LEVEL_DEBUG)

    def info(self, message=''):
        if self._level <= Logger.LOG_LEVEL_INFO:
            self.log(message, Logger.LOG_LEVEL_INFO)

            if self._log_file is not None and \
                self._where in (Logger.LOG_TO_FILE, Logger.LOG_TO_CONSOLE_AND_FILE):
                self.log_to_file("%s[%d]: info: :%s" % (self.module, self.pid, message))

    information = info

    def warn(self, message):
        if self._level <= Logger.LOG_LEVEL_WARN:
            txt = "warning: %s" % message.encode('utf-8')
            self.log(self.color(txt, 'fuscia'), Logger.LOG_LEVEL_WARN)

            syslog.syslog(syslog.LOG_WARNING, "%s[%d]: %s" % (self.module, self.pid, txt))

            if self._log_file is not None and \
                self._where in (Logger.LOG_TO_FILE, Logger.LOG_TO_CONSOLE_AND_FILE):
                self.log_to_file(txt)

    warning = warn

    def note(self, message):
        if self._level <= Logger.LOG_LEVEL_WARN:
            txt = "note: %s" % message
            self.log(self.color(txt, 'green'), Logger.LOG_LEVEL_WARN)

            if self._log_file is not None and \
                self._where in (Logger.LOG_TO_FILE, Logger.LOG_TO_CONSOLE_AND_FILE):
                self.log_to_file(txt)

    notice = note

    def error(self, message):
        if self._level <= Logger.LOG_LEVEL_ERROR:
            txt = "error: %s" % message.encode("utf-8")
            self.log(self.color(txt, 'red'), Logger.LOG_LEVEL_ERROR)

            syslog.syslog(syslog.LOG_ALERT, "%s[%d]: %s" % (self.module, self.pid, txt))

            if self._log_file is not None and \
                self._where in (Logger.LOG_TO_FILE, Logger.LOG_TO_CONSOLE_AND_FILE):
                self.log_to_file(txt)


    def fatal(self, message):
        if self._level <= Logger.LOG_LEVEL_FATAL:
            txt = "fatal error: :%s" % self.module.encode('utf-8')
            self.log(self.color(txt, 'red'), Logger.LOG_LEVEL_DEBUG)

            syslog.syslog(syslog.LOG_ALERT, "%s[%d]: %s" % (self.module, self.pid, txt))

            if self._log_file is not None and \
                self._where in (Logger.LOG_TO_FILE, Logger.LOG_TO_CONSOLE_AND_FILE):
                self.log_to_file(txt)


    def exception(self):
        typ, value, tb = sys.exc_info()
        body = "Traceback (innermost last):\n"
        lst = traceback.format_tb(tb) + traceback.format_exception_only(typ, value)
        body = body + "%-20s %s" % (''.join(lst[:-1]), lst[-1],)
        self.fatal(body)

    def color(self, text, color):
        if self.fmt:
            return ''.join([Logger.codes.get(color, 'bold'), text, Logger.codes['reset']])   
        return text

    def bold(self, text):
        return self.color(text, 'bold')

    def red(self, text):
        return self.color(text, 'red')
        
    def green(self, text):
        return self.color(text, 'green')
        
    def purple(self, text):
        return self.color(text, 'purple')
    
    def yellow(self, text):
        return self.color(text, 'yellow')
   
    def darkgreen(self, text):
        return self.color(text, 'darkgreen') 
      
    def blue(self, text):
        return self.color(text, 'blue')
    
