#50.042 FCS Lab 6 template
#Year 2019

from math import sqrt, floor
import primes

# Mission, solve discrete log

def baby_step(alpha,beta,p,fname):
    m = floor(sqrt(p-1))
    with open(fname, 'w') as fptr:
        for i in range(m):
            res = (primes.square_multiply(alpha, i, p) * beta) % p
            if i == m-1:
                fptr.write(str(res))
            else:
                fptr.write(str(res))
                fptr.write('\n')
    
def giant_step(alpha,p,fname):
    m = floor(sqrt(p - 1))
    with open(fname, 'w') as fptr:
        for i in range(m):
            res = primes.square_multiply(alpha, m * i, p)
            if i == m - 1:
                fptr.write(str(res))
            else:
                fptr.write(str(res))
                fptr.write('\n')

def baby_giant(alpha,beta,p):
    # call each step first
    m = floor(sqrt(p - 1))
    baby_step(alpha, beta, p, 'baby.txt')
    giant_step(alpha, p, 'giant.txt')
    # open baby.txt, store in set
    lookup_baby = {}
    with open('baby.txt', 'r') as f1:
        index = 0
        for line in f1:
            # reversed dict
            lookup_baby[line] = int(index)
            index += 1

    with open('giant.txt', 'r', newline='\n') as f2:
        x_g = 0
        for candidate in f2:
            if candidate in lookup_baby:
                x_b = lookup_baby.get(candidate)
                return (x_g * m) - x_b
            else:
                x_g += 1

if __name__=="__main__":
    """
    test 1
    My private key is:  264
    Test other private key is:  7265
    
    """
    p=17851
    alpha=17511
    A=2945
    B=11844
    sharedkey=1671
    a=baby_giant(alpha,A,p)
    b=baby_giant(alpha,B,p)
    guesskey1=primes.square_multiply(A,b,p)
    guesskey2=primes.square_multiply(B,a,p)
    print('Guess key 1:', guesskey1)
    print('Guess key 2:', guesskey2)
    print('Actual shared key :', sharedkey)

