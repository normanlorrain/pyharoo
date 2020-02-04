from pyharoo.haru import *



error_handler = None 
NULL = None
pdf = HPDF_New (error_handler, NULL)
page_1 = HPDF_AddPage (pdf)

HPDF_SaveToFile (pdf, r"test.pdf")

HPDF_Free (pdf)