# Sheikh Salim 1003367
# 50.042 FCS Lab 6 template

import random
def square_multiply(a,x,n):
    # from lecture slides
    res = 1
    for i in bin(x)[2:]:
        res = res * res % n
        if i == '1':
            res = res*a % n
    return res

def miller_rabin(n, a):

    # trying to find d and r
    r = 0
    d = n-1
    while d % 2 ==0:
        d = d // 2
        r += 1

    # non deterministic variant - adapted from wikipedia
    for i in range(a):
        random_int = random.randint(2, n-2)
        x = square_multiply(random_int, d, n)
        if x == 1 or x == n-1:
            continue
        for j in range(r-1):
            x = x**2 % n
            if x == n-1:
                break
        else:
            return False  # composite
    return True  # probbaly

def gen_nbits(n):
    # Step 1 : Generate random bits of same length
    random_bit = random.getrandbits(n)
    # Step 2 : Make sure its odd, and make sure proper n-bit generated
    lb_mask = 1
    fb_mask = 1 << n - 1
    random_bit = random_bit | lb_mask | fb_mask
    return random_bit

def gen_prime_nbits(n):
    # Step 3 : Check if this candidate is a prime
    while True:
        candidate = gen_nbits(n)
        # Rationale given that https://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes
        if miller_rabin(candidate, 40):
            return candidate




if __name__=="__main__":
    print('Is 561 a prime?')
    print(miller_rabin(561, 2))
    print('Is 27 a prime?')
    print(miller_rabin(27, 2))
    print('Is 61 a prime?')
    print(miller_rabin(61, 2))

    print('Random number (100 bits):')
    print(gen_prime_nbits(100))
    print('Random number (140 bits):')
    print(gen_prime_nbits(140))
