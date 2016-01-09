#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) Copyright 2003-2014 Hewlett-Packard Development Company, L.P.
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
# Author: Don Welch, Amarnath Chitumalla
#

__version__ = '15.1'
__title__ = 'Dependency/Version Check Utility'
__mod__ = 'hp-check'
__doc__ = """Checks dependency versions,permissions of HPLIP. (Run as 'python ./check.py' from the HPLIP tarball before installation.)"""

# Std Lib
import sys
import os
import getopt
import re
import StringIO

# Local
from base.g import *
from base import utils, tui, queues, smart_install
from installer.core_install import *
from prnt import cups
device_avail = False
try:
    from base import device, pml
    # This can fail due to hpmudext not being present
except ImportError:
    log.debug("Device library is not avail.")
else:
    device_avail = True


################ Global variables ############
USAGE = [(__doc__, "", "name", True),
         ("Usage: %s [OPTIONS]" % __mod__, "", "summary", True),
         utils.USAGE_OPTIONS,
         ("Compile-time check:", "-c or --compile", "option", False),
         ("Run-time check:", "-r or --run or --runtime", "option", False),
         ("Compile and run-time checks:", "-b or --both (default)", "option", False),
         utils.USAGE_LOGGING1, utils.USAGE_LOGGING2, utils.USAGE_LOGGING3,
         utils.USAGE_LOGGING_PLAIN,
         utils.USAGE_HELP,
         
         utils.USAGE_NOTES,
         ("1. For checking for the proper build environment for the HPLIP supplied tarball (.tar.gz or .run),", "", "note", False),
         ("use the --compile or --both switches.", "", "note", False),
         ("2. For checking for the proper runtime environment for a distro supplied package (.deb, .rpm, etc),", "", "note", False),
         ("use the --runtime switch.", "", "note", False),
        ]
        
Ver_Func_Pat = re.compile('''FUNC#(.*)''')

EXTERNALDEP = 1
GENERALDEP = 2
COMPILEDEP = 3
PYEXT = 4 
SCANCONF = 5
IS_LIBUSB01_ENABLED = 'no'

############ Functions #########
# Usage function
def usage(typ='text'):
    if typ == 'text':
        utils.log_title(__title__, __version__)

    utils.format_text(USAGE, typ, __title__, __mod__, __version__)
    sys.exit(0)


# Displays the the hp-check usage information.
def show_title():
        utils.log_title(__title__, __version__)

        log.info(log.bold("Note: hp-check can be run in three modes:"))

        for l in tui.format_paragraph("1. Compile-time check mode (-c or --compile): Use this mode before compiling the HPLIP supplied tarball (.tar.gz or .run) to determine if the proper dependencies are installed to successfully compile HPLIP."):
            log.info(l)

        for l in tui.format_paragraph("2. Run-time check mode (-r or --run): Use this mode to determine if a distro supplied package (.deb, .rpm, etc) or an already built HPLIP supplied tarball has the proper dependencies installed to successfully run."):
            log.info(l)

        for l in tui.format_paragraph("3. Both compile- and run-time check mode (-b or --both) (Default): This mode will check both of the above cases (both compile- and run-time dependencies)."):
            log.info(l)

        log.info()
        for l in tui.format_paragraph("Check types:"):
            log.info(l)
        for l in tui.format_paragraph("a. EXTERNALDEP - External Dependencies"):
            log.info(l)
        for l in tui.format_paragraph("b. GENERALDEP  - General Dependencies (required both at compile and run time)"):
            log.info(l)
        for l in tui.format_paragraph("c. COMPILEDEP  - Compile time Dependencies"):
            log.info(l)
        for l in tui.format_paragraph("d. [All are run-time checks]"):
            log.info(l)
        for l in tui.format_paragraph("PYEXT\nSCANCONF\nQUEUES\nPERMISSION"):
            log.info(l)

        log.info()
        log.info("Status Types:")
        log.info("    OK")
        log.info("    MISSING       - Missing Dependency or Permission or Plug-in")
        log.info("    INCOMPAT      - Incompatible dependency-version or Plugin-version")
        log.info()

# Status_Type function. --> Returns the package installed status indformation
def Status_Type(Installedsts, min_ver,Installed_ver):
    if Installedsts is True or Installedsts !=  0:
        if min_ver == '-' or check_version(Installed_ver,min_ver):
            return "OK"
        else:
            return "INCOMPAT"
    else:
        return "MISSING"

    
