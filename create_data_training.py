
'''
by jeferson de souza

Script for get frames of mosaic image. Use opencv drawing functions and mouse event.

The origin's image is to big to show in the screen, so we get shunk of image and shift some pixel with keyboard comands

From that, we select a ROI and save with a double click button.

'''


import numpy as np
import cv2, os,sys

a,aa,b,bb =0,0,0,0

cordx = None
cordy = None
index = 0
data_cords = {} 


descriptor = None

if len(sys.argv) <=1:
	descriptor = cv2.ORB_create()
else:
	if sys.argv[1] =='orb':

		descriptor = cv2.ORB_create()
	elif sys.argv[1] == 'akase':
		descriptor = cv2.AKAZE_create()
	else:
		descriptor = cv2.ORB_create()


def open_window(name,img):
	try:
		cv2.namedWindow(name)
		cv2.resizeWindow(name, 300,300)
		cv2.moveWindow(name, 0,0)
		cv2.imshow(name, img)
	except:
		pass

def invert_coordenate(x,xx):

    if x < xx:
	a = x
	x = xx
	xx = a
    return x,xx

def retangulo(event, x,y , flags, param):

    global xx, yy, press, fract_img, aux, pattern1,pattern2,patternDefine, number_image, descriptor
    global a,aa,b,bb

    if event == cv2.EVENT_RBUTTONDOWN:

 	with open('coordenadas.json') as ddd:
		json.dump(data_cords,ddd)   							 	


    if event == cv2.EVENT_LBUTTONDOWN:
    	#print 'LBUTTON'
    	fract_img = np.copy(aux_puro)	
           
	xx,yy = x,y
    	press = True

    elif event == cv2.EVENT_MOUSEMOVE:
	
        if(press):
		
		fract_img = np.copy(aux)
            	cv2.rectangle(fract_img,(xx,yy),(x,y), (0,0,200), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        fract_img = np.copy(aux)
        cv2.rectangle(fract_img, (xx, yy), (x, y), (0, 0, 200), 2)
	
	if x < xx:
		s = x
		x = xx
		xx = s
	if y  < yy:
		s = y
		y = yy
		yy= s

	if(abs(x-xx)> 0 and abs(y-yy)> 0):
		if patternDefine:
		
        		pattern1 = cv2.cvtColor(fract_img[yy:y,xx:x],cv2.COLOR_BGR2GRAY)
        		open_window('pattern1',pattern1)
			patternDefine = False
			a,aa,b,bb = x,xx,y,yy	

		else:

			pattern2 = cv2.cvtColor(fract_img[yy:y,xx:x],cv2.COLOR_BGR2GRAY)
        		open_window('pattern2',pattern2)
			patternDefine = True
		print patternDefine

	number_image += 1
	xx, yy = 0, 0
	press = False

    elif event == cv2.EVENT_LBUTTONDBLCLK:
	#a = 0
	data_cords[index] = [a,aa,b,bb]
	index += 1
    	#cv2.imwrite('padroes_teste/'+str(a)+'_'+str(aa)+'_'+str(b)+'_'+str(bb)+'.jpg',pattern1)

    elif event == cv2.EVENT_RBUTTONDBLCLK:

	try:

		#descriptor = cv2.ORB_create()

		kp1 = descriptor.detect(pattern1, None)

		kp1, des1 = descriptor.compute(pattern1,kp1)

		kp2 = descriptor.detect(pattern2, None)

		kp2, des2 = descriptor.compute(pattern2,kp2)

		bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)

		matches = bf.match(des1,des2)

		matches = sorted(matches, key=lambda x:x.distance)

		#matchesMask = [[0,0] for i in xrange(len(matches))]
		
		#print 'MATHES', enumerate(matches)
		
		result = cv2.drawMatches(pattern1, kp1, pattern2, kp2, matches[:20],None,flags=2)

		#for pp, (m,n) in enumerate(matches):

		'''
		print matches, type(matches)
		for m in matches:
			print m.distance
		'''

		_lista = [m.distance  for m in matches if m.distance < 10]

		print _lista
		open_window('result',result)

	except Exception as e:

		print e.message
		pass

   


path_img = '../'#'/home/jeferson/Desktop/imagens_mosaico/' #'/home/jeferson/MEGA/IEAv/imagens_mosaico/'


#img = cv2.imread(path_img+ 'univap-final_transparent_mosaic_COM-APOIO.tif')

img = cv2.imread('../lena.jpg')

#asd = cv2.resize(img, (900,900))

#cv2.imwrite(path_im+'mosaico.png',asd)

#sys.exit()

number_image = int(len(os.listdir(path_img+'frames/')))

size = 900
shift = 100
fx = 0
fxx= size
fy = 0
fyy = size

press = False

fract_img = np.copy(img[fx:fxx,fy:fyy,:])

aux = np.copy(fract_img)

aux_puro = np.copy(fract_img)

pattern1, pattern2 = None, None

patternDefine = True

cv2.namedWindow('imagem')

cv2.setMouseCallback('imagem',retangulo)

while(1):
    
    change = False
    key = cv2.waitKey(1)
    if(key != -1):
	
        if(key == 119 or key == 82 ):
            #print 'cima'
            if(fx < size ):
                fx = 0
                fxx = size
            elif(fxx < shift):
                fxx = shift
            elif (fxx > shift and fx >= shift):
                fx -= shift
                fxx -= shift
	    change = True

        elif(key == 115 or key == 84):
            #print 'baixo'
            if(fxx + shift > img.shape[0]):
                fxx = img.shape[0]
            elif(fxx +shift <= img.shape[0]):
                fxx+= shift
                fx += shift
	    change = True

        elif (key == 97 or key == 81):
            #print 'esquerda'
            if(fy < size):
                fy = 0
                fyy = size
            elif(fyy <= shift):
                fyy = shift
            elif(fy - shift > 0 and fyy - shift >= shift):
                fyy -= shift
                fy -= shift
	    change = True

#int(shift/3)
        elif (key == 100 or key == 83):
            #print 'direita'
            if(fyy + shift + size > img.shape[1]):
                fyy = img.shape[1]
                fy = img.shape[1] -size
            elif(fyy + shift < img.shape[1] and fy + shift < img.shape[1]-shift):
                fyy+=shift
                fy+=shift
	    change = True

        #print 'CHAVEEEEE', key

        #print fx, fxx, fy, fyy

	if change:
		aux_puro = np.copy(img[fx:fxx, fy:fyy])
		
		fract_img = np.copy(img[fx:fxx, fy:fyy])

        	aux = np.copy(fract_img)	

	cv2.imshow('imagem',fract_img)

    if(key ==27):
        break



