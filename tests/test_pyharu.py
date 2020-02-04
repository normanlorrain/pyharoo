import pytest
import sys
from ctypes import *
from pathlib import Path

from pyharoo.haru import *
from pyharoo.haru.hpdf_errorcode import error_detail

TEST_DIR = Path(__file__).parent.absolute() / 'output'
TEST_DIR.mkdir(parents=True, exist_ok=True)


@HPDF_Error_Handler(None, HPDF_UINT, HPDF_UINT, c_void_p)
def error_handler (error_no, detail_no, user_data):
    print (f"ERROR: {error_detail[error_no]}, detail_no={detail_no}")
    return

error_handler = None


def test_emptyPDF():
    pdf = HPDF_New (error_handler, NULL)
    page_1 = HPDF_AddPage (pdf)
    outfilename = TEST_DIR/"test.pdf"
    res = HPDF_SaveToFile (pdf, outfilename)
    if res: 
        detail = HPDF_GetErrorDetail()
        print(detail)
        raise Exception( error_detail[res] )
    HPDF_Free (pdf)