# get_comment function --> Returns the 'comments' corresponding to the function.
def get_comment(package, Inst_status, installed_ver):
    comment = "-"
    if package == 'pyqt' or package == 'pyqt4':
        if Inst_status == 'OK':
            if not check_version(installed_ver, '2.3') and check_version(installed_ver, '2.2'):
                comment = "Fax is not supported if version is lessthan 2.3"
            elif not check_version(installed_ver, '2.2'):
                comment = "Python Programming is not supported if version is lessthan 2.2" 
    elif package == 'hpaio':
        if Inst_status == 'OK':
            comment = "'hpaio found in /etc/sane.d/dll.conf'"
        else:
            comment = "'hpaio not found in /etc/sane.d/dll.conf. hpaio needs to be added in this file.'"
    elif package == 'cupsext' or package == 'pcardext' or package == 'hpmudext':
        if Inst_status != 'OK':
            comment = "'Not Found or Failed to load, Please reinstall HPLIP'"
    elif package =='cups':
        if Inst_status != 'OK':
            comment = "'CUPS may not be installed or not running'"
        else:
            comment = "'CUPS Scheduler is running'"
    elif package == 'libusb' and IS_LIBUSB01_ENABLED == "yes":
        if Inst_status != 'OK':
            comment = "'libusb-1.0 needs to be installed'"
    elif package == 'dbus':
        if Inst_status != 'OK':
            comment = "'DBUS may not be installed or not running'"
        else:
            comment = "-"
    else:
        if Inst_status != 'OK':
            comment = "'%s needs to be installed'"%package
    return comment

def get_libusb_version():
    if IS_LIBUSB01_ENABLED == "yes":
        return get_version('libusb-config --version')
    else:
        return '1.0'



