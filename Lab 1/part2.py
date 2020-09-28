#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# 1003367 - Sheikh Salim
# Simple file read in/out


# Import libraries
import sys
import argparse
import string


def encrypt_bytes(byte, key):
    # print("Byte value is ", byte)
    byte_val = (byte + key) % 256
    return byte_val


def decrypt_bytes(byte, key):
    # same as ex 1.1, we wanna make sure no negs
    byte_val = (byte - key + 256) % 256
    return byte_val



def doStuff(filein,fileout, mode, key):
    # open file handles to both files

    # does the additional checks
    encrypt = True
    if mode.upper() == 'E':
        encrypt = True
    elif mode.upper() == "D":
        encrypt = False
    else:
        raise argparse.ArgumentTypeError("This will never happen, created for testing arparser only")

    if key < 0 or key > 255:
        raise argparse.ArgumentTypeError("Value of %i is not supported as key" % key)

    # PROTIP: pythonic way
    with open(filein, mode="rb") as fin:
        text = bytearray(fin.read())
        if encrypt == True:
            print('encrypt mode')
            result = bytearray([encrypt_bytes(byte, key) for byte in text])
        else:
            print('decrypt mode')
            result = bytearray([decrypt_bytes(byte, key) for byte in text])

        # file will be closed automatically when interpreter reaches end of the block
    with open(fileout, mode='wb') as fout:
        fout.write(result)

# our main function
if __name__=="__main__":
    # set up the argument parser, also going to handle the nitty gritty input sanitation
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='filein',help='input file', required=True)
    parser.add_argument('-o', dest='fileout', help='output file', required=True)
    parser.add_argument('-k', dest='key', help='key must be between 0 and 255', type=int, required=True)
    parser.add_argument('-m', dest='mode', help='mode', choices={"D", "d", "e", "E"}, default='E')


    # parse our arguments
    args = parser.parse_args()
    filein=args.filein
    fileout=args.fileout
    key=args.key
    mode=args.mode

    doStuff(filein,fileout, mode, key)

    # all done



# For part 3, we can analyse the fileheader of the encrypted file and determine that the header corresponds to filetype `FD=`
# We know for a fact that we expected to receive a `PNG`. Hence, using the ord function in python to convert ascii chars into
# integers, we can easily determine the shifts
# P -> F : 80 -> 70
# N -> D : 78 -> 68
# G -> = : 71 -> 61
#
# Hence, from this, we can deduce that the key has to be 256-10 = 246, since we see it going backwards by -10 shifts
# With this in mind, we decrypt and the result is a swiss flag :) If we weren't as lucky, prolly will have used bruteforce


