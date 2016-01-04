/*****************************************************************************\
  LJZjStream.cpp : Implementation for the LJZjStream class

  Copyright (c) 1996 - 2009, Hewlett-Packard Co.
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

#include "CommonDefinitions.h"
#include "Pipeline.h"
#include "Encapsulator.h"
#include "ColorMatcher.h"
#include "Halftoner.h"
#include "ModeJbig.h"
#include "resources.h"
#include "ColorMaps.h"
#include "PrinterCommands.h"
#include "LJZjStream.h"
#include "Utils.h"
#include "hpjbig_wrapper.h"

#define ZJC_BAND_HEIGHT    100

LJZjStream::LJZjStream () : Encapsulator ()
{
    memset(&m_PM, 0, sizeof(m_PM));
    strcpy(m_szLanguage, "ZJS");
    m_pModeJbig = NULL;
    m_bNotSent = true;
}

LJZjStream::~LJZjStream()
{
}

DRIVER_ERROR LJZjStream::addJobSettings()
{
    BYTE    cItems[3] = {ZJI_DMCOLLATE, ZJI_PAGECOUNT, ZJI_DMDUPLEX};
    addToHeader("%s", "\x1B\x25-12345X@PJL ENTER LANGUAGE=ZJS\x0AJZJZ");
    BYTE    *p = cur_pcl_buffer_ptr;
    p[3] = 52;
    p[7] = ZJT_START_DOC;
    p[11] = 3;
    p[13] = 36;
    p[14] = 'Z';
    p[15] = 'Z';
    int    i = 16;
    for (int j = 0; j < 3; j++)
    {
        p[i + 3] = 12;
        p[i + 5] = cItems[j];
        p[i + 6] = ZJIT_UINT32;
        p[i + 11] = j / 2;
        i += 12;
    }
    cur_pcl_buffer_ptr += i;
    DRIVER_ERROR err = Cleanup();
    return err;
}

DRIVER_ERROR LJZjStream::Configure(Pipeline **pipeline)
{
    DRIVER_ERROR err;
    Pipeline    *p = NULL;
    Pipeline    *head;
    unsigned int width;
    ColorMatcher *pColorMatcher;
    Halftoner    *pHalftoner;
    int          iRows[MAXCOLORPLANES];
    unsigned int uiResBoost;
    head = *pipeline;

/*
 *  I need a flag in the printmode structure to whether create a CMYGraymap
 *  and set the ulMap1 to it.
 */

    m_PM.BaseResX = m_pQA->horizontal_resolution;
    m_PM.BaseResY = m_pQA->vertical_resolution;
    m_PM.eHT = FED;
    m_PM.MixedRes = false;
    m_PM.BlackFEDTable = HTBinary_open;
    if (m_pJA->color_mode == 0)
    {
        m_PM.cmap.ulMap1 = NULL;
        m_PM.cmap.ulMap2 = NULL;
        m_PM.cmap.ulMap3 = ucMapDJ4100_KCMY_Photo_BestA_12x12x1;
        m_PM.dyeCount = 4;
        m_PM.ColorFEDTable = HT1200x1200x1PhotoBest_open;
    }
    else
    {
        m_PM.cmap.ulMap1 = ulMapDJ600_CCM_K;
        m_PM.dyeCount = 1;
        m_PM.ColorFEDTable = HTBinary_open;
    }

    for (int i = 0; i < MAXCOLORPLANES; i++)
    {
        m_PM.ColorDepth[i] = 1;
        m_PM.ResolutionX[i] = m_pQA->horizontal_resolution;
        m_PM.ResolutionY[i] = m_pQA->vertical_resolution;
        iRows[i] = m_PM.ResolutionX[i] / m_PM.BaseResX;
    }

    uiResBoost = m_PM.BaseResX / m_PM.BaseResY;
    if (uiResBoost == 0)
        uiResBoost = 1;

    width = m_pMA->printable_width;

    pColorMatcher = new ColorMatcher(m_PM.cmap, m_PM.dyeCount, width);
    head = new Pipeline(pColorMatcher);
    pHalftoner = new Halftoner (&m_PM, width, iRows, uiResBoost, m_PM.eHT == MATRIX);
    p = new Pipeline(pHalftoner);
    head->AddPhase(p);
    m_pModeJbig = new ModeJbig(width);
    p = new Pipeline(m_pModeJbig);
    head->AddPhase(p);
    m_pModeJbig->myplane = COLORTYPE_COLOR;

    m_iPlanes = 1;
    m_iBpp = 1;
    int    height = m_pMA->printable_height;
    ZJPLATFORM    ezj_platform = ZJSTREAM;
    if (!strcmp(m_pJA->printer_platform, "ljzjscolor"))
    {
        m_iBpp = 2;
        ezj_platform = ZJCOLOR;
        if (m_pJA->color_mode == 0)
        {
            m_iPlanes = 4;
        }
        height = ZJC_BAND_HEIGHT;
    }
    err = m_pModeJbig->Init(height, m_iPlanes, m_iBpp, ezj_platform);

    *pipeline = head;
    return err;
}