########## Classes ###########
#DependenciesCheck class derived from CoreInstall
class DependenciesCheck(CoreInstall):
    def __init__(self,mode=MODE_CHECK, ui_mode=INTERACTIVE_MODE, ui_toolkit='qt4'):
        CoreInstall.__init__(self,mode,ui_mode,ui_toolkit)
        self.num_errors = 0
        self.num_warns = 0
        
        self.missing_user_grps = ''
        self.disable_selinux = False
        self.req_deps_to_be_installed = []
        self.opt_deps_to_be_installed =[]
        self.cmds_to_be_run = []
        self.comm_error_devices = {}
        self.plugin_status = ''
        self.smart_install_devices = []
        
        self.user_grps_cmd = ''

        self.hplip_dependencies ={ EXTERNALDEP:
             {
#            <packageName>: (<Is Req/Opt Pack>, <Module>, <Package description>, <Installed check>, <min vrsion>, <cmd for installed version>),
            'dbus':             (True,  ['fax'], "DBus", self.check_dbus,'-','dbus-daemon --version'),
            'cups' :            (True,  ['base'], 'CUPS', self.check_cups,'1.1','cups-config --version'),
            'gs':               (True,  ['base'], "Ghostscript", self.check_gs,'7.05','gs --version'),
            'policykit':        (False, ['gui_qt4'], "Admin-Policy-framework", self.check_policykit,'-','pkexec --version'), # optional for non-sudo behavior of plugins (only optional for Qt4 option)
            'xsane':            (False, ['scan'], "SANE-GUI", self.check_xsane,'0.9','FUNC#get_xsane_version'),
            'scanimage':        (False, ['scan'], "Shell-Scanning", self.check_scanimage,'1.0','scanimage --version'),
            'network':        (False, ['network'], "Network-wget", self.check_wget,'-','wget --version'),
            },
            GENERALDEP:
            {'libpthread':       (True,  ['base'], "POSIX-Threads-Lib", self.check_libpthread,'-','FUNC#get_libpthread_version'),
            'libusb':           (True,  ['base'], "USB-Lib", self.check_libusb,'-','FUNC#get_libusb_version'),
            'libcrypto':        (True,  ['network'], "OpenSSL-Crypto-Lib", self.check_libcrypto,'-','openssl version'),
            'libjpeg':          (True,  ['base'], "JPEG-Lib", self.check_libjpeg,'-',None),
            'libnetsnmp-devel': (True,  ['network'], "SNMP-Networking-SDK", self.check_libnetsnmp,'5.0.9','net-snmp-config --version'),
            'cups-image':       (True,  ['base'], "CUPS-Image-Lib", self.check_cups_image,'-','cups-config --version'),
            'cups-devel':       (True,  ['base'], 'CUPS-SDK', self.check_cups_devel,'-','cups-config --version'),
            'cups-ddk':          (False, ['base'], "CUPS-DDK", self.check_cupsddk,'-',None), # req. for .drv PPD installs
            'python-dbus':      (True,  ['fax'], "Python-DBUS", self.check_python_dbus,'0.80.0','FUNC#get_python_dbus_ver'),
            'pyqt4':            (True,  ['gui_qt4'], "Python-Qt4", self.check_pyqt4,'4.0','FUNC#get_pyQt4_version'), # PyQt 4.x )
            'pyqt4-dbus' :      (True,  ['gui_qt4'], "PyQt4-DBUS", self.check_pyqt4_dbus,'4.0','FUNC#get_pyQt4_version'), 
            'pyqt':            (True,  ['gui_qt'], "Python-Qt", self.check_pyqt,'2.3','FUNC#get_pyQt_version'), 
            'python-devel' :    (True,  ['base'], "Python-SDK", self.check_python_devel,'2.2','python --version'),
            'python-notify' :   (False, ['gui_qt4'], "Desktop-notifications", self.check_pynotify,'-','python-notify --version'), # Optional for libnotify style popups from hp-systray
            'python-xml'  :     (True,  ['base'], "Python-XML-Lib", self.check_python_xml,'-','FUNC#get_python_xml_version'),
            'pil':              (False, ['scan'], "Python-Image-Lib", self.check_pil,'-','FUNC#get_pil_version'), #required for commandline scanning with hp-scan
            'sane':             (True,  ['scan'], "Scan-Lib", self.check_sane,'-','sane-config --version'),
            'sane-devel' :      (True,  ['scan'], "SANE-SDK", self.check_sane_devel,'-','sane-config --version'),
            'reportlab':        (False, ['fax'], "Python-PDF-Lib", self.check_reportlab,'2.0','FUNC#get_reportlab_version'),
            },
            COMPILEDEP:
            { 'gcc' :             (True,  ['base'], 'gcc-Compiler', self.check_gcc, '-','gcc --version'),
            'libtool':          (True,  ['base'], "Build-tools", self.check_libtool,'-','libtool --version'),
            'make' :            (True,  ['base'], "GNU-Build-tools", self.check_make,'3.0','make --version'),
            },
            PYEXT: 
             { 'cupsext' :         (True,  ['base'], 'CUPS-Extension', self.check_cupsext,'-','FUNC#get_HPLIP_version'),
            'hpmudext' :        (True,  ['base'], 'IO-Extension', self.check_hpmudext,'-','FUNC#get_HPLIP_version'),
            'pcardext' :        (True,  ['base'], 'PhotoCard-Extension', self.check_pcardext,'-','FUNC#get_HPLIP_version'),
            },
            SCANCONF:
            { 'hpaio' :           (True,  ['scan'], 'HPLIP-SANE-Backend', self.check_hpaio,'-','FUNC#get_HPLIP_version'), 
            'scanext' :           (True,  ['scan'], 'Scan-SANE-Extension', self.check_scanext,'-','FUNC#get_HPLIP_version'), 
            }
        }

        self.version_func={
            'FUNC#get_python_dbus_ver':get_python_dbus_ver,
            'FUNC#get_pyQt4_version':get_pyQt4_version,
            'FUNC#get_pyQt_version':get_pyQt_version,
            'FUNC#get_reportlab_version':get_reportlab_version,
            'FUNC#get_xsane_version':get_xsane_version,
            'FUNC#get_pil_version':get_pil_version,
            'FUNC#get_libpthread_version':get_libpthread_version,
            'FUNC#get_python_xml_version':get_python_xml_version,
            'FUNC#get_HPLIP_version':get_HPLIP_version,
            'FUNC#get_libusb_version':get_libusb_version,
            }

    def get_required_deps(self):
        return self.req_deps_to_be_installed


    def get_optional_deps(self):
        return self.opt_deps_to_be_installed


    def get_cmd_to_run(self):
        return self.cmds_to_be_run


    def get_disable_selinux_status(self):
        return self.disable_selinux


    def get_communication_error_devs(self):
        return self.comm_error_devices


    def get_missing_user_grps(self):
        return self.missing_user_grps


    def get_user_grp_cmd(self):
        return self.user_grps_cmd


    def get_plugin_status(self):
        return self.plugin_status


    def get_smart_install_devices(self):
        return self.smart_install_devices


    def validate(self,time_flag=DEPENDENCY_RUN_AND_COMPILE_TIME, is_quiet_mode= False):
        ############ Variables #######################
        cups_ddk_not_req = False
        hpmudext_avail = False
        add_user_to_group = None
        ui_toolkit = sys_conf.get('configure','ui-toolkit')
        org_log_location = log.get_where()

        if is_quiet_mode:
            log.set_where(log.LOG_TO_FILE)

        IS_LIBUSB01_ENABLED = sys_conf.get('configure', 'libusb01-build', 'no')
        vrs =self.get_distro_data('versions_list')
        supported_distro_vrs= self.distro_version
        if self.distro_version not in vrs and len(vrs):
            supported_distro_vrs= vrs[len(vrs)-1]
            log.warn(log.bold("%s-%s version is not supported. Using %s-%s versions dependencies to verify and install..." \
                     %(self.distro_name, self.distro_version, self.distro_name, supported_distro_vrs)))
          
        tui.header("SYSTEM INFO")
        Sts, Kernel_info =utils.run("uname -r -v -o")
        Sts, Host_info =utils.run("uname -n")
        Sts, Proc_info =utils.run("uname -r -v -o")
        log.info(" Kernel: %s Host: %s Proc: %s Distribution: %s %s"\
             %(Kernel_info,Host_info,Proc_info,self.distro_name, self.distro_version))
        log.info(" Bitness: %s bit\n"%utils.getBitness())
        tui.header("HPLIP CONFIGURATION")
        v = sys_conf.get('hplip', 'version')
        if v:
            home = sys_conf.get('dirs', 'home')
            log.info("HPLIP-Version: HPLIP %s" %v)
            log.info("HPLIP-Home: %s" %home)
            if self.is_auto_installer_support():
                log.info("HPLIP-Installation: Auto installation is supported for %s distro  %s version " %(self.distro_name, self.distro_version))
            else:
                log.warn("HPLIP-Installation: Auto installation is not supported for %s distro  %s version " %(self.distro_name, self.distro_version))

            log.info()
            log.info(log.bold("Current contents of '/etc/hp/hplip.conf' file:"))
            try:
                output = file('/etc/hp/hplip.conf', 'r').read()
            except (IOError, OSError), e:
                log.error("Could not access file: %s. Check HPLIP installation." % e.strerror)
                self.num_errors += 1
            else:
                log.info(output)

            log.info()
            log.info(log.bold("Current contents of '/var/lib/hp/hplip.state' file:"))
            try:
                output = file(os.path.expanduser('/var/lib/hp/hplip.state'), 'r').read()
            except (IOError, OSError), e:
                log.info("Plugins are not installed. Could not access file: %s" % e.strerror)
            else:
                log.info(output)

            log.info()
            log.info(log.bold("Current contents of '~/.hplip/hplip.conf' file:"))
            try:
                output = file(os.path.expanduser('~/.hplip/hplip.conf'), 'r').read()
            except (IOError, OSError), e:
                log.warn("Could not access file: %s" % e.strerror)
                self.num_warns += 1
            else:
                log.info(output)

            scanning_enabled = utils.to_bool(sys_conf.get('configure', 'scanner-build', '0'))
            log.info(" %-20s %-20s %-10s %-10s %-10s %-10s %s"%( "<Package-name>", " <Package-Desc>", "<Required/Optional>", "<Min-Version>","<Installed-Version>", "<Status>", "<Comment>"))
            for s in self.hplip_dependencies:
                if s == EXTERNALDEP: 
                    if time_flag == DEPENDENCY_RUN_AND_COMPILE_TIME or time_flag == DEPENDENCY_RUN_TIME:
                        tui.header(" External Dependencies")
                    else: continue
                elif s == GENERALDEP: 
                    if time_flag == DEPENDENCY_RUN_AND_COMPILE_TIME or time_flag == DEPENDENCY_RUN_TIME:
                        tui.header(" General Dependencies")
                    else: continue
                elif s == COMPILEDEP: 
                    if time_flag == DEPENDENCY_RUN_AND_COMPILE_TIME or time_flag == DEPENDENCY_COMPILE_TIME:
                        tui.header(" Compile Time Dependencies")
                    else: continue
                elif s == PYEXT: tui.header(" Python Extentions")
                elif s == SCANCONF: tui.header(" Scan Configuration")
                else: tui.header(" Other Dependencies")
                for d in self.hplip_dependencies[s]:
                    if d == 'cups-ddk' and cups_ddk_not_req == True:
                        continue
                    elif ui_toolkit != 'qt4' and ui_toolkit != 'qt3' and d == 'pyqt':
                        continue
                    elif d == 'pyqt' and ui_toolkit == 'qt4':
                        continue
                    elif d == 'pyqt4' and ui_toolkit == 'qt3':
                        continue
                    elif d == 'hpaio' and not scanning_enabled:
                        continue
                    elif self.distro_name =="rhel" and "5." in self.distro_version:
                        if d in ['dbus','python-devel','python-dbus','pyqt4-dbus','libnetsnmp-devel','gcc','make','reportlab','policykit','sane-devel','cups-ddk']:
                            continue

                    if self.hplip_dependencies[s][d][5] is None:
                        installed_ver = '-'
                    elif Ver_Func_Pat.search(self.hplip_dependencies[s][d][5]):
                        if self.hplip_dependencies[s][d][5] in self.version_func:
                            installed_ver = self.version_func[self.hplip_dependencies[s][d][5]]()
                        else:
                            installed_ver = '-'
                    else:
                        installed_ver = get_version(self.hplip_dependencies[s][d][5])
                    Status = Status_Type(self.hplip_dependencies[s][d][3](),self.hplip_dependencies[s][d][4],installed_ver) 
                    comment = get_comment(d, Status, installed_ver)
                    packages_to_install, commands=[],[]
                    if self.is_auto_installer_support():
                        packages_to_install, commands = self.get_dependency_data(d)
                        if not packages_to_install and d == 'hpaio':
                            packages_to_install.append(d)
                    else:
                        packages_to_install, commands = self.get_dependency_data(d,supported_distro_vrs)
                        if not packages_to_install and d == 'hpaio':
                            packages_to_install.append(d)
                            
                    if self.hplip_dependencies[s][d][0]:
                        package_type = "REQUIRED"
                    else:
                        package_type = "OPTIONAL"
                        
                    if d == 'cups' and ((installed_ver == '-') or check_version(installed_ver,'1.4')):
                        cups_ddk_not_req = True
                        log.debug("cups -ddk not required as cups version [%s] is => 1.4 "%installed_ver)
                    if d == 'hpmudext' and Status == 'OK':
                        hpmudext_avail = True
                        
                    if Status == 'OK':
                        log.info(" %-20s %-25s %-15s %-15s %-15s %-10s %s" %(d,self.hplip_dependencies[s][d][2], package_type,self.hplip_dependencies[s][d][4],installed_ver,Status,comment))
                    else:
                        log.info(log.red(" error: %-13s %-25s %-15s %-15s %-15s %-10s %s" %(d,self.hplip_dependencies[s][d][2], package_type,self.hplip_dependencies[s][d][4],installed_ver,Status,comment)))
                        self.num_errors += 1
                        for cmd in commands:
                            if cmd:
                                self.cmds_to_be_run.append(cmd)
                        if package_type == "OPTIONAL":
                            for pkg in packages_to_install:
                                if pkg:
                                    self.opt_deps_to_be_installed.append(pkg)
                        else:
                            for pkg in packages_to_install:
                                if pkg:
                                    self.req_deps_to_be_installed.append(pkg)

            if scanning_enabled:
                tui.header("DISCOVERED SCANNER DEVICES")
                if utils.which('scanimage'):
                    status, output = utils.run("scanimage -L")
                    if status != 0 :
                        log.error("Failed to get Scanners information.")
                    elif 'No scanners were identified' in output:
                        log.info("No Scanner found.")
                    else:
                        log.info(output)

            if device_avail:
                #if prop.par_build:
                    #tui.header("DISCOVERED PARALLEL DEVICES")
                    #devices = device.probeDevices(['par'])
                    #if devices:
                        #f = tui.Formatter()
                        #f.header = ("Device URI", "Model")
                        #for d, dd in devices.items():
                            #f.add((d, dd[0]))
                        #f.output()
                    #else:
                        #log.info("No devices found.")
                        #if not core.have_dependencies['ppdev']:
                            #log.error("'ppdecmds_to_be_runv' kernel module not loaded.")

                if prop.usb_build:
                    tui.header("DISCOVERED USB DEVICES")

                    devices = device.probeDevices(['usb'])

                    if devices:
                        f = tui.Formatter()
                        f.header = ("Device URI", "Model")

                        for d, dd in devices.items():
                            f.add((d, dd[0]))

                        f.output()

                    else:
                        log.info("No devices found.")


            tui.header("INSTALLED CUPS PRINTER QUEUES")

            lpstat_pat = re.compile(r"""(\S*): (.*)""", re.IGNORECASE)
            status, output = utils.run('lpstat -v')
            log.info()

            cups_printers = []
            plugin_sts = None
            for p in output.splitlines():
                try:
                    match = lpstat_pat.search(p)
                    printer_name = match.group(1)
                    device_uri = match.group(2)
                    cups_printers.append((printer_name, device_uri))
                except AttributeError:
                    pass

            log.debug(cups_printers)
            if cups_printers:
                #non_hp = False
                for p in cups_printers:
                    printer_name, device_uri = p

                    if device_uri.startswith("cups-pdf:/") or \
                        device_uri.startswith('ipp://'):
                        continue

                    try:
                        back_end, is_hp, bus, model, serial, dev_file, host, zc, port = \
                            device.parseDeviceURI(device_uri)
                    except Error:
                        back_end, is_hp, bus, model, serial, dev_file, host, zc, port = \
                            '', False, '', '', '', '', '', '', 1

                    #print back_end, is_hp, bus, model, serial, dev_file, host, zc, port

                    log.info(log.bold(printer_name))
                    log.info(log.bold('-'*len(printer_name)))

                    x = "Unknown"
                    if back_end == 'hpfax':
                        x = "Fax"
                    elif back_end == 'hp':
                        x = "Printer"

                    log.info("Type: %s" % x)

                    #if is_hp:
                    #    x = 'Yes, using the %s: CUPS backend.' % back_end
                    #else:
                    #    x = 'No, not using the hp: or hpfax: CUPS backend.'
                    #    non_hp = True

                    #log.info("Installed in HPLIP?: %s" % x)
                    log.info("Device URI: %s" % device_uri)

                    ppd = os.path.join('/etc/cups/ppd', printer_name + '.ppd')

                    if os.path.exists(ppd):
                        log.info("PPD: %s" % ppd)
                        nickname_pat = re.compile(r'''\*NickName:\s*\"(.*)"''', re.MULTILINE)
                        try:
                            f = file(ppd, 'r').read(4096)
                        except IOError:
                            log.warn("Failed to read %s ppd file"%ppd)
                            desc = ''
                        else:
                            try:
                                desc = nickname_pat.search(f).group(1)
                            except AttributeError:
                                desc = ''

                        log.info("PPD Description: %s" % desc)

                        status, output = utils.run('lpstat -p%s' % printer_name)
                        log.info("Printer status: %s" % output.replace("\n", ""))

                        if back_end == 'hpfax' and not 'HP Fax' in desc:
                            self.num_errors += 1
                            log.error("Incorrect PPD file for fax queue '%s'. Fax queues must use 'HP-Fax-hplip.ppd'." % printer_name)

                        elif back_end == 'hp' and 'HP Fax' in desc:
                            self.num_errors += 1
                            log.error("Incorrect PPD file for a print queue '%s'. Print queues must not use 'HP-Fax-hplip.ppd'." % printer_name)

                        elif back_end not in ('hp', 'hpfax'):
                            log.warn("Printer is not HPLIP installed. Printers must use the hp: or hpfax: CUPS backend for HP-Devices.")
                            self.num_warns += 1

                    if device_avail and is_hp:
                        d = None
                        try:
                            try:
                                d = device.Device(device_uri,None, None, None, True)
                            except Error:
                                log.error("Device initialization failed.")
                                continue

                            plugin = d.mq.get('plugin', PLUGIN_NONE)
                            if plugin in (PLUGIN_REQUIRED, PLUGIN_OPTIONAL):
                                if not plugin_sts:
                                    from installer import pluginhandler
                                    pluginObj = pluginhandler.PluginHandle()
                                    plugin_sts = pluginObj.getStatus()

                                if plugin_sts == pluginhandler.PLUGIN_INSTALLED:
                                    self.plugin_status = PLUGIN_INSTALLED
                                    if plugin == pluginhandler.PLUGIN_REQUIRED:
                                        log.info("Required plug-in status: Installed")
                                    else:
                                        log.info("Optional plug-in status: Installed")
                                elif plugin_sts == pluginhandler.PLUGIN_NOT_INSTALLED:
                                    self.plugin_status = PLUGIN_NOT_INSTALLED
                                    if plugin == PLUGIN_REQUIRED:
                                        self.num_errors += 1
                                        log.error("Required plug-in status: Not installed")
                                    else:
                                        self.num_warns +=1
                                        log.warn("Optional plug-in status: Not installed")
                                elif plugin_sts == pluginhandler.PLUGIN_VERSION_MISMATCH:
                                    self.num_warns += 1
                                    self.plugin_status = pluginhandler.PLUGIN_VERSION_MISMATCH
                                    log.warn("plug-in status: Version mismatch")


                            if bus in ('par', 'usb'):
                                try:
                                    d.open()
                                except Error, e:
                                    log.error(e.msg)
                                    deviceid = ''
                                else:
                                    deviceid = d.getDeviceID()
                                    log.debug(deviceid)

                                #print deviceid
                                if not deviceid:
                                    log.error("Communication status: Failed")
                                    self.comm_error_devices[printer_name] = device_uri
                                    self.num_errors += 1
                                else:
                                    log.info("Communication status: Good")

                            elif bus == 'net':
                                try:
                                    error_code, deviceid = d.getPML(pml.OID_DEVICE_ID)
                                except Error:
                                    pass

                                #print error_code
                                if not deviceid:
                                    log.error("Communication status: Failed")
                                    self.comm_error_devices[printer_name] = device_uri
                                    self.num_errors += 1
                                else:
                                    log.info("Communication status: Good")

                        finally:
                            if d is not None:
                                d.close()
                    log.info()
            else:
                log.warn("No queues found.")

            tui.header("PERMISSION")
            sts,avl_grps_out =utils.run('groups')
            self.user_grps_cmd  = self.get_distro_ver_data('add_user_to_group', '',supported_distro_vrs)
            sts, out = utils.check_user_groups(self.user_grps_cmd, avl_grps_out) 
            if sts:
                log.info("%-15s %-30s %-15s %-8s %-8s %-8s %s"%("groups", "user-groups","Required", "-","-", "OK",avl_grps_out))
            else:
                log.info(log.red("error: %-8s %-30s %-15s %-8s %-8s %-8s %s"%("groups", "user-groups", "Required","-", "-", "MISSING", out)))
                self.num_errors += 1
                self.missing_user_grps = out

            if hpmudext_avail:
                lsusb = utils.which('lsusb')
                if lsusb:
                    lsusb = os.path.join(lsusb, 'lsusb')
                    status, output = utils.run("%s -d03f0:" % lsusb)

                    if output:
                        lsusb_pat = re.compile("""^Bus\s([0-9a-fA-F]{3,3})\sDevice\s([0-9a-fA-F]{3,3}):\sID\s([0-9a-fA-F]{4,4}):([0-9a-fA-F]{4,4})(.*)""", re.IGNORECASE)
                        log.debug(output)
                        try:
                            import hpmudext
                        except ImportError:
                            log.error("NOT FOUND OR FAILED TO LOAD! Please reinstall HPLIP and check for the proper installation of hpmudext.")
                            self.num_errors += 1

                        for o in output.splitlines():
                            ok = True
                            match = lsusb_pat.search(o)

                            if match is not None:
                                bus, dev, vid, pid, mfg = match.groups()
                                #log.info("\nHP Device 0x%x at %s:%s: " % (int(pid, 16), bus, dev))
                                result_code, deviceuri = hpmudext.make_usb_uri(bus, dev)

                                if result_code == hpmudext.HPMUD_R_OK:
                                #    log.info("    Device URI: %s" %  deviceuri)
                                    d = None
                                    try:
                                        d = device.Device(deviceuri,None, None, None, True)
                                    except Error:
                                        continue
                                    if not d.supported:
                                        continue
                                else:
                                    log.warn("    Device URI: (Makeuri FAILED)")
                                    continue
                                printers = cups.getPrinters()
                                printer_name=None
                                for p in printers:
                                    if p.device_uri == deviceuri:
                                        printer_name=p.name
                                        break

                                devnode = os.path.join("/", "dev", "bus", "usb", bus, dev)

                                if not os.path.exists(devnode):
                                    devnode = os.path.join("/", "proc", "bus", "usb", bus, dev)

                                if os.path.exists(devnode):
                                   # log.debug("    Device node: %s" % devnode)
                                    st_mode, st_ino, st_dev, st_nlink, st_uid, st_gid, \
                                       st_size, st_atime, st_mtime, st_ctime =  os.stat(devnode)

                                    getfacl = utils.which('getfacl',True)
                                    if getfacl:
                                       # log.debug("%s %s" % (getfacl, devnode))
                                        status, output = utils.run("%s %s" % (getfacl, devnode))
                                        getfacl_out_list = output.split('\r\n')

                                        out =''
                                        for g in getfacl_out_list:
                                            if 'getfacl' not in g and '' is not g and 'file' not in g:
                                                pat = re.compile('''.*:(.*)''')
                                                if pat.search(g):
                                                    out = out +' '+ pat.search(g).group(1)
                                        log.info("%-15s %-30s %-15s %-8s %-8s %-8s %s"%("USB", printer_name, "Required", "-", "-", "OK", "Node:'%s' Perm:'%s'"%(devnode,out)))
                                    else:
                                        log.info("%-15s %-30s %-15s %-8s %-8s %-8s %s"%("USB", printer_name, "Required","-","-","OK", "Node:'%s' Mode:'%s'"%(devnode,st_mode&0777)))

            selinux_file = '/etc/selinux/config'
            if os.path.exists(selinux_file):
                tui.header("SELINUX")
                try:
                    selinux_fp = file(selinux_file, 'r')
                except IOError:
                    log.error("Failed to open %s file."%selinux_file)
                else:
                    for line in selinux_fp:
                        line=re.sub(r'\s','',line)
                        if line == "SELINUX=enforcing":
                            self.num_warns += 1
                            log.warn("%-12s %-12s %-10s %-3s %-3s %-8s %s" \
                                          %("SELinux",  "enabled", "Optional", "-", "-", "INCOMPAT", "'SELinux needs to be disabled for Plugin printers and Fax functionality.'"))
                            self.disable_selinux = True
                            break
                    if self.disable_selinux == False:
                        log.info("%-15s %-15s %-10s %-3s %-3s %-8s %s"\
                                                  %("SELinux",  "disabled", "Optional", "-", "-", "OK", "-"))

            self.smart_install_devices = smart_install.get_smartinstall_enabled_devices()
            if len(self.smart_install_devices):
                tui.header("'CD-ROM'/'Smart Install' Detected Devices")
                self.num_errors += 1
                for d in self.smart_install_devices:
                    log.error("%-30s %-20s %s "%(d, "CD_ROM_Enabled", "Needs to disable Smart Install"))

        else:
            log.error("HPLIP not found.")
            self.num_errors += 1

        if is_quiet_mode:
            log.set_where(org_log_location)

        return self.num_errors, self.num_warns


    def display_summary(self):
        tui.header("SUMMARY")
        
        log.info(log.bold("Missing Required Dependencies"))
        log.info(log.bold('-'*len("Missing Required Dependencies")))
        if len(self.req_deps_to_be_installed) == 0:
            log.info("None")
        else:
            for packages_to_install in self.req_deps_to_be_installed:
                if packages_to_install == 'cups':
                    log.error("'%s' package is missing or '%s' service is not running."%(packages_to_install,packages_to_install))
                else:
                    log.error("'%s' package is missing/incompatible "%packages_to_install)
        
        log.info("")
        log.info(log.bold("Missing Optional Dependencies"))
        log.info(log.bold('-'*len("Missing Optional Dependencies")))
        if len(self.opt_deps_to_be_installed) == 0:
            log.info("None\n")
        else:
            for packages_to_install in self.opt_deps_to_be_installed:
                log.error("'%s' package is missing/incompatible "%packages_to_install)
        
        if self.plugin_status == PLUGIN_NOT_INSTALLED or self.plugin_status == PLUGIN_VERSION_MISMATCH:
            log.info("")
            log.info(log.bold("Plug-in Status"))
            log.info(log.bold('-'*len("Plug-in Status")))
            log.error("Plug-ins need to be installed")
        
        if self.disable_selinux == True:
            log.info("")
            log.info(log.bold("SELINUX"))
            log.info(log.bold('-'*len("SELINUX")))
            log.error("SELINUX need to be disabled")
        
        if self.missing_user_grps:
            log.info("")
            log.info(log.bold("USER GROUPS"))
            log.info(log.bold('-'*len("USER GROUPS")))
            log.error("%s groups need to be added for %s user"%(self.missing_user_grps,prop.username))
            
        if self.smart_install_devices:
            log.info("")
            log.info(log.bold("SMART INSTALL/CD_ROM ENABLED DEVICES"))
            log.info(log.bold('-'*len("SMART INSTALL/CD_ROM ENABLED DEVICES")))
            for dev in self.smart_install_devices:
                log.error("%s"%dev)
            url, tool_name = smart_install.get_SmartInstall_tool_info()
            log.info(log.bold("Smart Install is enabled for these devices. Please disable Smart Install to enable device functionalities.\n\nRefer link '%s' to disable Smart Install.\n"%(url)))
            
        log.info("")
        log.info("Total Errors: %d" % self.num_errors)
        log.info("Total Warnings: %d" % self.num_warns)
        log.info()
        if self.disable_selinux or self.missing_user_grps or (self.plugin_status == PLUGIN_VERSION_MISMATCH) or (self.plugin_status == PLUGIN_NOT_INSTALLED) or len(self.req_deps_to_be_installed) or len(self.opt_deps_to_be_installed):
             log.info("Re-run 'hp-doctor' command to prompt and fix the issues. ")
             

