#!/usr/bin/env python
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

__version__ = '4.0'
__title__ = "Fax Address Book"
__doc__ = "A simple fax address book for HPLIP."

import cmd
from base.g import *
from base import utils, tui
import getopt

log.set_module("hp-fab")


USAGE = [(__doc__, "", "name", True),
         ("Usage: hp-fab [MODE] [OPTIONS]", "", "summary", True),
         ("[MODE]", "", "header", False),
         ("Enter interactive mode:", "-i or --interactive (see Note 1)", "option", False),
         ("Enter graphical UI mode:", "-u or --gui (Default)", "option", False),
         utils.USAGE_SPACE,
         utils.USAGE_OPTIONS,
         utils.USAGE_LANGUAGE,
         utils.USAGE_LOGGING1, utils.USAGE_LOGGING2, utils.USAGE_LOGGING3,
         utils.USAGE_HELP,
         utils.USAGE_NOTES,
         ("1. Use 'help' command at the fab > prompt for command help (interactive mode (-i) only).", "", "note", False),
         utils.USAGE_SPACE,
         utils.USAGE_SEEALSO,
         ("hp-sendfax", "", "seealso", False),
         ]

def usage(typ='text'):
    if typ == 'text':
        utils.log_title(__title__, __version__)

    utils.format_text(USAGE, typ, __title__, 'hp-fab', __version__)
    sys.exit(0)


