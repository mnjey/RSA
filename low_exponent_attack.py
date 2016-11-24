#Try low exponent attack while e=3 or e=5
import os
import os.path
import sys
import copy
import binascii
import math
import gmpy2

key_in_work=5                                                                 #key_in_work is the value which equals to the e which is going to decode

def classify(class_list):                                                     #The function which is going to classify the frames of ciphertext.In this case,we are going to select the frames whose exponents are the same. 
	result_dict={}
	for item in class_list:
		if item[0] not in result_dict.keys():
			result_dict[item[0]]={}
		if item[1] not in result_dict[item[0]].keys():
			result_dict[item[0]][item[1]]=set()
		result_dict[item[0]][item[1]]=result_dict[item[0]][item[1]]|{item[2]}
	return result_dict



os.chdir("./fujian2")                                                         #The ciphertexts are all in the directory,fujian2
list_dir=os.listdir('.')
frame_list=[]                                                                 #frame_list is the list whose element is the tuples of (e,N,c,frame_name)
for frame_file in list_dir:
	with open(frame_file) as fd:
		code_str=fd.readline()
		N=int(code_str[0:256],16)                                             #extract N in the frame
		e=int(code_str[256:512],16)                                           #extract e in the frame
		c=code_str[512:768]                                                   #extract c in the frame
		frame_list.append((e,N,c,frame_file))



frame_class=classify(frame_list)
#print frame_list
all_file_name=[]
e=key_in_work
print "These frames has the same e (e="+repr(e)+"):"
for item in frame_list:                                                       #extract frames whose exponent equals to e
	if(item[0]==e):
		print item[3]
		all_file_name.append(item[3])
N=[]
c=[]



N=list(frame_class[key_in_work].keys())                                       #select all N in frame_class in order

for item in N:                                                                #select all c in frame_class in order 
	c.append(int(frame_class[key_in_work][item].pop(),16))
                                                                              #apply Chinese remainder theorem
M=1
for item in N:                                                                #calculate the M which is the product of all the N
	M*=item
Me=0
for index in range(len(N)):
	Me+=c[index]*(M/N[index])*gmpy2.invert(M/N[index],N[index])
Me%=M                                                                         #calcute the M^e with Chinese remainder theorem
M_result,flag=gmpy2.iroot(Me,e)                                               #calcute the M from M^e,if M is an integer,all the frames are encoded from the same plaintext,or the frames are not from the same plaintext
if flag:
	print "Trying "+",".join(all_file_name)+"......"
	result=hex(M_result).strip('L')[-16:]
	print "The plaintext message is :\n"+binascii.a2b_hex(result)
else:
	print "Fail to decode the ciphertext while e="+repr(e)


