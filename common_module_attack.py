#Common_module_attack.Try decoding ciphertext frames with the same N but different e 
import os
import os.path
import sys
import copy
import binascii
import gmpy2


def classify(class_list):                                                     #The function which is going to classify the frames of ciphertext.In this case,we are going to select the frames whose modules,N are the same. 
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
#print list_dir
frame_list=[]                                                                 #frame_list is the list whose element is the tuples of (e,N,c,frame_name)
for frame_file in list_dir:
	with open(frame_file) as fd:
		code_str=fd.readline()
		N=code_str[0:256]                                                     #extract N in the frame
		e=code_str[256:512]                                                   #extract e in the frame
		c=code_str[512:768]                                                   #extract c in the frame
		frame_list.append((N,e,c,frame_file))
frame_class=classify(frame_list)

for key in frame_class:                                                       #judge if there are any frames having the same module
	len_tmp=len(frame_class[key])
	if len_tmp>1:
		key_in_work=key
		break


N=key_in_work
print "These frames has the same N:"
for item in frame_list:                                                       #extract frames whose module equals to N
	if(item[0]==N):
		print item[3]
print
e1,e2=frame_class[key_in_work].keys()
c1=frame_class[key_in_work][e1].pop()
c2=frame_class[key_in_work][e2].pop()



N=int(N,16)
e1=int(e1,16)
e2=int(e2,16)
c1=int(c1,16)
c2=int(c2,16)
tmp,X,Y=gmpy2.gcdext(e1,e2)                                                   #apply extend euclidean algorithm to get X,Y(X*e1+Y*e2=1)

if(X<0):                                                                      #translate negative exponent to positive exponent by calculating the inverse of ciphertext
	c1=gmpy2.invert(c1,N)
	X=abs(X)
if(Y<0):
	c2=gmpy2.invert(c2,N)
	Y=abs(Y)


print
result=hex(pow(c1,X,N)*pow(c2,Y,N)%N).strip('L')[-16:]                        #claculate the plaintext frame and output it

print "The plaintext message is: \n"+binascii.a2b_hex(result)




