###
## * << Haru Free PDF Library 2.0.0 >> -- raw_image_demo.c
## *
## * Copyright (c) 1999-2006 Takeshi Kanno <takeshi_kanno@est.hi-ho.ne.jp>
## *
## * Permission to use, copy, modify, distribute and sell this software
## * and its documentation for any purpose is hereby granted without fee,
## * provided that the above copyright notice appear in all copies and
## * that both that copyright notice and this permission notice appear
## * in supporting documentation.
## * It is provided "as is" without express or implied warranty.
## *
##

## port to python by Li Jun
## http://groups.google.com/group/pythoncia

import os, sys
from pathlib import Path

from ctypes import *

up = 2


def setlibpath(up):
    import sys

    path = os.path.normpath(os.path.split(os.path.realpath(__file__))[0] + "\.." * up)
    if path not in sys.path:
        sys.path.append(path)


setlibpath(up)

from haru import *
from haru.c_func import *
from haru.hpdf_errorcode import *


@HPDF_Error_Handler(None, HPDF_UINT, HPDF_UINT, c_void_p)
def error_handler(error_no, detail_no, user_data):
    global pdf
    printf("ERROR: %s, detail_no=%u\n", error_detail[error_no], detail_no)
    HPDF_Free(pdf)
    sys.exit(1)


RAW_IMAGE_DATA = [
    0xFF,
    0xFF,
    0xFF,
    0xFE,
    0xFF,
    0xFF,
    0xFF,
    0xFC,
    0xFF,
    0xFF,
    0xFF,
    0xF8,
    0xFF,
    0xFF,
    0xFF,
    0xF0,
    0xF3,
    0xF3,
    0xFF,
    0xE0,
    0xF3,
    0xF3,
    0xFF,
    0xC0,
    0xF3,
    0xF3,
    0xFF,
    0x80,
    0xF3,
    0x33,
    0xFF,
    0x00,
    0xF3,
    0x33,
    0xFE,
    0x00,
    0xF3,
    0x33,
    0xFC,
    0x00,
    0xF8,
    0x07,
    0xF8,
    0x00,
    0xF8,
    0x07,
    0xF0,
    0x00,
    0xFC,
    0xCF,
    0xE0,
    0x00,
    0xFC,
    0xCF,
    0xC0,
    0x00,
    0xFF,
    0xFF,
    0x80,
    0x00,
    0xFF,
    0xFF,
    0x00,
    0x00,
    0xFF,
    0xFE,
    0x00,
    0x00,
    0xFF,
    0xFC,
    0x00,
    0x00,
    0xFF,
    0xF8,
    0x0F,
    0xE0,
    0xFF,
    0xF0,
    0x0F,
    0xE0,
    0xFF,
    0xE0,
    0x0C,
    0x30,
    0xFF,
    0xC0,
    0x0C,
    0x30,
    0xFF,
    0x80,
    0x0F,
    0xE0,
    0xFF,
    0x00,
    0x0F,
    0xE0,
    0xFE,
    0x00,
    0x0C,
    0x30,
    0xFC,
    0x00,
    0x0C,
    0x30,
    0xF8,
    0x00,
    0x0F,
    0xE0,
    0xF0,
    0x00,
    0x0F,
    0xE0,
    0xE0,
    0x00,
    0x00,
    0x00,
    0xC0,
    0x00,
    0x00,
    0x00,
    0x80,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
]


def main():
    global pdf

    fname = os.path.realpath(sys.argv[0])
    fname = fname[: fname.rfind(".")] + ".pdf"

    pdf = HPDF_New(error_handler, NULL)
    if not pdf:
        printf("error: cannot create PdfDoc object\n")
        return 1

    HPDF_SetCompressionMode(pdf, HPDF_COMP_ALL)

    # create default-font
    font = HPDF_GetFont(pdf, "Helvetica", NULL)

    # add a new page object.
    page = HPDF_AddPage(pdf)

    HPDF_Page_SetWidth(page, 172)
    HPDF_Page_SetHeight(page, 80)

    HPDF_Page_BeginText(page)
    HPDF_Page_SetFontAndSize(page, font, 20)
    HPDF_Page_MoveTextPos(page, 220, HPDF_Page_GetHeight(page) - 70)
    HPDF_Page_ShowText(page, "RawImageDemo")
    HPDF_Page_EndText(page)

    # load RGB raw-image file.
    DATA_DIR = Path(__file__).parent.absolute()
    DATA_FILE = DATA_DIR / "rawimage/32_32_rgb.dat"
    image = HPDF_LoadRawImageFromFile(pdf, DATA_FILE, 32, 32, HPDF_CS_DEVICE_RGB)

    x = 20
    y = 20

    # Draw image to the canvas. (normal-mode with actual size.)
    HPDF_Page_DrawImage(page, image, x, y, 32, 32)

    # load GrayScale raw-image file.
    DATA_FILE = DATA_DIR / "rawimage/32_32_gray.dat"
    image = HPDF_LoadRawImageFromFile(pdf, DATA_FILE, 32, 32, HPDF_CS_DEVICE_GRAY)

    x = 70
    y = 20

    # Draw image to the canvas. (normal-mode with actual size.)
    HPDF_Page_DrawImage(page, image, x, y, 32, 32)

    # load GrayScale raw-image (1bit) file from memory.
    image = HPDF_LoadRawImageFromMem(
        pdf, RAW_IMAGE_DATA, 32, 32, HPDF_CS_DEVICE_GRAY, 1
    )

    x = 120
    y = 20

    # Draw image to the canvas. (normal-mode with actual size.)
    HPDF_Page_DrawImage(page, image, x, y, 32, 32)

    # save the document to a file
    HPDF_SaveToFile(pdf, fname)

    # clean up
    HPDF_Free(pdf)

    return 0


main()
