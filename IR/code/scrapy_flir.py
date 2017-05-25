import numpy as np
import os, sys, subprocess
import cv2, io
import PIL.Image as pil
import random

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


'''
Formula temperatura

T = B / np.log(R1/(R2*(img+O))+F)

'''

def mouse_event(event):

	print  event.pickx, event.picky
#*************************************************************************************************

COLORS = [ (202, 201, 197),  # Light gray
			(171, 9, 0),      # Red
    			(166, 78, 46),    # Light orange
    			(255, 190, 67),   # Yellow
    			(163, 191, 63),   # Light green
    			(122, 159, 191),  # Li	ght blue
    			(140, 5, 84),     # Pink
    			(166, 133, 93),   # Light brown
    			(75, 64, 191),    # Red blue
    			(237, 124, 60),    # orange
		]

#*************************************************************************************************

def open_window(name,img):
	try:
		cv2.namedWindow(name)
		cv2.resizeWindow(name, 300,300)
		cv2.moveWindow(name, 0,0)
		cv2.imshow(name, img)
	except:
		pass

#*************************************************************************************************

def next_color(color_list):
		#Create a different color from a base color list.
		
		step = 20

		color = color_list[random.randint(0, len(color_list) - 1)]
		while True:
			#for color in color_list:

			yield map(lambda base: (base + step) % 256, color)

			step += 50

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

scope = range(0,100,30)

color = []

for i in range(len(scope)-1):

	color.append(tuple(next(next_color(COLORS))))

print color 

legenda = np.zeros(((len(scope)-1)*30,75,3))

k =0

font = cv2.FONT_HERSHEY_COMPLEX_SMALL
for i in range(0,legenda.shape[0],30):

	if k <= len(scope)-2:
	
		legenda[i:i+30,:,:] = color[k]

		cv2.putText(legenda,str(scope[k])+'-'+str(scope[k+1]),(2,i+20), font, 1, (0,0,0), 1, cv2.LINE_AA)

		k+=1

for arquivo in os.listdir(path):
	
	if arquivo.endswith(".jpg"):	
		
		param = get_parameters(path+arquivo)
		
		raw = get_rawData(path+arquivo)

		imgThermal =  get_temperature(param, raw)

		asd = np.zeros((imgThermal.shape[0], imgThermal.shape[1],3))

		for i in xrange(0, imgThermal.shape[0]):
			for j in xrange(0, imgThermal.shape[1]):
				for k in xrange(1, len(scope)-1):
					
					if(imgThermal[i,j]>= scope[k-1] and imgThermal[i,j] < scope[k]):
						asd[i,j,0] = color[k][0]

						asd[i,j,1] = color[k][1]

						asd[i,j,2] = color[k][2]
						
						break
						
		figure  = plt.figure()

		

		one = figure.add_subplot(1,3,1)

		one.set_title('Original')

		one.axis('off')

		one.canvas.mpl_connect('pick_event', mouse_event)	

		plt.imshow(cv2.imread(path+arquivo))

		two = figure.add_subplot(1,3,2)

		two.set_title('Segmentado')

		two.axis('off')
		
		plt.imshow(asd)

		tree = figure.add_subplot(1,3,3)

		tree.set_title('Legenda')

		tree.axis('off')

		plt.imshow(legenda)

		
			
		plt.show()

		sys.exit()
		#print np.max(imgThermal), np.min(imgThermal), np.mean(imgThermal)
		#open_window('teste',asd)
		#open_window('original',cv2.imread(path+arquivo))
		#cv2.imwrite(path+'testes/'+arquivo[:-3]+'_teste.jpg',asd)

		#cv2.waitKey(0)
#*************************************************************************************************







