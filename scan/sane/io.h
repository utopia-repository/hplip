/************************************************************************************\

  io.h - HP SANE backend for multi-function peripherals (libsane-hpaio)

  (c) 2001-2006 Copyright Hewlett-Packard Development Company, LP

  Permission is hereby granted, free of charge, to any person obtaining a copy 
  of this software and associated documentation files (the "Software"), to deal 
  in the Software without restriction, including without limitation the rights 
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
  of the Software, and to permit persons to whom the Software is furnished to do 
  so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS 
  FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
  IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

  Contributing Author: Don Welch, David Suffield 

\************************************************************************************/

#if !defined(_IO_H)
#define _IO_H

#include "sane.h"
#include "hpmud.h"

int __attribute__ ((visibility ("hidden"))) SendScanEvent(char * device_uri, int event, char * type);
int __attribute__ ((visibility ("hidden"))) ReadChannelEx(int deviceid, int channelid, unsigned char * buffer, int length, int timeout);

#endif


