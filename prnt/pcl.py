#!/usr/bin/env python
#
# $Revision: 1.8 $ 
# $Date: 2005/09/06 22:42:22 $
# $Author: dwelch $
#
# (c) Copyright 2003-2004 Hewlett-Packard Development Company, L.P.
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


import struct
from base import pml

ESC = '\x1b'
RESET = '\x1bE'
UEL = '\x1b%-12345X'
PJL_ENTER_LANG = "@PJL ENTER LANGUAGE=PCL3GUI\n"
PJL_BEGIN_JOB = '@PJL JOB NAME="unnamed"\n'
PJL_END_JOB = '@PJL EOJ\n'

def buildPCLCmd( punc, letter1, letter2, data=None, value=None ):
    if data is None:
        return ''.join( [ ESC, punc, letter1, str(value), letter2 ] )
        
    return ''.join( [ ESC, punc, letter1, str(len(data)), letter2, data ] )


def buildEmbeddedPML( pml ):
    return ''.join( [ UEL, PJL_ENTER_LANG, RESET, pml, RESET, UEL ] )
    

## """\x1bE\x1b%-12345X@PJL JOB NAME="unnamed"\n@PJL ENTER LANGUAGE=PCL3GUI\n\x1bE\x1b&b15WPML \x04\x00\x04\x01\x01\x05\x02\x04\x02\x04N\x1bE\x1b%-12345X@PJL EOJ\n\x1b%-12345X"""
##   '\x1bE\x1b%-12345X@PJL JOB NAME="unnamed"\n@PJL ENTER LANGUAGE=PCL3GUI\n\x1bE\x1b&b15WPML \x04\x00\x04\x01\x01\x05\x02\x04\x02\x01\x03\x1bE\x1b%-12345X@PJL EOJ\n\x1b%-12345X'

def buildEmbeddedPML2( pml ):
    return ''.join( [ RESET, UEL, PJL_BEGIN_JOB, PJL_ENTER_LANG, RESET, pml, RESET, PJL_END_JOB, RESET, UEL ] )


def buildDynamicCounter( counter ):
    return ''.join( [ UEL, PJL_ENTER_LANG, ESC, '*o5W\xc0\x01', struct.pack( ">I", counter )[1:], UEL ] )
    
    
def buildRP( a, b, c, d, e ):
    return ''.join( [ '\x00'*600, RESET, UEL, PJL_ENTER_LANG, buildPCLCmd( '&', 'b', 'W', pml.buildEmbeddedPMLSetPacket( '1.1.1.36', a + b + c + d + e, pml.TYPE_STRING ) ), RESET, UEL ] )
