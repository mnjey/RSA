#Although factoring large number is a hard problem,some large numbers with weaknesses are easy to factor.This program shows how to factor large numbers with one kind of weakness
import threading
import gmpy2
import hashlib
from binascii import a2b_hex,b2a_hex
import os


def classify(class_list):                                                     #The function which is going to classify the frames of ciphertext.In this case,we are going to select the frames whose modules,N are the same. 
	result_dict={}
	for item in class_list:
		if item[0] not in result_dict.keys():
			result_dict[item[0]]={}
		if item[1] not in result_dict[item[0]].keys():
			result_dict[item[0]][item[1]]=set()
		result_dict[item[0]][item[1]]=result_dict[item[0]][item[1]]|{(item[2],item[3])}
	return result_dict




def fermat_factor(n):                                                         #This function is very effective for those large numbers whose p and q are close.
    assert n % 2 != 0

    a = gmpy2.isqrt(n)
    b2 = a**2 - n

    while not gmpy2.is_square(b2):
        a += 1
        b2 = a**2 - n

    factor1 = a + gmpy2.isqrt(b2)
    factor2 = a - gmpy2.isqrt(b2)
    return int(factor1), int(factor2) 


class multithread_factor(threading.Thread):                                   #Because this kind of attack is only useful to these numbers with weakness,we design a multi-thread program to test all the frames at the same time
    def __init__(self,N,e,frame_name):
        threading.Thread.__init__(self)
        self.N=N
        self.e=e
        self.frame_name=frame_name
    def run(self):
        (p, q) = fermat_factor(self.N)
        phi_n = (p - 1) * (q - 1)
        #print int(p)*int(q)-N
        print "decoding"
        print self.frame_name
        print p
        print q
        d = gmpy2.invert(self.e, phi_n)
        print d
if __name__ == "__main__":
	os.chdir("./fujian2")                                                         #The ciphertexts are all in the directory,fujian2
	list_dir=os.listdir('.')
	#print list_dir
	frame_list=[]                                                                 #frame_list is the list whose element is the tuples of (e,N,c,frame_name)
	for frame_file in list_dir:
		with open(frame_file) as fd:
			code_str=fd.readline()
			N=int(code_str[0:256],16)                                             #extract N in the frame
			e=int(code_str[256:512],16)                                           #extract e in the frame
			c=code_str[512:768]                                                   #extract c in the frame
			frame_list.append((N,e,c,frame_file))
	frame_class=classify(frame_list)
	for N in frame_class:
		for e in frame_class[N]:
			one_thread=multithread_factor(N,e,frame_class[N][e].pop()[1])
			one_thread.start()
