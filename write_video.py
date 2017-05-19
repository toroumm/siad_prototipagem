#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2, os,sys, json, pickle


#with open('data.json', 'r') as fp:
#    data = json.load(fp)

begin = 2000
size = 100
shift = 25
shiftx = 25
shifty = 600
def open_window(name,img):
	try:
		cv2.namedWindow(name)
		cv2.resizeWindow(name, 300,300)
		cv2.moveWindow(name, 0,0)
		cv2.imshow(name, img)
	except:
		pass

def write_video():

	

	size = 1000
	shift = 50
	fx = begin
	fxx= begin+size
	fy = begin
	fyy = begin+size

	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter('mosaico_win_'+str(size)+'_shiftx_'+str(shiftx)+'_shifty_'+str(shifty)+'.avi',fourcc, 20.0, (size,size))
	img = cv2.imread('univap-final_transparent_mosaic_COM-APOIO.tif')
	#img = cv2.imread('lena.jpg')
	fract_img = np.copy(img[fx:fxx, fy:fyy])

	line = False
	column = False

	out.write(fract_img)

	orb = cv2.ORB_create()

	data = {}

	while(1):

		kp1 = orb.detect(fract_img, None)

		kp1, des1 = orb.compute(fract_img,kp1)

		#if des1 is not None :
		
		#	data[str(fx)+'_'+str(fxx)+'_'+str(fy)+'_'+str(fyy)] = {'des':des1, 'fx':fx,'fxx':fxx,'fy':fy,'fyy':fyy}
		#	print str(fx)+'_'+str(fxx)+'_'+str(fy)+'_'+str(fyy)
		#else:
		#	print des1, kp1 
		#print fx,fxx,fy,fyy

		if(line):
			fx = begin
			fxx = begin+size
			line = False
		if(column):
			break

		if fxx < img.shape[1]-begin:
			fx += shiftx
			fxx += shiftx
		else:
			fx = img.shape[1]-shiftx-begin
			fxx = img.shape[1]-begin
			line = True
			
			if fyy < img.shape[0]-begin:
				fyy += shifty
				fy +=shifty
			else:
				fy = img.shape[0]-shifty-begin
				fyy = img.shape[0]-begin
				column = True
	
		fract_img = np.copy(img[fy:fyy, fx:fxx])

		out.write(fract_img)
		
		open_window('video',fract_img)

		cv2.waitKey(5)

'''

	with open('json_data/mosaico_features_size_'+str(size)+'_shift_'+str(shift)+'.pk1', 'wb') as handle:
    		pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
'''


'''
	with open('json_data/mosaico_features_size_'+str(size)+'_shift_'+str(shift)+'.json', 'w') as fp:
		json.dump(data, fp)

'''

write_video()

#with open('json_data/mosaico_features_size_'+str(size)+'_shift_'+str(shift)+'.pk1', 'rb') as handle:
#	t =pickle.load(handle)

#print t



print 'acabou'
	    
