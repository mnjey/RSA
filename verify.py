#By now, we have guessed out all the plaintext frames.Here we just to verify them.
import os
import os.path
import sys
import copy
import binascii
import math

def classify(class_list):
	#store_list=copy.deepcopy(class_list)
	#result_list=[]
	result_dict={}
	for item in class_list:
		if item[0] not in result_dict.keys():
			#result_list.append(item[0])
			result_dict[item[0]]={}
		#index_num=result.index(item[0])
		if item[1] not in result_dict[item[0]].keys():
			result_dict[item[0]][item[1]]=set()
		result_dict[item[0]][item[1]]=result_dict[item[0]][item[1]]|{item[2]}
	return result_dict








os.chdir("./fujian2")
list_dir=os.listdir('.')
print list_dir
frame_list=[]
E_attemp=3
plain_l=[]
with open('../answer.txt') as fd:                                    #We put all the plaintext frame in answer.txt
	for line in fd.readlines():
		plain_l.append(line.strip())
for frame_file in list_dir:
	with open(frame_file) as fd:
		code_str=fd.readline()
		N=int(code_str[0:256],16)
		e=int(code_str[256:512],16)
		c=code_str[512:768].lower()
		frame_list.append((frame_file,e,N,c))
index=0
for plain in plain_l:                                                #Here we encrypt our plaintext with the parameters in the ciphertext to see if the encrypted plaintext equals to the ciphertext
	print "Plaintext frame "+repr(index)
	plain_num=int(plain,16)
	for item_0 in frame_list:
		if(int(item_0[3],16) == pow(plain_num,item_0[1],item_0[2])):
			print item_0[0]
	index+=1
