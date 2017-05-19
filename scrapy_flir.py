import numpy as np

import os, sys, subprocess

import cv2

path = '/media/sf_ownCloud/visao_computacional/FLIR/imagens/'

#a = os.system('exiftool -r -createDate '+path)


_param = {}

img_thermo = 0

for arquivo in os.listdir(path):
	
	if arquivo.endswith(".jpg"):	
		out = subprocess.check_output('exiftool -a -pl* '+path+ arquivo, shell = True)
		
		out = list(out.split())
			
		#img_thermo = subprocess.check_output('exiftool -b -rawThermalImage '+path+ arquivo, shell = True)

		#print img_thermo

		#sys.exit()			
		
		for i in xrange(0,len(out),4):		
			_param[out[i+1]] = out[i+3]
		break



img = cv2.imread(img_thermo)

print img.shape

cv2.namedWindow('image')

cv2.imshow('image',img)

cv2.waitKey(0)


