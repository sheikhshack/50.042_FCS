#50.042 FCS Lab 6 template
#Year 2019

import primes 
import random


def dhke_setup(nb):
    # choosing a prime number
    p = 11
    # getting the generator

    for i in range(2, p-1):
        current_generator = random.randint(2, p-2)
        print('current candidate: ', current_generator)
        first_inst = primes.square_multiply(current_generator, 1, p)
        print('First instance ', first_inst)
        last_inst = primes.square_multiply(current_generator, p, p)
        print('last instance ', last_inst)

        if first_inst == last_inst:
            # starts the computation
            for j in range(2,p):
                current_inst = primes.square_multiply(current_generator, i, p)
                if current_inst == last_inst:  # loop detected
                    if i != p-1:
                        break
                    else:
                        return p, current_generator




    pass

def gen_priv_key(p):
    pass

def get_pub_key(alpha, a, p):
    pass

def get_shared_key(keypub,keypriv,p):
    pass
    
if __name__=="__main__":
    p,alpha= dhke_setup(10)
    print('Generate P and alpha:')
    print('P:', p)
    print('alpha:', alpha)
    # print
    # a=gen_priv_key(p)
    # b=gen_priv_key(p)
    # print('My private key is: ', a)
    # print('Test other private key is: ', b)
    # print
    # A=get_pub_key(alpha,a,p)
    # B=get_pub_key(alpha,b,p)
    # print('My public key is: ', A)
    # print('Test other public key is: ', B)
    # print
    # sharedKeyA=get_shared_key(B,a,p)
    # sharedKeyB=get_shared_key(A,b,p)
    # print('My shared key is: ', sharedKeyA)
    # print('Test other shared key is: ', sharedKeyB)
    # print('Length of key is %d bits.' % sharedKeyA.bit_length())