DRIVER_ERROR LJZjStream::StartPage (JobAttributes *pJA)
{
    DRIVER_ERROR        err = NO_ERROR;
    DWORD               dwNumItems = 14;
    BYTE                szStr[16 + 15 * 12];
    int                 i;
    int                 width;

    m_iPlaneNumber = 0;
    m_iCurRaster   = 0;

    width = ((m_pMA->printable_width + 31) / 32) * 32;
    if (m_pJA->color_mode == 0)
        dwNumItems++;

    i = 0;
    i += SendChunkHeader (szStr, 16 + dwNumItems * 12, ZJT_START_PAGE, dwNumItems);
    if (m_pJA->color_mode == 0)
    {
        i += SendItem (szStr+i, ZJIT_UINT32, ZJI_PLANE, m_iPlanes);
    }

    i += SendItem (szStr+i, ZJIT_UINT32, ZJI_DMPAPER, m_pMA->pcl_id);
    i += SendItem (szStr+i, ZJIT_UINT32, ZJI_DMCOPIES, 1);
    i += SendItem (szStr+i, ZJIT_UINT32, ZJI_DMDEFAULTSOURCE, m_pJA->media_source);
    i += SendItem (szStr+i, ZJIT_UINT32, ZJI_DMMEDIATYPE, m_pQA->media_type);
    i += SendItem (szStr+i, ZJIT_UINT32, ZJI_NBIE, m_iPlanes);
    i += SendItem (szStr+i, ZJIT_UINT32, ZJI_RESOLUTION_X, m_pQA->horizontal_resolution);
    i += SendItem (szStr+i, ZJIT_UINT32, ZJI_RESOLUTION_Y, m_pQA->vertical_resolution);
    i += SendItem (szStr+i, ZJIT_UINT32, ZJI_RASTER_X, width * m_iBpp);
    i += SendItem (szStr+i, ZJIT_UINT32, ZJI_RASTER_Y, m_pMA->printable_height);
    i += SendItem (szStr+i, ZJIT_UINT32, ZJI_VIDEO_BPP, m_iBpp);
    i += SendItem (szStr+i, ZJIT_UINT32, ZJI_VIDEO_X, width);
    i += SendItem (szStr+i, ZJIT_UINT32, ZJI_VIDEO_Y, m_pMA->printable_height);
    i += SendItem (szStr+i, ZJIT_UINT32, ZJI_RET, RET_ON);
    i += SendItem (szStr+i, ZJIT_UINT32, ZJI_TONER_SAVE, (m_pQA->print_quality == -1) ? 1 : 0);

    err = sendBuffer ((const BYTE *) szStr, i);
    return err;
}

DRIVER_ERROR LJZjStream::sendBlankBands()
{
    if (strcmp(m_pJA->printer_platform, "ljzjscolor"))
    {
        return NO_ERROR;
    }
    DRIVER_ERROR    err = NO_ERROR;
    int    remaining_rasters = m_pMA->printable_height - m_iCurRaster;
    int    num_planes = (m_pJA->color_mode == 0) ? 4 : 1;
    if (remaining_rasters <= 0)
    {
        return NO_ERROR;
    }

    RASTERDATA    raster_data;
    if (remaining_rasters < ZJC_BAND_HEIGHT)
    {
        memset(&raster_data, 0, sizeof(raster_data));
        m_pModeJbig->SetBandHeight(remaining_rasters);
        for (int k = 0; k < num_planes; k++)
        {
            m_pModeJbig->Flush();
            m_pModeJbig->NextOutputRaster(raster_data);
            err = Encapsulate(&raster_data, true);
            if (err != NO_ERROR)
                return err;
        }
        m_pModeJbig->SetBandHeight(ZJC_BAND_HEIGHT);
        return err;
    }

    memset(&raster_data, 0, sizeof(raster_data));
    m_pModeJbig->Process(&raster_data);
    m_pModeJbig->Flush();
    m_pModeJbig->NextOutputRaster(raster_data);
    while (remaining_rasters > 0)
    {
        for (int k = 0; k < num_planes; k++)
        {
            err = Encapsulate(&raster_data, true);
            if (err != NO_ERROR)
            {
                return err;
            }
        }
        remaining_rasters -= ZJC_BAND_HEIGHT;
    }
    if (remaining_rasters <= 0)
    {
        return NO_ERROR;
    }

    memset(&raster_data, 0, sizeof(raster_data));
    m_pModeJbig->SetBandHeight(remaining_rasters);
    m_pModeJbig->Process(&raster_data);
    m_pModeJbig->Flush();
    m_pModeJbig->NextOutputRaster(raster_data);
    for (int k = 0; k < num_planes; k++)
    {
        err = Encapsulate(&raster_data, true);
    }
    m_pModeJbig->SetBandHeight(ZJC_BAND_HEIGHT);

    return err;
}