# Console class (from ASPN Python Cookbook)
# Author:   James Thiele
# Date:     27 April 2004
# Version:  1.0
# Location: http://www.eskimo.com/~jet/python/examples/cmd/
# Copyright (c) 2004, James Thiele
class Console(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.intro  = "Type 'help' for a list of commands. Type 'exit' or 'quit' to quit."
        self.db =  fax.FaxAddressBook2() # database instance
        self.prompt = log.bold("hp-fab > ")

    # Command definitions
    def do_hist(self, args):
        """Print a list of commands that have been entered"""
        print self._hist

    def do_exit(self, args):
        """Exits from the console"""
        return -1

    def do_quit(self, args):
        """Exits from the console"""
        return -1

    # Command definitions to support Cmd object functionality
    def do_EOF(self, args):
        """Exit on system end of file character"""
        return self.do_exit(args)

    def do_help(self, args):
        """Get help on commands
           'help' or '?' with no arguments prints a list of commands for which help is available
           'help <command>' or '? <command>' gives help on <command>
        """
        # The only reason to define this method is for the help text in the doc string
        cmd.Cmd.do_help(self, args)

    # Override methods in Cmd object
    def preloop(self):
        """Initialization before prompting user for commands.
           Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
        """
        cmd.Cmd.preloop(self)   # sets up command completion
        self._hist    = []      # No history yet
        self._locals  = {}      # Initialize execution namespace for user
        self._globals = {}

        self.do_list('')

    def postloop(self):
        """Take care of any unfinished business.
           Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
        """
        cmd.Cmd.postloop(self)   # Clean up command completion
        print "Exiting..."

    def precmd(self, line):
        """ This method is called after the line has been input but before
            it has been interpreted. If you want to modifdy the input line
            before execution (for example, variable substitution) do it here.
        """
        self._hist += [line.strip()]
        return line

    def postcmd(self, stop, line):
        """If you want to stop the console, return something that evaluates to true.
           If you want to do some post command processing, do it here.
        """
        return stop

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def default(self, line):
        print log.red("error: Unrecognized command. Use 'help' to list commands.")

    def get_nickname(self, args, fail_if_match=True, alt_text=False):
        if not args:
            while True:
                if alt_text:
                    nickname = raw_input(log.bold("Enter the name (nickname) to add (<enter>=done*, c=cancel) ? ")).strip()
                else:
                    nickname = raw_input(log.bold("Enter the name (nickname) (c=cancel) ? ")).strip()

                if nickname.lower() == 'c':
                    print log.red("Canceled")
                    return ''

                if not nickname:
                    if alt_text:
                        return ''
                    else:
                        print log.red("error: Nickname must not be blank.")
                        continue


                if fail_if_match:
                    if self.db.get(nickname) is not None:
                        print log.red("error: Name already exists. Please choose a different name.")
                        continue

                else:
                    if self.db.get(nickname) is None:
                        print log.red("error: Name not found. Please enter a different name.")
                        continue

                break

        else:
            nickname = args.strip()

            if fail_if_match:
                if self.db.get(nickname) is not None:
                    print log.red("error: Name already exists. Please choose a different name.")
                    return ''

            else:
                if self.db.get(nickname) is None:
                    print log.red("error: Name not found. Please enter a different name.")
                    return ''

        return nickname


    def get_groupname(self, args, fail_if_match=True, alt_text=False):
        all_groups = self.db.get_all_groups()
        
        if not args:
            while True:
                if alt_text:
                    groupname = raw_input(log.bold("Enter the group name to join (<enter>=done*, c=cancel) ? ")).strip()
                else:
                    groupname = raw_input(log.bold("Enter the group name (c=cancel) ? ")).strip()


                if groupname.lower() == 'c':
                    print log.red("Canceled")
                    return ''

                if not groupname:
                    if alt_text:
                        return ''
                    else:
                        print log.red("error: The group name must not be blank.")
                        continue

                if fail_if_match: 
                    if groupname in all_groups:
                        print log.red("error: Name already exists. Please choose a different name.")
                        continue

                else:
                    if groupname not in all_groups:
                        print log.red("error: Name not found. Please enter a different name.")
                        continue

                break

        else:
            groupname = args.strip()

            if fail_if_match: 
                if groupname in all_groups:
                    print log.red("error: Name already exists. Please choose a different name.")
                    return ''

            else:
                if groupname not in all_groups:
                    print log.red("error: Name not found. Please enter a different name.")
                    return ''

        return groupname

    def do_list(self, args):
        """ 
        List names and/or groups.
        list [names|groups|all|]
        dir [names|groups|all|]
        """

        if args:
            scope = args.strip().split()[0]

            if args.startswith('nam'):
                self.do_names('')
                return
                
            elif args.startswith('gro'):
                self.do_groups('')
                return

        self.do_names('')
        self.do_groups('')

    do_dir = do_list

    def do_names(self, args):
        """
        List names.
        names
        """
        all_entries = self.db.get_all_records()
        log.debug(all_entries)

        print log.bold("\nNames:\n")
        if len(all_entries) > 0:
        
            f = tui.Formatter()
            f.header = ("Name", "Fax Number", "Member of Group(s)")
            for name, e in all_entries.items():
                f.add((name, e['fax'], ', '.join(e['groups'])))
                
            f.output()

        else:
            print "(None)"

        print

    def do_groups(self, args):
        """ 
        List groups.
        groups
        """
        #all_groups = self.db.AllGroups() XXXXXXXXXXXXXX
        all_groups = self.db.get_all_groups()
        log.debug(all_groups)

        print log.bold("\nGroups:\n")
        if len(all_groups):

            f = tui.Formatter()
            f.header = ("Group", "Members")
            for group in all_groups:
                f.add((group, ', '.join(self.db.group_members(group))))
            f.output()
            
        else:
            print "(None)"

        print


    def do_edit(self, args):
        """
        Edit an name.
        edit [name]
        modify [name]
        """
        nickname = self.get_nickname(args, fail_if_match=False)
        if not nickname: return

        e = self.db.get(nickname)
        log.debug(e)

        print log.bold("\nEdit/modify information for %s:\n" % nickname)

        save_title = e['title']
        title = raw_input(log.bold("Title (<enter>='%s', c=cancel)? " % save_title)).strip()

        if title.lower() == 'c':
            print log.red("Canceled")
            return

        if not title:
            title = save_title

        save_firstname = e['firstname']
        firstname = raw_input(log.bold("First name (<enter>='%s', c=cancel)? " % save_firstname)).strip()

        if firstname.lower() == 'c':
            print log.red("Canceled")
            return

        if not firstname:
            firstname = save_firstname

        save_lastname = e['lastname']
        lastname = raw_input(log.bold("Last name (<enter>='%s', c=cancel)? " % save_lastname)).strip()

        if lastname.lower() == 'c':
            print log.red("Canceled")
            return

        if not lastname:
            lastname = save_lastname

        save_faxnum = e['fax']
        while True:
            faxnum = raw_input(log.bold("Fax Number (<enter>='%s', c=cancel)? " % save_faxnum)).strip()

            if faxnum.lower() == 'c':
                print log.red("Canceled")
                return

            if not faxnum and not save_faxnum:
                print log.red("error: Fax number must not be empty.")
                continue

            if not faxnum:
                faxnum = save_faxnum

            ok = True
            for c in faxnum:
                if c not in '0123456789-(+) *#':
                    print log.red("error: Invalid characters in fax number. Fax number may only contain '0123456789-(+) '")
                    ok = False
                    break


            if ok: break

        save_notes = e['notes']
        notes = raw_input(log.bold("Notes (<enter>='%s', c=cancel)? " % save_notes)).strip()

        if notes.lower() == 'c':
            print log.red("Canceled")
            return

        if not notes:
            notes = save_notes

        if e['groups']:
            print "\nLeave or Stay in a Group:\n"

        new_groups = []
        for g in e['groups']:
            ok, ans = tui.enter_yes_no("Stay in group %s" % g, 
                choice_prompt="(y=yes* (stay), n=no (leave), c=cancel)")

            if not ok:
                print log.red("Canceled")
                return
            
            if ans:
                new_groups.append(g)

        print "\nJoin New Group(s):\n"

        while True:
            add_group = self.get_groupname('', fail_if_match=False, alt_text=True) 

            if add_group.lower() == 'c':
                print log.red("Canceled")
                return

            if not add_group.lower():
                break

            get_all_groups = self.db.get_all_groups()

            if add_group not in all_groups:
                log.warn("Group not found.")
                ok, ans = tui.enter_yes_no("Is this a new group", 
                    choice_prompt="(y=yes* (new), n=no, c=cancel)")

                if not ok:
                    print log.red("Canceled")
                    return
                
                if not ans:
                    continue

            if add_group in e['groups']:
                log.error("error: Group already specified. Choose a different group name or press <enter> to continue.")
                continue

            new_groups.append(add_group)
        
        
        self.db.set(nickname, title, firstname, lastname, faxnum, new_groups, notes)
        self.do_show(nickname)

        print

    do_modify = do_edit


    def do_editgrp(self, args):
        """
        Edit a group.
        editgrp [group]
        modifygrp [group]
        """
        group = self.get_groupname(args, fail_if_match=False)
        if not group: return

        old_entries = self.db.group_members(group)

        new_entries = []

        print "\nLeave or Remove Existing Names in Group:\n"

        for e in old_entries:
            
            ok, ans = tui.enter_yes_no("Leave name '%s' in this group" % e, 
                choice_prompt="(y=yes* (leave), n=no (remove), c=cancel)")
                
            if not ok:
                print log.red("Canceled")
                return
            
            if ans:
                new_entries.append(e)

        print "\nAdd New Names in Group:\n"

        while True:
            nickname = self.get_nickname('', fail_if_match=False, alt_text=True)

            if nickname.lower() == 'c':
                print log.red("Canceled")
                return

            if not nickname.lower():
                break

            new_entries.append(nickname)
            
        self.db.update_groups(group, new_entries)

        print

    do_modifygrp = do_editgrp


    def do_add(self, args):
        """
        Add an name.
        add [name]
        new [name]
        """
        nickname = self.get_nickname(args, fail_if_match=True)
        if not nickname: return

        print log.bold("\nEnter information for %s:\n" % nickname)

        title = raw_input(log.bold("Title (c=cancel)? ")).strip()

        if title.lower() == 'c':
            print log.red("Canceled")
            return

        firstname = raw_input(log.bold("First name (c=cancel)? ")).strip()

        if firstname.lower() == 'c':
            print log.red("Canceled")
            return

        lastname = raw_input(log.bold("Last name (c=cancel)? ")).strip()

        if lastname.lower() == 'c':
            print log.red("Canceled")
            return

        while True:
            faxnum = raw_input(log.bold("Fax Number (c=cancel)? ")).strip()

            if faxnum.lower() == 'c':
                print log.red("Canceled")
                return

            if not faxnum:
                print log.red("error: Fax number must not be empty.")
                continue

            ok = True
            for c in faxnum:
                if c not in '0123456789-(+) *#':
                    print log.red("error: Invalid characters in fax number. Fax number may only contain '0123456789-(+) *#'")
                    ok = False
                    break


            if ok: break

        notes = raw_input(log.bold("Notes (c=cancel)? ")).strip()

        if notes.strip().lower() == 'c':
            print log.red("Canceled")
            return

        groups = []
        all_groups = self.db.get_all_groups()
        while True:
            add_group = raw_input(log.bold("Member of group (<enter>=done*, c=cancel) ?" )).strip()

            if add_group.lower() == 'c':
                print log.red("Canceled")
                return

            if not add_group:
                break

            if add_group not in all_groups:
                log.warn("Group not found.")

                while True:
                    user_input = raw_input(log.bold("Is this a new group (y=yes*, n=no) ?")).lower().strip()

                    if user_input not in ['', 'n', 'y']:
                        log.error("Please enter 'y', 'n' or press <enter> for 'yes'.")
                        continue

                    break

                if user_input == 'n':
                    continue

            if add_group in groups:
                log.error("Group already specified. Choose a different group name or press <enter> to continue.")
                continue

            groups.append(add_group)

        self.db.set(nickname, title, firstname, lastname, faxnum, groups, notes)
        self.do_show(nickname)


    do_new = do_add


    def do_addgrp(self, args):
        """
        Add a group.
        addgrp [group]
        newgrp [group]
        """
        group = self.get_groupname(args, fail_if_match=True)
        if not group: return

        entries = []
        while True:
            nickname = self.get_nickname('', fail_if_match=False, alt_text=True)

            if nickname.lower() == 'c':
                print log.red("Canceled")
                return

            if not nickname.lower():
                break

            entries.append(nickname)

        self.db.update_groups(group, entries)

        print

    do_newgrp = do_addgrp


    def do_view(self, args):
        """
        View all name data.
        view
        """
        all_entries = self.db.get_all_records()
        log.debug(all_entries)

        print log.bold("\nView all Data:\n")
        if len(all_entries) > 0:

            f = tui.Formatter()
            f.header = ("Name", "Title", "First Name", "Last Name", "Fax", "Notes", "Member of Group(s)")
            
            for name, e in all_entries.items():
                f.add((name, e['title'], e['firstname'], e['lastname'], e['fax'], 
                       e['notes'], ', '.join(e['groups'])))
                          
            f.output()

        print



    def do_show(self, args):
        """
        Show a name (all details).
        show [name]
        details [name]
        """
        name = self.get_nickname(args, fail_if_match=False)
        if not name: return

        e = self.db.get(name)
        if e:
            f = tui.Formatter()
            f.header = ("Key", "Value")
            f.add(("Name:", name))
            f.add(("Title:", e['title']))
            f.add(("First Name:", e['firstname']))
            f.add(("Last Name:", e['lastname']))
            f.add(("Fax Number:", e['fax']))
            f.add(("Notes:", e['notes']))
            f.add(("Member of Group(s):", ', '.join(e['groups'])))
            
            f.output()
            
        else:
            print log.red("error: Name not found. Use the 'names' command to view all names.")

        print

    do_details = do_show

    def do_rm(self, args):
        """
        Remove a name.
        rm [name]
        del [name]
        """
        nickname = self.get_nickname(args, fail_if_match=False)
        if not nickname: return

        self.db.delete(nickname)

        print

    do_del = do_rm

    def do_rmgrp(self, args):
        """
        Remove a group.
        rmgrp [group]
        delgrp [group]
        """
        group = self.get_groupname(args, fail_if_match=False)
        if not group: return

        self.db.delete_group(group)

        print

    do_delgrp = do_rmgrp


    def do_about(self, args):
        """About fab."""
        utils.log_title(__title__, __version__)


mode = GUI_MODE
mode_specified = False
loc = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'l:hgiuq:', 
        ['level=', 'help', 'help-rest', 'help-man',
         'help-desc', 'gui', 'interactive', 'lang='])