############ Main #######################
if __name__ == "__main__":
    try:
        log.set_module(__mod__)

        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hl:gtcrbsi', ['help', 'help-rest', 'help-man', 'help-desc', 'logging=', 'run', 'runtime', 'compile', 'both','fix'])
        except getopt.GetoptError, e:
            log.error(e.msg)
            usage()
            sys.exit(1)

        log_level = 'info'
        if os.getenv("HPLIP_DEBUG"):
            log_level = 'debug'

        time_flag = DEPENDENCY_RUN_AND_COMPILE_TIME
        is_quiet_mode = False
        fmt = True
        for o, a in opts:
            if o in ('-h', '--help'):
                usage()
            elif o == '--help-rest':
                usage('rest')
            elif o == '--help-man':
                usage('man')
            elif o == '--help-desc':
                print __doc__,
                sys.exit(0)
            elif o in ('-l', '--logging'):
                log_level = a.lower().strip()
            elif o == '-g':
                log_level = 'debug'
            elif o == '-t':
                fmt = False
            elif o in ('-c', '--compile'):
                time_flag = DEPENDENCY_COMPILE_TIME
            elif o in ('-r', '--runtime', '--run'):
                time_flag = DEPENDENCY_RUN_TIME
            elif o in ('-b', '--both'):
                time_flag = DEPENDENCY_RUN_AND_COMPILE_TIME
            elif o == '--fix':
                log.info(log.bold("\n\nNote:- 'hp-check --fix' is deprecated. Please run 'hp-doctor' command\n\n"))
                sys.exit(1)
            elif o == '-s':
                is_quiet_mode = True

        if not log.set_level(log_level):
            usage()

        if not fmt:
            log.no_formatting()

        log_file = os.path.abspath('./hp-check.log')
        log.info(log.bold("Saving output in log file: %s" % log_file))

        if os.path.exists(log_file):
            os.remove(log_file)

        log.set_logfile(log_file)
        if not is_quiet_mode:
            log.set_where(log.LOG_TO_CONSOLE_AND_FILE)
        else:
            log.set_where(log.LOG_TO_FILE)

        show_title()
        ui_toolkit = sys_conf.get('configure','ui-toolkit')
        core =  DependenciesCheck(MODE_CHECK,INTERACTIVE_MODE,ui_toolkit)
        core.init()
        num_errors, num_warns = core.validate(time_flag, is_quiet_mode)

        if num_errors or num_warns:
            core.display_summary()
        else:
            log.info(log.green("No errors or warnings."))

    except KeyboardInterrupt:
        log.error("User exit")

    log.info()
    log.info("Done.")