DRIVER_ERROR LJZjStream::FormFeed ()
{
    DRIVER_ERROR        err = NO_ERROR;
    BYTE                szStr[128];
    int                 size = 16;

    err = sendBlankBands();
    if (err != NO_ERROR)
        return err;

    SendChunkHeader (szStr, 16, ZJT_END_PAGE, 0);
    if (!strcmp(m_pJA->printer_platform, "ljzjscolor"))
    {
        int                 i = 0;
        int                 iCol = (m_pJA->color_mode == 0) ? 1 : 0;

        memset(szStr, 0, sizeof(szStr));
        i = SendChunkHeader (szStr, 112, ZJT_END_PAGE, 8);
        for (int j = 0; j < 8; j++)
        {
            i += SendItem (szStr+i, ZJIT_UINT32, 0x8200+j, (j % 4 == 3) ? 1 : iCol);
        }
        size = 112;
    }

    err = sendBuffer ((const BYTE *) szStr, size);

    return err;
}

DRIVER_ERROR LJZjStream::EndJob()
{
    BYTE    szStr[16];
    memset(szStr, 0, sizeof(szStr));
    szStr[3] = 16;
    szStr[7] = ZJT_END_DOC;
    szStr[14] = 'Z';
    szStr[15] = 'Z';
    return this->sendBuffer((const BYTE *) szStr, 16);
}

DRIVER_ERROR    LJZjStream::Encapsulate (RASTERDATA *raster, bool bLastPlane)
{
if (raster->rasterdata[COLORTYPE_COLOR] == NULL || raster->rastersize[COLORTYPE_COLOR] == 0)
{
    return NO_ERROR;
}
    if (!strcmp(m_pJA->printer_platform, "ljzjscolor"))
    {
        return encapsulateColor(raster);
    }

    DRIVER_ERROR        err = NO_ERROR;
    BYTE                szStr[36];
    int                 i = 0;
    int                 iTotalSize = raster->rastersize[COLORTYPE_COLOR];

/*
 *  Send JBIG header info
 */

    i = SendChunkHeader (szStr, 36, ZJT_JBIG_BIH, 0);

    memcpy (szStr + 16, raster->rasterdata[COLORTYPE_COLOR], 20);
    err = sendBuffer ((const BYTE *) szStr, 36);
    ERRCHECK;

    iTotalSize -= 20;
    int     iPadCount = 0;
    if (iTotalSize % 16)
    {
        iPadCount = ((iTotalSize / 16 + 1) * 16) - iTotalSize;
    }
    int      dwTotal = iTotalSize;
    BYTE     *p = raster->rasterdata[COLORTYPE_COLOR] + 20;
    i = dwTotal / 65536;

    for (int j = 0; j < i; j++)
    {
        SendChunkHeader (szStr, 16 + 65536, ZJT_JBIG_HID, 0);
        err = sendBuffer ((const BYTE *) szStr, 16);
        ERRCHECK;
        err = sendBuffer ((const BYTE *) p, 65536);
        ERRCHECK;
        dwTotal -= 65536;
        p += 65536;
    }
    i = SendChunkHeader (szStr, 16 + dwTotal + iPadCount, ZJT_JBIG_HID, 0);
    err = sendBuffer ((const BYTE *) szStr, 16);
    ERRCHECK;
    err = sendBuffer ((const BYTE *) p, dwTotal);
    ERRCHECK;
    if (iPadCount != 0)
    {
        memset (szStr, 0, iPadCount);
        err = sendBuffer ((const BYTE *) szStr, iPadCount);
    }
    i = SendChunkHeader (szStr, 16, ZJT_END_JBIG, 0);
    if (err == NO_ERROR)
        err = sendBuffer ((const BYTE *) szStr, 16);
    err = Cleanup();
    return err;
}

