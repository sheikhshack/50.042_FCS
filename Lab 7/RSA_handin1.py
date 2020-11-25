# Sheikh 1003367 - Lab 7 RSA

import random
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from base64 import b64decode,b64encode



# From Lab 6
def square_multiply(a,x,n):
    res = 1
    for i in bin(x)[2:]:
        res = res * res % n
        if i == '1':
            res = res*a % n
    return res

def encrypt_message(msg, e, n, integer_mode=False):
    if not integer_mode:
        msg_int = int.from_bytes(msg, byteorder='little')
    else:
        msg_int = msg
    ciphertext = square_multiply(msg_int, e, n)
    res = ciphertext.to_bytes((ciphertext.bit_length() + 7) // 8, byteorder='little')
    # with open('encrypted_msg.txt', 'wb') as fwrite:
    #     fwrite.write(res)
    return res  # returns the byte array

def decrypt_message(ciphertext, d, n, integer_mode=False):
    if not integer_mode:
        cipher_int = int.from_bytes(ciphertext, byteorder='little')
    else:
        cipher_int = ciphertext
    plaintext = square_multiply(cipher_int, d, n)
    res = plaintext.to_bytes((plaintext.bit_length() + 7) // 8, byteorder='little')
    return res

def convert_to_bytes(integer_val):
    return integer_val.to_bytes((integer_val.bit_length() + 7) // 8, byteorder='little')


if __name__=="__main__":
    #### Submission for part 1.1, simple encryption ####

    # Step 1 : Extract the keys
    print('Part I-------------')

    pubkey, privkey = open('mykey.pem.pub','r').read(), open('mykey.pem.priv','r').read()
    rsakey_pub, rsakey_priv = RSA.importKey(pubkey), RSA.importKey(privkey)

    # Step 2: Encrypt using the pubkey (digital signature style)
    with open('message.txt', 'r') as fptr:
        msg = fptr.read().encode()
        fptr.close()
    print('\nContent of file read (bytes):', msg)
    ciphertext = encrypt_message(msg, rsakey_pub.e, rsakey_pub.n)
    print('\nEncrypted message given by (in bytes):', ciphertext)

    # Step 3 : Decrypt the message

    decrypted_plaintext = decrypt_message(ciphertext, rsakey_priv.d, rsakey_priv.n)
    print('\nDecrypted message given by (in bytes) :', decrypted_plaintext)

    #### Submission for part 1.2, signature ####

    # Step 1: We first hash the message
    with open('message.txt', 'r') as fptr:
        hashed_msg = SHA256.new(fptr.read().encode())
        fptr.close()
    print('\nHashed digest given by :', hashed_msg.digest())

    # Step 2  - apply decryption on the hash
    hashed_to_bytes = hashed_msg.digest()
    signed_hash = decrypt_message(hashed_to_bytes, rsakey_priv.d, rsakey_priv.n)

    # Step 3, verify the signature
    verified_hash = encrypt_message(signed_hash, rsakey_pub.e, rsakey_pub.n)
    assert (verified_hash == hashed_to_bytes)
    print('Verified hash to be :', verified_hash)
    print('Verification is SUCCESFUL')


    #### Submission for part 2.1, RSA Encryption Protocol Attack ####
    print('\nPart II-------------')
    print('---- Executing RSA Encryption Protocol Attack ----')
    # Step 1: we first encrypt the number 100
    integer_choice_1 = 100
    print('Encrypting: ', integer_choice_1 )
    encrypted_integer_1 = encrypt_message(integer_choice_1, rsakey_pub.e, rsakey_pub.n, integer_mode=True)
    print('Result:')
    print(b64encode(encrypted_integer_1).decode())

    # Step 2: To achieve encrypted value for number 200, we multiply the integer value of encrypted text
    multiplier_value = 2
    y_s = encrypt_message(multiplier_value, rsakey_pub.e, rsakey_pub.n, integer_mode=True)
    print('Modified to:')
    # TODO: Do we remove modn? Either way is fine lol
    encrypted_integer_2 = (int.from_bytes(encrypted_integer_1, byteorder='little') * ((int.from_bytes(y_s, byteorder='little') ) % rsakey_pub.n))
    print(b64encode(convert_to_bytes(encrypted_integer_2)).decode())
    decrypted_integer_2 = decrypt_message(encrypted_integer_2, rsakey_priv.d, rsakey_priv.n, integer_mode=True)
    print('\nDecrypted: ', int.from_bytes(decrypted_integer_2, byteorder='little'))

    #### Submission for part 2.2, RSA Digital Signature Protocol Attack ####
    print('---- Executing RSA Digital Signature Attack ----')

    # Generate a random signature S
    random_signature = 'garbagestuff'.encode()
    # Generate a new digest from the signature using pubkey
    existential_message = encrypt_message(random_signature, rsakey_pub.e, rsakey_pub.n)
    print('Created existential attack message: ', existential_message)
    # Attempts to verify the digital signature
    assert(encrypt_message(random_signature, rsakey_pub.e, rsakey_pub.n) == existential_message)
    print('Valid signature confirmed, passed assert')











