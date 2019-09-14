# -*- coding: utf-8 -*-
from __future__ import print_function
#!/usr/env/bin python3

import requests
import numpy as np
import json
import time
from tqdm import tqdm
import sys, errno
from itertools import product
import pandas as pd


import csv



# https://oauth.vk.com/blank.html#access_token=c44329369519758099e485f1bb86f0435399078b140fe6c3fa4d1e46f51e17beee232124809550c8487ae&expires_in=0&user_id=496092199

base = 'https://api.vk.com/method/'

group_id = 'lamodaru'
access_token = 'c44329369519758099e485f1bb86f0435399078b140fe6c3fa4d1e46f51e17beee232124809550c8487ae'
version = '5.1'

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r{} |{}| {}% {}'.format(prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

def get_members(group_id):

	method = 'groups.getMembers'
	target_group = group_id
	count = 0
	url = '{}{}?group_id={}&access_token={}&v={}'.format(base,method,target_group,access_token,version)
	members_list = []

	# first let's get the members number
	r = requests.get(url)
	# Decode the JSON data into a dictionary: json_data
	json_data = r.json()
	# print(json_data)
	members_count = json_data['response']['count']
	print('There are {} members in {} community '.format(members_count,group_id))
	for step,rq in enumerate(range(0,(members_count//1000)+1)):
		printProgressBar(step,members_count//1000)
		offset = rq*1000

		new_url = '{}&offset={}'.format(url,offset)
		json_data = requests.get(new_url).json()
		members_list.extend(json_data['response']['users'])

		if(rq%3==0) and rq>0:
			# print('Wait..members')
			time.sleep(1)

	return members_list

def get_wall(chel):
	method = 'wall.get'

def get_friends_for_id(id):
	method = 'friends.get'
	# print('------------------------\n\n',id)
	target_id = id
	count = 0
	url = '{}{}?user_id={}&access_token={}&v={}'.format(base,method,target_id,access_token,version)
	# print(url)
	friends_list = []	


	# first let's get the friends number
	json_data = requests.get(url).json()
	# print(json_data)
	if 'response' in json_data.keys():
		friends_cound = json_data['response']['count']
	else:
 		return False
	# print(friends_cound)
	for rq in range(0,(friends_cound//1000)+1):

		# print(range(0,(friends_cound//1000)+1))
		offset = rq*1000

		new_url = '{}&offset={}'.format(url,offset)
		json_data = requests.get(new_url).json()
			# print(json_data)
		if 'response' in json_data.keys():
			friends_list.extend(json_data['response']['items'])
		else:
	 		continue		
		

		if(rq%3==0):
			# print('Wait..friends')
			time.sleep(1)
	# print(id,friends_cound, len(friends_list))
	return friends_list



'''


'''
if __name__ == "__main__":
	members = get_members(group_id)

	draph_dic = {}

	# print(members)


	for i,member in enumerate(members):
		printProgressBar(i,len(members))
		# printProgressBar(iteration=i,total=len(members))

		try:
			print('LOOP  ',i,len(members))
		except:
			pass
		friends_fro_id =  get_friends_for_id(member)
		if friends_fro_id:
			draph_dic[member] = friends_fro_id
		if(i%3==0):
			# print('Wait..main')
			time.sleep(1)


	nodes = [{'node':x} for x in list(draph_dic.keys())]
	nodes_list = [x for x in list(draph_dic.keys())]
	edges = []

	for k,v in draph_dic.items():
		edges.extend([{'node1':x,'node2':y} for x in [k] for y in v if (x in nodes_list and y in nodes_list)])	# this is for diGraph, for simple Graph and if not (y,x) in edges 
	    # G_lmc.add_edges_from(zip([node]*len(list(G.neighbors(node))), G.neighbors(node)))

	print("Your graph has {} nodes".format(len(nodes)))
	print("Your graph has {} edges".format(len(edges)))
	
	nodes_df = pd.DataFrame(nodes,columns=['node'])
	edges_df = pd.DataFrame(edges,columns=['node1','node2'])
	print(nodes_df.head())
	print(edges_df.head())
	nodes_df.to_csv('nodes_full.csv')
	edges_df.to_csv('edges_full.csv')