DRIVER_ERROR    LJZjStream::encapsulateColor (RASTERDATA *raster)
{
    bool            bLastStride = true;
    int             kEnd = 2;
    DRIVER_ERROR    err = NO_ERROR;
    BYTE            szStr[256];
    int             i = 0;

    HPLJZjsJbgEncSt     *se = (HPLJZjsJbgEncSt *) (raster->rasterdata[COLORTYPE_COLOR] + raster->rastersize[COLORTYPE_COLOR]);

    if (m_pJA->color_mode == 0)
    {
        kEnd = 5;
    }
    if (m_iPlaneNumber == 0 || m_pJA->color_mode != 0)
        m_iCurRaster += se->yd;
    if (m_iCurRaster < m_pMA->printable_height)
    {
        bLastStride = false;
    }


/*
 *  Send JBIG header info
 */

    // Send out the JBIG header if first plane and it hasn't already been sent out yet.
    if (m_iPlaneNumber == 0 && m_bNotSent)
    {
        m_bNotSent = false;
        i = 0;
        for (int k = 1; k < kEnd; k++)
        {
            i = SendChunkHeader (szStr, 132, ZJT_BITMAP, 8);
            szStr[13] += 20;
            i += SendItem (szStr+i, ZJIT_UINT32, ZJI_BITMAP_TYPE, 1);
            i += SendItem (szStr+i, ZJIT_UINT32, ZJI_BITMAP_PIXELS, se->xd);
            i += SendItem (szStr+i, ZJIT_UINT32, ZJI_BITMAP_STRIDE, se->xd);
            i += SendItem (szStr+i, ZJIT_UINT32, ZJI_BITMAP_LINES, se->yd);
            i += SendItem (szStr+i, ZJIT_UINT32, ZJI_BITMAP_BPP, 1);
            i += SendItem (szStr+i, ZJIT_UINT32, ZJI_VIDEO_BPP, m_iBpp);
            i += SendItem (szStr+i, ZJIT_UINT32, ZJI_PLANE,
                           (m_pJA->color_mode == 0) ? k : 4);
            i += SendItemExtra (szStr+i, ZJIT_BYTELUT, ZJI_ENCODING_DATA, 20, 20);
            szStr[i++] = se->dl;
            szStr[i++] = se->d;
            szStr[i++] = se->planes;
            szStr[i++] = 0;
            for (int j = 3; j >= 0; j--)
            {
                szStr[i] = (BYTE) ((se->xd  >> (8 * j)) & 0xFF);
                szStr[4+i] = (BYTE) ((se->yd  >> (8 * j)) & 0xFF);
                szStr[8+i] = (BYTE) ((se->l0  >> (8 * j)) & 0xFF);
                i++;
            }
            i += 8;

            szStr[i++] = se->mx;
            szStr[i++] = se->my;
            szStr[i++] = se->order;
            szStr[i++] = se->options;
            err = sendBuffer ((const BYTE *) szStr, 132);
            ERRCHECK;
        }
    }

    BYTE    *p = raster->rasterdata[COLORTYPE_COLOR] + 20;
    int     dwNumItems;
    int     dwSize;

    DWORD    dwTotalSize = raster->rastersize[COLORTYPE_COLOR];
    dwTotalSize -= 20;
    int     iPadCount = 0;

    i = 0;
    if (dwTotalSize % 4)
    {
        iPadCount = ((dwTotalSize / 4 + 1) * 4) - dwTotalSize;
    }

    dwSize = 16 + dwTotalSize + iPadCount;
    dwNumItems = 1;
    if (bLastStride)
    {
        dwNumItems = 3;
        m_bNotSent = true;
    }
    dwSize += (dwNumItems * 12);
    i = SendChunkHeader (szStr, dwSize, ZJT_BITMAP, dwNumItems);
    i += SendItem (szStr+i, ZJIT_UINT32, ZJI_PLANE, (kEnd == 5) ? m_iPlaneNumber+1 : 4);
    if (bLastStride)
    {
        i += SendItem (szStr+i, ZJIT_UINT32, ZJI_BITMAP_LINES, se->yd);
        i += SendItem (szStr+i, ZJIT_UINT32, ZJI_END_PLANE, bLastStride);
    }
    err = sendBuffer ((const BYTE *) szStr, i);
    ERRCHECK;

    err = sendBuffer ((const BYTE *) p, dwTotalSize);
    ERRCHECK;
    if (iPadCount != 0)
    {
        memset (szStr, 0, iPadCount);
        err = sendBuffer ((const BYTE *) szStr, iPadCount);
    }

    if (m_pJA->color_mode == 0)
    {
        m_iPlaneNumber++;
        if (m_iPlaneNumber == 4)
        {
            m_iPlaneNumber = 0;
        }
    }
    return err;
}

