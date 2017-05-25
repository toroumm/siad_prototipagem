import numpy as np
import os, sys, subprocess
import cv2, io
import PIL.Image as pil
import random

'''
Formula temperatura

T = B / np.log(R1/(R2*(img+O))+F)

'''
#

COLORS = [ (202, 201, 197),  # Light gray
			(171, 9, 0),      # Rede
    			(166, 78, 46),    # Light orange
    			(255, 190, 67),   # Yellow
    			(163, 191, 63),   # Light green
    			(122, 159, 191),  # Li	ght blue
    			(140, 5, 84),     # Pink
    			(166, 133, 93),   # Light brown
    			(75, 64, 191),    # Red blue
    			(237, 124, 60),    # orange
		]

def next_color(color_list):
		#Create a different color from a base color list.
		
		step = 1

		color = color_list[random.randint(0, len(color_list) - 1)]
		while True:
			#for color in color_list:

			yield map(lambda base: (base + step) % 256, color)

			step += 197


#*************************************************************************************************

def get_rawData(path_file):
	
	out = subprocess.check_output('exiftool -b -rawThermalImage '+path_file, shell=True)

	return  np.asarray(pil.open(io.BytesIO(out)))

#*************************************************************************************************

def get_parameters(path_file):

	_param = {}
	
	out = subprocess.check_output('exiftool -a -pl* '+path+ arquivo, shell = True)
		
	out = list(out.split())
		
	for i in xrange(0,len(out),4):		
		_param[out[i+1]] = out[i+3]
		
	return _param

#*************************************************************************************************

def get_temperature(param, data):

	return float(param['B']) / np.log(float(param['R1']) / ((float(param['R2']) * (data[:]+ float(param['O'])))) + float(param['F']))-273


#*************************************************************************************************

path = '../images/'#'/media/sf_ownCloud/visao_computacional/FLIR/imagens/'


for i in range(10):

	print tuple(next(next_color(COLORS)))


sys.exit()

for arquivo in os.listdir(path):
	
	if arquivo.endswith(".jpg"):	
		
		param = get_parameters(path+arquivo)
		
		raw = get_rawData(path+arquivo)

		imgThermal =  get_temperature(param, raw)

		print np.max(imgThermal), np.min(imgThermal), np.mean(imgThermal)

		
		






