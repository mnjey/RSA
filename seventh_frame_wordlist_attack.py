#By now,we have found that the structure of plaintext frame.
#In this program,we give the prefix of the fourth plaintext frame.And we already have get the sixth plaintext frame which ends with "." and the eighth plaintext frame is " "Logic",we just construct a wordlist of the words which looks meaningful.
import os
import os.path
import sys
import copy
import binascii
import math






os.chdir("./fujian2")
list_dir=os.listdir('.')
frame_list=[]
E_attemp=3
plain_pre="9876543210abcdef000000060000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
#The seventh plaintext frame starts with the string,plain_pre.
potential_ending=[' It says',' It said',' That is',' He says',' He said']    #This is our wordlist.The seventh plaintext frame probably ends with these words with length 8.
for frame_file in list_dir:
	with open(frame_file) as fd:
		code_str=fd.readline()
		N=int(code_str[0:256],16)                                            #extract N in the frame
		e=int(code_str[256:512],16)                                          #extract e in the frame
		c=code_str[512:768].lower()                                          #extract c in the frame
		frame_list.append((frame_file,e,N,c))

for item_0 in frame_list:                                                    #We just try all the items in the wordlist to see which is the plaintext message.
	for item in potential_ending:
		plain_num=int(plain_pre+binascii.b2a_hex(item),16)
		if(item_0[3].lstrip('0') in hex(pow(plain_num,item_0[1],item_0[2]))):
			print "Decoding "+item_0[0]+"......"
			print "The plaintext message is "+item


