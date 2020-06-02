#!/usr/bin/env python
import sys
import os
from PyPDF2 import PdfFileReader, PdfFileMerger
def merger():
	merger = PdfFileMerger()
	files = os.listdir(sys.argv[1])
	print(len(files))
	for cap_num in range(1,len(files)+1):
		merger.append(PdfFileReader(sys.argv[1]+'/'+str(cap_num)+".pdf", 'rb'))
	merger.write("merged.pdf")
