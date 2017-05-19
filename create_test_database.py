#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2, os,sys, json,pickle



_files = os.listdir('padroes_teste/')

path = 'padroes_teste_modificados/'

size = [0.25,0.5,2,4]

smoth = [3,5,7,11]

orb = cv2.ORB_create()

data_json = {}

#with open(path+'database_test.pk1', 'rb') 	as handle:
#	t =pickle.load(handle)


for f in _files:
	
	name = f[:-4]
	
	original = cv2.imread('padroes_teste/'+f,0)
	#imagem original
	
	img = np.copy(original)
		
	kp = orb.detect(img, None)

	kp,des = orb.compute(img,kp)

	data_json[name] = {'des':des}

	cv2.imwrite(path+name+'.jpg',img)

	print original.shape, f
	#rot
	for ii in xrange(15,345,30):
		
		#img original dividida por 3 rotacionada
		M = cv2.getRotationMatrix2D((img.shape[0]/3,img.shape[1]/3),ii,1)
		
		img1 = cv2.warpAffine(img,M,(img.shape[0],img.shape[1]))
		
		kp1 = orb.detect(img1,None)

		kp1, des1 = orb.compute(img1, kp1)

		data_json[name+'_rot_'+str(ii)] = {'des':des1}

		cv2.imwrite(path+name+'_rot_'+str(ii)+'.jpg', img1)
	
		#esc
		for jj in size:

			#imagem original escalada
			img2_1 = cv2.resize(img,(int(jj*img.shape[0]), int(jj*img.shape[1])), interpolation = cv2.INTER_CUBIC)

			kp2_1 = orb.detect(img2_1, None)

			kp2_1, des2_1 = orb.compute(img2_1,kp2_1)

			data_json[name+'_esc_'+str(jj)] = {'des':des2_1} 

			cv2.imwrite(path + name+'_esc_'+str(jj)+'.jpg',img2_1)

			#imagem rotacionada e escalada
			img2_2 = cv2.resize(img1,(int(jj*img.shape[0]), int(jj*img.shape[1])), interpolation = cv2.INTER_CUBIC)

			kp2_2 = orb.detect(img2_2,None)

			kp2_2, des2_2 = orb.compute(img2_2,kp2_2)

			data_json[ name+'_rot_'+str(ii)+'_esc_'+str(jj)] = {'des':des2_2}

			cv2.imwrite(path + name+'_rot_'+str(ii)+'_esc_'+str(jj)+'.jpg',img2_1)

			
			#smt
			for kk in smoth:

				#imagem original filtrada
				img3_1 = cv2.GaussianBlur(img,(kk,kk),0)

				kp3_1 = orb.detect(img3_1, None)
				
				kp3_1, des3_1 = orb.compute(img3_1,kp3_1 )

				data_json[name + '_smt_'+ str(kk)+'jpg'] = {'des':des3_1}
		
				cv2.imwrite(path + name + '_smt_'+ str(kk)+'.jpg',img3_1)
		
				#imagem escalada e filtrada
				img3_2 = cv2.GaussianBlur(img2_1,(kk,kk),0)

				kp3_2 = orb.detect(img3_1, None)
				
				kp3_2, des3_2 = orb.compute( img3_2,kp3_2)

				data_json[name +'_esc_'+str(jj) + '_smt_'+ str(kk)] = {'des':des3_2}
				cv2.imwrite(path + name +'_esc_'+str(jj) + '_smt_'+ str(kk) +'.jpg',img3_2)

				#imagem rotacionada e filtrada
				img3_3 = cv2.GaussianBlur(img1,(kk,kk),0)

				kp3_3 = orb.detect(img3_3, None)
				
				kp3_3, des3_3 = orb.compute(img3_3,kp3_3 )

				data_json[name +'_rot_'+str(ii) +  '_smt'+ str(kk)+'jpg'] = {'des':des3_3}

				cv2.imwrite(path + name +'_rot_'+str(ii) + '_smt_'+ str(kk) +'.jpg',img3_3)

				#imagem escalada rotacionada e filtrada
				img3_4 = cv2.GaussianBlur(img2_2,(kk,kk),0)

				kp3_4 = orb.detect(img3_4, None)
				
				kp3_4, des3_4 = orb.compute(img3_4,kp3_4 )

				data_json[name +'_rot_'+str(ii) +  '_esc_'+ str(jj)+'_smt_'+str(kk) +'jpg'] = {'des':des3_4}


				cv2.imwrite(path + name +'_rot_'+str(ii) +  '_esc_'+ str(jj)+'_smt_'+str(kk)+'.jpg',img3_3)

				with open(path+'database_test.pk1', 'wb') as handle:
    					pickle.dump(data_json, handle, protocol=pickle.HIGHEST_PROTOCOL)

				#sys.exit(0)
				
