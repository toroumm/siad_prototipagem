import numpy as np
import os, sys, subprocess
import cv2, io
import PIL.Image as pil
import random

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import Slider
import matplotlib.gridspec as gridspec

#from matplotlib.backends.backend_gtk import FigureCanvasGTK
 

'''
Formula temperatura

T = B / np.log(R1/(R2*(img+O))+F)

'''
def get_clusters(termal, img):

	mean, desvpad = np.mean(termal), np.std(termal)	

	img[termal <= (mean+desvpad) ] = 0

	return img

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
def mouse_event(event):

	#print  event.x, event.y
	global imgThermal
	
	print 'Temperatura',imgThermal[int(event.xdata),int(event.ydata)]



#*************************************************************************************************

def threshold(value):

	global imgSeg, figure, imgThermal, gs, legenda

	c = np.copy(imgSeg[:imgThermal.shape[0], :imgThermal.shape[1]])

	c[imgThermal <= int(value) ] = 0

	ax2 = figure.add_subplot(1,2,1)#gs[4:8])

	#ax2.set_position(gs[6:7].get_position(figure))

	ax2.set_title('Segmentado')

	ax2.axis('off')
		
	plt.imshow(imgSeg[:imgThermal.shape[0], :imgThermal.shape[1]])

	'''
	ax2 = figure.add_subplot(gs[0:6])

	ax2.set_position(gs[0:6].get_position(figure))

	ax2.set_title('Segmentado')

	ax2.axis('off')
		
	plt.imshow(imgSeg[:imgThermal.shape[0], :imgThermal.shape[1]])

	figure.tight_layout() 
	'''
	plt.imshow(c)
	
	figure.canvas.draw()

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

scope = range(0,100,10)

color = []

for i in range(len(scope)-1):

	color.append(tuple(next(next_color(COLORS))))

print color, len(color)

legenda = np.zeros(((len(scope)-1)*30,75,3))

k =0

imgOrignal, imgSeg,  = None, None

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

		imgSeg = np.zeros((imgThermal.shape[0], imgThermal.shape[1],3))

		for i in xrange(0, imgThermal.shape[0]):

			for j in xrange(0, imgThermal.shape[1]):

				for k in xrange(1, len(scope)-1):
					 
					if(imgThermal[i,j]>= scope[k-1] and imgThermal[i,j] < scope[k]):

						#if i > 450 and j > 300 and i < 480 and j < 320: 
						#	print k, scope[k-1],scope[k] , imgThermal[i,j], color[k] 
						imgSeg[i,j,0] = color[k-1][0]

						imgSeg[i,j,1] = color[k-1][1]

						imgSeg[i,j,2] = color[k-1][2]
						
						break
			
		figure  = plt.figure(figsize=(8,6)) 
		
		gs = gridspec.GridSpec(1,9)
		
		#****************************************************
		
		#ax1 =figure.add_subplot(121)#gs[:4])
		
		#ax1.set_position(gs[1:2].get_position(figure))

		#ax1.set_title('Original')

		#ax1.axis('off')

		imgOrignal = cv2.imread(path+arquivo)

		#plt.imshow(imgOrignal[:imgThermal.shape[0], :imgThermal.shape[1]])

		#****************************************************

		ax2 = figure.add_subplot(121)#gs[0:6])

		#ax2.set_position(gs[0:6].get_position(figure))

		ax2.set_title('Segmentado')

		ax2.axis('off')
		
		plt.imshow(imgSeg[:imgThermal.shape[0], :imgThermal.shape[1]])

		#figure.tight_layout() 

		#****************************************************

		ax3 = figure.add_subplot(1,7,6)#gs[7:9])

		#ax3.set_position(gs[7:9].get_position(figure))

		ax3.set_title('Legenda')

		ax3.axis('off')
		
		plt.imshow(legenda)

		#****************************************************

		figure2 = plt.figure()

		ax4  = figure2.add_subplot(1,1,1)

		ax4.set_title('Pontos Acima do Desvio Padrao')

		ax4.axis('off')

		plt.imshow(get_clusters(imgThermal,imgOrignal))
	
		figure.canvas.mpl_connect('button_press_event',mouse_event)

		ax = figure.add_axes([0.1, 0.85, 0.85, 0.1]) 

		trackbar = Slider(ax,'Filtro',0,100,1)

		trackbar.on_changed(threshold)	

		#print 'TAMANHO', plt.rcParams["figure.figsize"]
	  	
		plt.show()

		sys.exit()
#*************************************************************************************************







