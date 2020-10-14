#!/usr/bin/env python3
# ECB plaintext extraction skeleton file for 50.042 FCS

import argparse


def getInfo(headerfile):
    with open(headerfile, 'rb') as header:
        content = header.read()
        print('Header given by ', content, ' with length ', len(content))
    return content


def getMostCommonBytePattern(infile, decrypted_header):
    counts = {}
    with open(infile, 'rb') as scanner:
        # moves filepointer ahead to skip header + the trailing bytes in the block (15 +1 = 16 full block)
        blocks_to_skip = int(len(decrypted_header) / 8) + 1  # in this case its 2 blocks = 16 bytes
        scanner.read(blocks_to_skip * 8)
        while True:
            scan_byte = scanner.read(8)
            if not scan_byte:
                break
            counts[scan_byte] = counts.get(scan_byte, 0) + 1
    return max(counts, key=counts.get)


def extract(infile, outfile, headerfile):
    decrypted_header = getInfo(headerfile)
    most_common = getMostCommonBytePattern(infile, decrypted_header)
    with open(infile, 'rb') as source, open(outfile, 'wb') as dest:
        # moves filepointer ahead to skip header + the trailing bytes in the block (15 +1 = 16 full block)
        blocks_to_skip = int(len(decrypted_header) / 8) + 1  # in this case its 2 blocks = 16 bytes
        print(source.read(blocks_to_skip * 8))
        padder = 8 - len(decrypted_header) % 8
        dest.write((decrypted_header.decode() + padder * '\n').encode())
        while True:
            byte = source.read(8)
            if not byte:
                break
            # int_format = int.from_bytes(byte, byteorder='big')
            if byte == most_common:
                stringified_byte = b'00000000'
            else:
                stringified_byte = b'11111111'
            dest.write(stringified_byte)
        source.close()
        dest.close()


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description='Extract PBM pattern.')
    parser.add_argument('-i', dest='infile',help='input file, PBM encrypted format')
    parser.add_argument('-o', dest='outfile',help='output PBM file')
    parser.add_argument('-hh', dest='headerfile',help='known header file')

    args=parser.parse_args()
    infile=args.infile
    outfile=args.outfile
    headerfile=args.headerfile

    print('Reading from: %s'%infile)
    print('Reading header file from: %s'%headerfile)
    print('Writing to: %s'%outfile)


    success=extract(infile,outfile,headerfile)


