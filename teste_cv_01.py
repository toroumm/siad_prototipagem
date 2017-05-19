import cv2
import numpy as np




#cap  = cv2.VideoCapture(0)

lena = cv2.imread('lena.jpg',0)

lena2x = cv2.resize(lena,None,fx=2,fy=2,interpolation = cv2.INTER_CUBIC)


cv2.namedWindow('img')
cv2.namedWindow('img2')
cv2.namedWindow('result')

orb = cv2.ORB_create()

kp1 = orb.detect(lena, None)

kp1, des1 = orb.compute(lena,kp1)

kp2 = orb.detect(lena2x, None)

kp2, des2 = orb.compute(lena2x,kp2)

bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)

matches = bf.match(des1,des2)

matches = sorted(matches, key=lambda x:x.distance)

result = cv2.drawMatches(lena, kp1, lena2x, kp2, matches[:20],None,flags=2)

lena = cv2.drawKeypoints(lena,kp1,None,color=(0,255,0),flags=0)

lena2x = cv2.drawKeypoints(lena2x,kp2,None,color=(0,255,0),flags=0)

cv2.imshow('img',lena)

cv2.imshow('img2',lena2x)

cv2.imshow('result',result)


while(1):
	key = cv2.waitKey(5)
	if key != 255:
		print key
"""
while(1):

	ret, frame =cap.read()

	print frame

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	cv2.imshow('img',gray)

	cv2.waitKey(0)

"""
