#50.042 FCS Lab 6 template
#Year 2019

import primes 
import random


def dhke_setup(nb):
    # choosing a prime number
    p = primes.gen_prime_nbits(nb)
    # getting the generator
    a = random.randint(2, p-2)
    return p, a
    #
    # for i in range(2, p-1):
    #     current_generator = random.randint(2, p-2)
    #     print('current candidate: ', current_generator)
    #     first_inst = primes.square_multiply(current_generator, 1, p)
    #     print('First instance ', first_inst)
    #     last_inst = primes.square_multiply(current_generator, p, p)
    #     print('last instance ', last_inst)
    #
    #     if first_inst == last_inst:
    #         # starts the computation
    #         current_inst = first_inst
    #         for j in range(2,p+1):
    #             current_inst = (current_inst * current_generator) % p
    #             # print('current value is at ', current_inst)
    #             if current_inst == last_inst:  # loop detected
    #                 if j != p:
    #                     print('Loop detected at :' ,j)
    #                     break
    #                 else:
    #                     return p, current_generator


def gen_priv_key(p):
    return random.randint(2, p-2)


def get_pub_key(alpha, a, p):
    return primes.square_multiply(alpha, a, p)

def get_shared_key(keypub,keypriv,p):
    return primes.square_multiply(keypub, keypriv, p)
    
if __name__=="__main__":
    p,alpha= dhke_setup(80)
    print('Generate P and alpha:')
    print('P:', p)
    print('alpha:', alpha)
    print
    a=gen_priv_key(p)
    b=gen_priv_key(p)
    print('My private key is: ', a)
    print('Test other private key is: ', b)
    print
    A=get_pub_key(alpha,a,p)
    B=get_pub_key(alpha,b,p)
    print('My public key is: ', A)
    print('Test other public key is: ', B)
    print
    sharedKeyA=get_shared_key(B,a,p)
    sharedKeyB=get_shared_key(A,b,p)
    print('My shared key is: ', sharedKeyA)
    print('Test other shared key is: ', sharedKeyB)
    print('Length of key is %d bits.' % sharedKeyA.bit_length())