except getopt.GetoptError, e:
    log.error(e.msg)
    usage()

if os.getenv("HPLIP_DEBUG"):
    log.set_level('debug')

for o, a in opts:
    if o in ('-l', '--logging'):
        log_level = a.lower().strip()
        if not log.set_level(log_level):
            usage()

    elif o == '-g':
        log.set_level('debug')

    elif o in ('-h', '--help'):
        usage()

    elif o == '--help-rest':
        usage('rest')

    elif o == '--help-man':
        usage('man')

    elif o == '--help-desc':
        print __doc__,
        sys.exit(0)

    elif o in ('-i', '--interactive'):
        if mode_specified:
            log.error("You may only specify a single mode as a parameter (-i or -u).")
            sys.exit(1)

        mode = INTERACTIVE_MODE
        mode_specified = True

    elif o in ('-u', '--gui'):
        if mode_specified:
            log.error("You may only specify a single mode as a parameter (-i or -u).")
            sys.exit(1)

        mode = GUI_MODE
        mode_specified = True
        
    elif o in ('-q', '--lang'):
        if a.strip() == '?':
            utils.show_languages()
            sys.exit(0)
            
        loc = utils.validate_language(a.lower())        

utils.log_title(__title__, __version__)

# Security: Do *not* create files that other users can muck around with
os.umask(0037)

