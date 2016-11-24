#Because we have many modules,there are probably two mudules having a same factor
import os
import os.path
import sys
import copy
import binascii
import math
def gcd(a,b):
	while(a!=0):
		a,b=b%a,a
	return b


def findModInverse(a,m):
	if(gcd(a,m)!=1):
		return None
	u1,u2,u3=1,0,a
	v1,v2,v3=0,1,m
	while(v3!=0):
		q=u3//v3
		v1,v2,v3,u1,u2,u3=(u1-q*v1),(u2-q*v2),(u3-q*v3),v1,v2,v3
	#print v1,v2,v3,u1,u2,u3
	return u1%m




os.chdir("./fujian2")
list_dir=os.listdir('.')
#print list_dir
frame_list=[]

for frame_file in list_dir:
	with open(frame_file) as fd:
		code_str=fd.readline()
		N=int(code_str[0:256],16)
		e=int(code_str[256:512],16)
		c=code_str[512:768].lower()
		frame_list.append((frame_file,e,N,c))
for i in range(len(frame_list)):
	for j in range(i+1,len(frame_list)):
		if(frame_list[i][2]!=frame_list[j][2] and gcd(frame_list[i][2],frame_list[j][2])!=1):
			#print frame_list[i][0]+"    "+repr(frame_list[i][1])+"   "+frame_list[j][0]+"       "+repr(frame_list[j][1])
			frame_with_common_factor=[frame_list[i],frame_list[j]]
			common_factor=gcd(frame_list[i][2],frame_list[j][2])
print "The following frames have common factor: \n"+frame_with_common_factor[0][0]+"   "+frame_with_common_factor[1][0]
print
for frame in frame_with_common_factor:
	print "Decording "+frame[0]+" ......"
	p=common_factor
	q=frame[2]/p
	phiN=(p-1)*(q-1)
	d=findModInverse(frame[1],phiN)
	#print "d is "+repr(d)
	#print math.log(d,2)
	plain=pow(int(frame[3],16),d,frame[2])
	plain_hex=hex(plain)
	plain_str=binascii.a2b_hex(plain_hex[-17:-1])
	print "The plaintext frame is: \n"+plain_hex	
	print "The plaintext message is: \n"+plain_str
	print "N has those factors: \n"+repr(p)+"\n"+repr(q)
	print "The d is: \n"+repr(d)
	print

