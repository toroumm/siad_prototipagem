#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2, os,sys, json,pickle

def checkType(name):

	if not ('rot' in name or 'esc' in name or 'smt' in name):
		return 'normal'
	else:
		if('rot' in name and  'esc' not in name and 'smt' not in name):
			return 'rot'
		elif('esc' in name and  'rot' not in name and 'smt' not in name):
			return 'esc'
		elif('smt' in name and  'rot' not in name and 'esc' not in name):
			return 'smt'
		elif('rot' in name and  'esc'  in name and 'smt' not in name):
			return 'rot_esc'
		elif('rot' in name and  'smt'  in name and 'esc' not in name):
			return 'rot_smt'
		elif('rot' in name and  'smt'  in name and 'esc'  in name):
			return 'rot_smt_esc'
		elif('esc' in name and  'smt'  in name and 'rot' not in name):
			return 'esc_smt'

#**********************************************************************************************
		
def get_pos(key):
	coord = []
	k = None
	count  = 0
	for i in key:
		if i != '_' and i != '-':
			if k == None:
				k = i
			else:
				k = k+str(i)

		else:
			coord.append(int(k))
			k = None
		
		if len(coord) >= 4:	
			return coord
	if len(coord)<=3:
		coord.append(int(k))
	return coord

#**********************************************************************************************

def check_hit(coord_base, coord_comp):

	#for i in xrange(0,len(coord_base)):

	if coord_comp[0]  >=coord_base[0]  and coord_comp[1] <= coord_base[1] and coord_comp[2] >= coord_base[2]  and  coord_comp[3] <= coord_base[3]  :
		return True
	else:
		return False

#**********************************************************************************************

path_base = 'json_data/'

path_test = 'padroes_teste_modificados/'

dmax = [2,5,10,20,30,50]

with open(path_base+'mosaico_features_size_100_shift_25.pk1', 'rb') as handle:
	database =pickle.load(handle)


with open(path_test+'database_test.pk1', 'rb') as handle:
	test =pickle.load(handle)

bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)

resultado = {}

for t in test:

	des_test = test[t]['des']

	_type = checkType(t)

	if _type not in resultado.keys():
		resultado[_type] = {}

	#print get_pos(t), 
	
	for d in database:

		des_base = database[d]['des']
	
		match = bf.match(des_test,des_base)

		for _max in dmax:

			if _max not in resultado[_type].keys():
				resultado[_type][_max] = {'acerto':0,'erro':0}
		
			_distances = [m.distance for m in match if m.distance < _max]

			#print get_pos(t),get_pos(d), d, t
			
			print len(_distances), check_hit(get_pos(t), get_pos(d)), get_pos(t), get_pos(d)
	
			if len(_distances)> 5:
				
				if check_hit(get_pos(t), get_pos(d)):
					resultado[_type][_max]['acerto'] +=1
				else:
					resultado[_type][_max]['erro'] +=1


with open('json_data/resultado_01.json', 'w') as fp:
	json.dump(resultado, fp)

#print resultado
#		sys.exit()
	
#**********************************************************************************************