if mode == GUI_MODE:
    if not utils.canEnterGUIMode():
        mode = NON_INTERACTIVE_MODE

if mode == GUI_MODE:
    from qt import *
    from ui.faxaddrbookform import FaxAddrBookForm

    app = None
    addrbook = None
    # create the main application object
    app = QApplication(sys.argv)
    
    if loc is None:
        loc = user_cfg.ui.get("loc", "system")
        if loc.lower() == 'system':
            loc = str(QTextCodec.locale())
            log.debug("Using system locale: %s" % loc)

    if loc.lower() != 'c':
        log.debug("Trying to load .qm file for %s locale." % loc)
        trans = QTranslator(None)
        
        try:
            l, e = loc.split('.')
        except ValueError:
            l = loc
            e = 'utf8'
        
        qm_file = 'hplip_%s.qm' % l
        log.debug("Name of .qm file: %s" % qm_file)
        loaded = trans.load(qm_file, prop.localization_dir)
        
        if loaded:
            app.installTranslator(trans)
        else:
            loc = 'c'

    if loc == 'c':
        log.debug("Using default 'C' locale")
    else:
        log.debug("Using locale: %s" % loc)
        QLocale.setDefault(QLocale(loc))
        prop.locale = loc
        try:
            locale.setlocale(locale.LC_ALL, locale.normalize(loc))
        except locale.Error:
            pass

    addrbook = FaxAddrBookForm()
    addrbook.show()
    app.setMainWidget(addrbook)

    try:
        log.debug("Starting GUI loop...")
        app.exec_loop()
    except KeyboardInterrupt:
        pass

    sys.exit(0)

else: # INTERACTIVE_MODE
    try:
        from fax import fax
    except ImportError:
        # This can fail on Python < 2.3 due to the datetime module
        log.error("Fax address book disabled - Python 2.3+ required.")
        sys.exit(1)    

    console = Console()
    try:
        try:
            console.cmdloop()
        except KeyboardInterrupt:
            log.error("Aborted.")
    finally:
        pass
