#!/usr/bin/env python
# -*- coding: utf-8 -*-


import cv2
import numpy as np
import os, sys
import json,pickle

def open_window(name,img):
	try:
		cv2.namedWindow(name)
		cv2.resizeWindow(name, 300,300)
		cv2.moveWindow(name, 0,0)
		cv2.imshow(name, img)
	except:
		pass


beginx = 0
beginy = 0
size = 1000
shiftx = 100
shifty = 600

dir_name = 'resultado_win_'+str(size)+'_shiftx_'+str(shiftx)+'_shifty_'+str(shifty)


list_points = [5,10,15,20,25,30]

dirs = os.listdir('compare_img/')

if dir_name not in dirs:

	os.mkdir('compare_img/'+dir_name)
	for i in list_points:
		os.mkdir('compare_img/'+dir_name+'/'+'points_'+str(i))

img1 = cv2.imread('base_img/mosaico.tif')

img2 = cv2.imread('base_img/mosaico_modificado.tif')

cv2.imwrite('mosaico_modificado_resize.png', img2)

cv2.imwrite('mosaico_resize.png', img1)

sys.exit()

width = img1.shape[0]

height = img1.shape[1]

descriptor = cv2.ORB_create()
 

fx = beginx
fxx = beginx + size
fy = beginy
fyy = beginy + size

line = False
column = False

frac1 = np.copy(img1[fy:fyy, fx:fxx])

frac2 = np.copy(img2[fy:fyy, fx:fxx])

bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)

fourcc = cv2.VideoWriter_fourcc(*'XVID')

out = cv2.VideoWriter('resultado_win_'+str(size)+'_shiftx_'+str(shiftx)+'_shifty_'+str(shifty)+'.avi',fourcc, 20.0, (size,size))


while(1):
	

	kp1 = descriptor.detect(frac1, None)

	kp1, des1 = descriptor.compute(frac1,kp1)

	kp2 = descriptor.detect(frac2, None)

	kp2, des2 = descriptor.compute(frac2,kp2)

	match = bf.match(des1,des2)

	match = sorted(match, key=lambda x:x.distance)

	points = len([m.distance for m in match if m.distance < 5])
	cir = False
	for p in list_points:
		if points <= p and points > 0:
			if p <= 15:
				cir = True
			cv2.imwrite('compare_img/'+dir_name+'/'+'points_'+str(p)+'/'+str(fy)+'_'+str(fyy)+'_'+str(fx)+'_'+str(fxx)+'_'+str(p)+'.png', np.concatenate((frac1,frac2), axis=1))
	if cir == True:
				
		for c in xrange(10,100,10):		
			cv2.circle(frac2,(int(size/2),int(size/2)),c,(0,0,255),2)

		
	result = cv2.drawMatches(frac1, kp1, frac2, kp2, match[:20],None,flags=2)

	print points, len(match)

	result = cv2.resize(result,(size,size))

	out.write(result)
	

	if(line):

		fx = beginx
		fxx = beginx+size
		line = False
	if(column):
		break

	if fxx < img1.shape[1]:
		fx += shiftx
		fxx += shiftx
	else:
		fx = img1.shape[1]-shiftx
		fxx = img1.shape[1]-beginx
		line = True
			
		if fyy < img1.shape[0]:
			fyy += shifty
			fy +=shifty
		else:
			fy = img1.shape[0]-shifty
			fyy = img1.shape[0]
			column = True

	frac1 = np.copy(img1[fy:fyy, fx:fxx])

	frac2 = np.copy(img2[fy:fyy, fx:fxx])

	open_window('resultado',result)

	cv2.waitKey(5)


	
