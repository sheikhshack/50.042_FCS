#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# 1003367 - Sheikh Salim
# Simple file read in/out


# Import libraries
import sys
import argparse
import string


def encrypt_chars(char, key):
    if char in string.printable:
        encrypted_char = ((string.printable.index(char) + int(key)) % len(string.printable))
        return string.printable[encrypted_char]
    else:
        print("OOOOF--------------------------------------")
        return char


def decrypt_chars(char, key):
    if char in string.printable:
        # to offset the negative, we intro + 100, followed by a mod
        decrypted_char = (string.printable.index(char) - int(key) + 100) % len(string.printable)
        return string.printable[decrypted_char]
    else:

        return char



def doStuff(filein,fileout, mode, key):
    # open file handles to both files
    fin  = open(filein, mode='r', encoding='utf-8', newline='\n')       # read mode
    fin_b = open(filein, mode='rb')  # binary read mode
    fout = open(fileout, mode='w', encoding='utf-8', newline='\n')      # write mode
    fout_b = open(fileout, mode='wb')  # binary write mode
    c    = fin.read()         # read in file into c as a str
    result = []

    # and write to fileout

    # close all file streams
    fin.close()
    fin_b.close()
    fout.close()
    fout_b.close()

    # does the additional checks
    encrypt = True
    if mode.upper() == 'E':
        encrypt = True
    elif mode.upper() == "D":
        encrypt = False
    else:
        raise argparse.ArgumentTypeError("This will never happen, created for testing arparser only")

    if key < 0 or key > len(string.printable) - 1:
        raise argparse.ArgumentTypeError("Value of %i is not supported as key" % key)

    # PROTIP: pythonic way
    with open(filein, mode="r", encoding='utf-8', newline='\n') as fin:
        text = fin.read()
        if encrypt == True:
            print('encrypt mode')
            result = [encrypt_chars(char, key) for char in text]
        else:
            print('decrypt mode')
            result = [decrypt_chars(char, key) for char in text]

        # file will be closed automatically when interpreter reaches end of the block
    with open(fileout, mode='w', encoding='utf-8', newline='\n') as fout:
        fout.write(''.join(str(x) for x in result))

# our main function
if __name__=="__main__":
    # set up the argument parser, also going to handle the nitty gritty input sanitation
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='filein',help='input file', required=True)
    # >>> parser.add_argument('--foo', type=int, default=42, help='FOO!')
    parser.add_argument('-o', dest='fileout', help='output file', required=True)
    parser.add_argument('-k', dest='key', help='key, between 0 and 99', type=int,  required=True)
    parser.add_argument('-m', dest='mode', help='mode', choices={"D", "d", "e", "E"}, default="E")


    # parse our arguments
    args = parser.parse_args()
    filein=args.filein
    fileout=args.fileout
    key=args.key
    mode=args.mode

    doStuff(filein,fileout, mode, key)

    # all done


