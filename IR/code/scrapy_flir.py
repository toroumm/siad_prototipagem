import numpy as np
import os, sys, subprocess
import cv2, io
import PIL.Image as pil


'''
Formula temperatura

T = B / np.log(R1/(R2*(img+O))+F)

'''
#



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
		#print i, _param[out[i+1]]
	print 'OUTPUT', out
	return _param


#*************************************************************************************************

def get_temperature(param, data):

	return float(param['B']) / np.log(float(param['R1']) / ((float(param['R2']) * (data[:]+ float(param['O'])))) + float(param['F']))


#*************************************************************************************************

path = '/media/sf_ownCloud/visao_computacional/FLIR/imagens/'


for arquivo in os.listdir(path):
	
	if arquivo.endswith(".jpg"):	
		print get_rawData(path+arquivo)[1,1]
		print get_temperature(get_parameters(path+arquivo), get_rawData(path+arquivo))[1,1]
		print get_parameters(path + arquivo)

		break
		#out = subprocess.check_output('exiftool -a -pl* '+path+ arquivo, shell = True)
		
		#out = list(out.split())
			
		#img_thermo = subprocess.check_output('exiftool -b -rawThermalImage '+path+ arquivo, shell = True)

		#print img_thermo

		#sys.exit()			
		
		#for i in xrange(0,len(out),4):		
		#	_param[out[i+1]] = out[i+3]
		#	print i, _param[out[i+1]]
		#break






