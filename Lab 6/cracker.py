# Sheikh Salim 1003367
# 50.042 FCS Lab 6 template
# This is the cracker for part 6

import babygiant_template
import dhke_template
import primes_template
import time
import csv

# we start cracking from 16 onwards
with open('result.csv', 'w') as csvoutput:
    writer = csv.writer(csvoutput, lineterminator='\n', quoting=csv.QUOTE_NONE, escapechar='\\')

    for i in range(16, 80):
        try:
            while True:
                p, alpha = dhke_template.dhke_setup(i) # p is exposed
                a = dhke_template.gen_priv_key(p)
                b = dhke_template.gen_priv_key(p)
                A = dhke_template.get_pub_key(alpha, a, p) # exposed
                B = dhke_template.get_pub_key(alpha, b, p) # exposed
                sharedKey = dhke_template.get_shared_key(B,a,p) # exposed

                if sharedKey.bit_length() == i:
                    break

            # Cracking starts here proper
            start_time = time.perf_counter()
            a = babygiant_template.baby_giant(alpha, A, p)
            b = babygiant_template.baby_giant(alpha, B, p)
            guesskey1 = primes_template.square_multiply(A, b, p)
            guesskey2 = primes_template.square_multiply(B, a, p)

            if guesskey1 == sharedKey or guesskey2 == sharedKey:
                end_time = time.perf_counter()
                writer.writerow([i, end_time-start_time])
                print(guesskey1, guesskey2, sharedKey)
                print('Cracked key of length {0} in {1} s'.format(i, end_time-start_time))

        except KeyboardInterrupt:
            csvoutput.close()
            print('\nInterrupted, gracefully breaking and saving progress')


