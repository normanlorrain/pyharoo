import pytest

from pathlib import Path

from pyharoo.haru import *

TEST_DIR = Path(__file__).parent.absolute() / 'output'
TEST_DIR.mkdir(parents=True, exist_ok=True)



def test_emptyPDF():
    error_handler = None 
    NULL = None
    pdf = HPDF_New (error_handler, NULL)
    page_1 = HPDF_AddPage (pdf)
    outfilename = bytes(TEST_DIR/"test.pdf")
    print(outfilename)
    HPDF_SaveToFile (pdf, outfilename)

    HPDF_Free (pdf)