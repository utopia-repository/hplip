/*****************************************************************************\
  dj8x5.cpp : Implimentation for the DJ8x5 class

  Copyright (c) 1996 - 2001, Hewlett-Packard Co.
  All rights reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions
  are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.
  3. Neither the name of Hewlett-Packard nor the names of its
     contributors may be used to endorse or promote products derived
     from this software without specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED
  WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN
  NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
  TO, PATENT INFRINGEMENT; PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
  OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
  ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
  THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
\*****************************************************************************/


#if defined(APDK_DJ8xx)|| defined(APDK_DJ9xx)

#ifdef APDK_DJ8x5
#include "header.h"
#include "dj8xx.h"
#include "dj8x5.h"
#include "printerproxy.h"

APDK_BEGIN_NAMESPACE            // must be here for non-test harness case
extern BYTE* GetHT3x3_4();
extern BYTE* GetHT6x6_4();
APDK_END_NAMESPACE              // must be here for non-test harness case

APDK_BEGIN_NAMESPACE

extern uint32_t ulMapVOLTAIRE_CCM_K[ 9 * 9 * 9 ];
extern uint32_t ulMapPhobosPlainNormal[ 9 * 9 * 9 ];
extern uint32_t ulMapVENICE_HB_KCMY[ 9 * 9 * 9 ];
extern uint32_t ulMapPhobosDraft[ 9 * 9 * 9 ];


PhobosMode1::PhobosMode1()
: PrintMode(ulMapPhobosPlainNormal)
// 600x600x1 K
// 300x300x2 CMY
{

    ColorDepth[K]=1;  // 600x600x1 K

    for (int i=1; i < 4; i++)
        ColorDepth[i]=2;    // 300x300x2 CMY

    ResolutionX[K] =
    ResolutionY[K] = 600;

    MixedRes = TRUE;

    ColorFEDTable = GetHT3x3_4();

    bFontCapable = FALSE;       // Venice can't do fonts and hifipe at same time
    dyeCount = 3;
    CompatiblePens[0] = COLOR_PEN;
}

PhobosMode2::PhobosMode2()
: PrintMode(ulMapVENICE_HB_KCMY)
// 600x600x2 CMY
{
    int i;
    ColorDepth[K]=1;  // 600x600x1 K

    for (i=1; i < 4; i++)
        ColorDepth[i]=2;    // 600x600x2 CMY

    for (i=0; i < 4; i++)
        ResolutionX[i]=ResolutionY[i]=600;

    BaseResX = BaseResY = 600;
    MixedRes = FALSE;

    medium     = mediaGlossy;
    theQuality = qualityPresentation;

    ColorFEDTable = GetHT6x6_4();

     bFontCapable = FALSE;       // Venice can't do fonts and hifipe at same time

    dyeCount = 3;
    CompatiblePens[0] = COLOR_PEN;

    pmQuality   = QUALITY_BEST;
    pmMediaType = MEDIA_PHOTO;
}

PhobosMode3::PhobosMode3()
: PrintMode(ulMapPhobosDraft)
// 300x300x1 CMY
{

    dyeCount = 3;
    CompatiblePens[0] = COLOR_PEN;
    theQuality = qualityDraft;
    pmQuality  = QUALITY_DRAFT;
}

// Moved this mode to the Venice base class (8xx). des
/*
PhobosMode4::PhobosMode4 ()
    : PrintMode(ulMapVOLTAIRE_CCM_K)
// grayscale uses econo, 300, 1 bit
{
    ColorDepth[K] = 1;
    dyeCount = 1;
    CompatiblePens[0] = BLACK_PEN;
    theQuality = qualityDraft;
//    strcpy(ModeName,"Draft-Grayscale");
    pmQuality = QUALITY_DRAFT;
}
*/

// this mode not needed; system creates it automatically
// removed it because modeset should not depend on penss
/*
PhobosMode5::PhobosMode5 ()
    : PrintMode(ulMapPhobosDraft)
// grayscale uses color pen, 300
{
    dyeCount = 1;
    CompatiblePens[0] = COLOR_PEN;
//    strcpy(ModeName,"Grayscale");
    pmColor=GREY_CMY;
}
*/

DJ8x5::DJ8x5 (SystemServices* pSS, int numfonts, BOOL proto)
    : DJ8xx (pSS, numfonts, TRUE)
{
    CMYMap = ulMapPhobosDraft;

/*
 *  If we don't have device id, we won't know about the pens installed.
 *  But since both 825 and 845 ship with atleast a colorpen, we will
 *  default to COLOR_PEN, so it will work okay out of the box.
 */

    if ((!proto) && (IOMode.bDevID))
    {
        constructor_error = VerifyPenInfo();
        CERRCHECK;
    }
    else
    {
        ePen = COLOR_PEN;
    }

// Venice modes based on BOTH_PENS are already installed (i.e. pModes 0-4)

    pMode[5]    = new PhobosMode1 ();    // Normal Color CMY
    pMode[6]    = new PhobosMode2 ();    // Photo CMY
    pMode[7]    = new PhobosMode3 ();    // Draft Color CMY
    ModeCount = 8;

    DBG1("DJ8x5 created\n");
}

PEN_TYPE DJ8x5::DefaultPenSet()
{
    return COLOR_PEN;
}

DRIVER_ERROR DJ8x5::VerifyPenInfo ()
{

    DRIVER_ERROR err=NO_ERROR;

    if(IOMode.bDevID == FALSE)
        return err;

    err = ParsePenInfo (ePen);

    if(err == UNSUPPORTED_PEN) // probably Power Off - pens couldn't be read
    {
        DBG1("DJ8x5::Need to do a POWER ON to get penIDs\n");

        // have to delay for Broadway or the POWER ON will be ignored
        if (pSS->BusyWait((DWORD)2000) == JOB_CANCELED)
            return JOB_CANCELED;

        DWORD length=sizeof (Venice_Power_On);
        err = pSS->ToDevice (Venice_Power_On, &length);
        ERRCHECK;

        err = pSS->FlushIO ();
        ERRCHECK;

        // give the printer some time to power up
        if (pSS->BusyWait ((DWORD) 2500) == JOB_CANCELED)
            return JOB_CANCELED;

        err = ParsePenInfo(ePen);
    }

    ERRCHECK;

    // check for the normal case
    if (ePen == BOTH_PENS)
        return NO_ERROR;

    while (ePen == NO_PEN)
    {
        pSS->DisplayPrinterStatus(DISPLAY_NO_PENS);

        if (pSS->BusyWait(500) == JOB_CANCELED)
            return JOB_CANCELED;

        err =  ParsePenInfo(ePen);
        ERRCHECK;
    }

    pSS->DisplayPrinterStatus(DISPLAY_PRINTING);

    return NO_ERROR;
}

APDK_END_NAMESPACE

#endif // APDK_DJ8x5
#endif  // APDK_DJ895
