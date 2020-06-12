#!/usr/bin/env python
import sys
import os
from PyPDF2 import PdfFileReader, PdfFileMerger
def merger(book_name):
	merger = PdfFileMerger()
	files = os.listdir('flaskps/static/uploads/'+book_name)
	files.sort()
	#files = os.listdir('flaskps/static/uploads/'+book_name)
	print(files)
	for f in files:
		merger.append(PdfFileReader('flaskps/static/uploads/'+book_name+'/'+f, 'rb'))
	merger.write('flaskps/static/uploads/'+book_name+'/'+book_name+"_Full.pdf")
