

import exifread as ir

import cv2 

import numpy as np

tags = None
with open('../images/telhado2.jpg') as exread:
	tags = ir.process_file(exread)

print tags

for i in tags.keys():

	print i

print 'jaera'

print tags['EXIF MakerNote']

