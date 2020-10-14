#!/usr/bin/env python3
# ECB wrapper skeleton file for 50.042 FCS

from present import *
import argparse
import sys
import time
nokeybits=80
blocksize=64
blocksize_bytes = 8 # use bytes as python can only read whole bytes at a time, so doesnt matter


def encrypt_blocks(plain_block, key):
    if len(plain_block) < blocksize_bytes:
        print('Padding generated, using PKCS7')
        bytes_append = blocksize_bytes - len(plain_block)
        plain_block += bytes(bytes_append for i in range(bytes_append))
    # Big endian format, MSB at begining
    integer_format = int.from_bytes(plain_block, byteorder='big')
    return present(integer_format, key)

def decrypt_blocks(plain_block, key):
    # Big endian format, MSB at begining
    integer_format = int.from_bytes(plain_block, byteorder='big')
    return present_inv(integer_format, key)

# def remove_padding(block):
#     # PKCS7 standard
#     pad = block & 0xff
#     print('Block value is ', hex(block))
#     print('The and version gives', hex(block & 0xff))
#     # print('pad value given by', hex(int.from_bytes(pad, byteorder='big')))
#     if pad <= 0x10:
#         print('Padding detected, removing now')
#         block =
#         print(hex(int.from_bytes(block, byteorder='big')))
#         print('new shift ', hex(int.from_bytes(block[:len(block) - pad], byteorder='big')))
#         return int.from_bytes(block[:len(block) - pad], byteorder='little'), len(block)-pad
#     return block, 8


def remove_padding_v2(block):
    # PKCS7 standard
    print('block is ', hex(block))
    pad = block & 0xff
    print('Testing pad with value ', pad)
    # print('pad value given by', hex(int.from_bytes(pad, byteorder='big')))
    if pad > 0x10:
        print('No padding detected, exiting now')
        return block, 8
    for i in range(pad):
        temp_block = (block >> 8 * i) & 0xff
        if temp_block != pad:
            print('Oh fuck, guess it was coincidence')
            return block, 8
    block = block >> 8 * pad
    return block, 8-pad



def ecb(infile,outfile,key,mode):

    starts_time = time.perf_counter()
    with open(infile, 'rb') as source, open(outfile, 'wb') as dest:
        result = []
        if mode == 1:
            print('Setting up encrypt mode')
            while True:
                byte = source.read(blocksize_bytes)
                if not byte:
                    break
                encrypted = encrypt_blocks(byte, key)
                dest.write(encrypted.to_bytes(8, byteorder='big'))

        elif mode == 0:
            print('Setting up decrypt mode')
            while True:
                byte = source.read(blocksize_bytes)
                if not byte:
                    break
                decrypted = decrypt_blocks(byte, key)
                result.append(decrypted)
            # additional step of removing padding
            print(result[-1])
            result[-1], writingbits = remove_padding_v2(result[-1])
            print(result[-1])
            for i in range(len(result)-1):
                dest.write(result[i].to_bytes(8, byteorder='big'))
            dest.write(result[-1].to_bytes(writingbits, byteorder='big'))
    source.close()
    dest.close()
    ends_time = time.perf_counter()
    print('Total time ',ends_time - starts_time)






if __name__=="__main__":
    # parser=argparse.ArgumentParser(description='Block cipher using ECB mode.')
    # parser.add_argument('-i', dest='infile',help='input file')
    # parser.add_argument('-o', dest='outfile',help='output file')
    # parser.add_argument('-k', dest='keyfile',help='key file')
    # parser.add_argument('-m', dest='mode',help='mode')
    #
    # args=parser.parse_args()
    # infile=args.infile
    # outfile=args.outfile
    # keyfile=args.keyfile
    ecb('Tux.ppm', 'Tuxenc.ppm', 0xdeadbeefdeadbeef, 1)

    ecb('Tuxenc.ppm', 'Tuxdec.ppm', 0xdeadbeefdeadbeef, 0)
    # ecb_testdecrypt(0xdeadbeefdeadbeef)

    # ecb_test(0xdeadbeefdeadbeef)




