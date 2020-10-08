## Sheikh Salim 1003367
## FCS Lab 3
## Time taken : 28.535s. Please refer to the writeup for WriteUp.md for more details for parts 3 & 5

import hashlib
import string
import random
import os
import time
import csv

def hash_it(message):
    return hashlib.md5(message.encode()).hexdigest()


def randomiser(choices, targets):
    cracked= []
    relevant_hash = []
    for candidate1 in choices:
        for candidate2 in choices:
            for candidate3 in choices:
                for candidate4 in choices:
                    for candidate5 in choices:
                        attack_message = candidate1 + candidate2 + candidate3 + candidate4 + candidate5
                        hashed_attack = hash_it(attack_message)
                        if hashed_attack in targets:
                            cracked.append(attack_message)
                            relevant_hash.append(hashed_attack)
                            targets.remove(hashed_attack)
                            print([attack_message, hashed_attack])
                        if len(targets) == 0:
                            return cracked, relevant_hash

    return cracked, relevant_hash




def salt_and_hash(list_of_messages):
    try:
        os.remove('hash5_salted.txt')
        os.remove('hash5_salted_for_rbw.txt')
    except:
        print('We good')

    with open('hash5_salted.txt', 'w' ) as f1, open('hash5_salted_for_rbw.txt', 'w') as f2, open('pass_with_salt.txt', 'w') as f3:
        for message in list_of_messages:
            salt = random.choice(string.ascii_lowercase)
            appended = message + salt
            f3.write(appended + '\n')
            hashed = hash_it(appended)
            f1.write(hashed + ',' + salt)
            f2.write(hashed)
            f1.write('\n')
            f2.write('\n')

if __name__ == "__main__":

    with open('hash5.txt', 'r') as f:
        targets = set([line.strip() for line in f])

    ### This segment of the code deals with Part 3
    start_time = time.perf_counter()
    available_selection = string.ascii_lowercase + string.digits
    cracked, hashish = randomiser(available_selection, targets)
    end_time = time.perf_counter()
    print('Time taken: {}'.format(end_time-start_time))
    #### End of segmenmt for Part 3

    # ### This segment of the code deals with Part 5
    # list_of_cracked = ['aseas', 'cance', 'di5gv', 'dsmto', 'egunb', 'hed4e', 'lou0g', 'mlhdi', 'nized', 'ofror', 'opmen', 'owso9', 'sso55', 'tpoin', 'tthel']
    # salt_and_hash(list_of_cracked)
    # #### End of segmenmt for Part 5
    # #
    # # ### Additonal Formatting for Challenge
    # # save_and_format('output.csv', 'outputv1.csv', 'cracked_lmao.txt')

