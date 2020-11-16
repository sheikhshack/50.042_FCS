import RSA_part1
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256
from base64 import b64decode,b64encode


def generate_RSA(bits=1024):
    key = RSA.generate(bits)
    private_key = key.exportKey('PEM')
    public_key = key.publickey().exportKey('PEM')
    with open('friendkey.pem.priv', 'wb') as fpvt, open('friendkey.pem.pub', 'wb') as fpub:
        fpvt.write(private_key)
        fpub.write(public_key)

    return private_key, public_key

def encrypt_RSA(public_key_file, message):
    rsa_pubkey = RSA.importKey(open(public_key_file, 'r').read())
    cipher = PKCS1_OAEP.new(rsa_pubkey)
    ciphertext = b64encode(cipher.encrypt(message))
    return ciphertext

def decrypt_RSA(private_key_file,cipher):
    rsa_privkey = RSA.importKey(open(private_key_file, 'r').read())
    de_cipher = PKCS1_OAEP.new(rsa_privkey)
    plaintext = de_cipher.decrypt(b64decode(cipher))
    return plaintext

def sign_data(private_key_file,data):
    rsa_privkey = RSA.importKey(open(private_key_file, 'r').read())
    cipher = PKCS1_PSS.new(rsa_privkey)
    hashed_message = SHA256.new(data)
    signature = b64encode(cipher.sign(hashed_message))
    return signature

def verify_sign(public_key_file,sign,data):
    rsa_pubkey = RSA.importKey(open(public_key_file, 'r').read())
    verifier = PKCS1_PSS.new(rsa_pubkey)

    hashed_message = SHA256.new(data)
    if verifier.verify(hashed_message, b64decode(sign)):
        return True
    else:
        return False

# Helper function for attack
def convert_to_bytes(integer_val):
    return integer_val.to_bytes((integer_val.bit_length() + 7) // 8, byteorder='big')

def convert_to_int(b64bytes):
    return int.from_bytes(b64decode(b64bytes), byteorder='big')

def multiply_with_mod(public_key_file, ciphertext1, ciphertext2):
    # Both ciphers are currently in base64 format
    rsa_pubkey = RSA.importKey(open(public_key_file, 'r').read())
    m = convert_to_bytes((convert_to_int(ciphertext1) * convert_to_int(ciphertext2)) % rsa_pubkey.n)
    return b64encode(m)




if __name__=="__main__":
    # Not sure how to show with a friend, so Ill just demo the whole exchange here
    print('--------- Demo 1 - Encryption & Decryption')
    # print('\nGenerating keys... (if doesnt exist')
    # generate_RSA(1024)
    with open('message.txt', 'r') as fptr:
        msg = fptr.read().encode()

    # Encrypt the message with pubkey (Acting as friend)
    print('Simulating: Friend encrypts message with my public key')
    encrypted_text = encrypt_RSA('mykeyNew.pem.pub', msg)
    print('Encrypted text: ', encrypted_text.decode())
    print('Decrypting the message with my own private key...')
    decrypted_text = decrypt_RSA('mykeyNew.pem.priv', encrypted_text)
    print('Decrypted text: ', decrypted_text.decode())

    print('\n--------- Demo 2 - Data and Signature')
    # signature = sign_data('friendkey.pem.priv', msg)
    # with open('friend.sign', 'wb') as fren:
    #     fren.write(signature)

    with open('friend.sign') as fren:
        friends_signature = fren.read()
    print('Friend sent me the file friend.sign as his signature for the file message.txt: ', friends_signature)

    print('Verifying friends signature with his pubkey...')
    verified_status = verify_sign('friendkey.pem.pub', friends_signature, msg)
    print('Verified: ', verified_status)


    ## Demoing the attacks in part 3
    print('\n--------- Demo 3 - Attacks for new RSA Implementation ')

    print('#### Running the RSA Encryption Protocol Attack')
    # Step 1: we first encrypt the number 100
    integer_choice_1 = 100
    print('Encrypting: ', integer_choice_1)
    encrypted_integer_1 = encrypt_RSA('mykey.pem.pub', convert_to_bytes(integer_choice_1))
    print('Result of initial encryption:')
    print(encrypted_integer_1.decode())

    # Step 2: To achieve encrypted value for number 200, we multiply the integer value of encrypted text
    multiplier_value = 2
    y_s = encrypt_RSA('mykey.pem.pub', convert_to_bytes(multiplier_value))
    print('Modified to:')
    encrypted_integer_2 = multiply_with_mod('mykey.pem.pub', encrypted_integer_1, y_s)
    print(b64encode(encrypted_integer_2).decode())
    try:
        decrypted_integer_2 = decrypt_RSA('mykey.pem.priv', encrypted_integer_2)
        print('Decrypted: ', decrypted_integer_2)
    except ValueError:
        print('Attack failed miserably. Decryption fails the integrity check inbuilt.')


    #### Submission for part 2.2, RSA Digital Signature Protocol Attack ####
    print('\n#### Running the RSA Digital Signature Protocol Attack')
    # Generate a random signature S
    random_signature = 'garbagestuff'.encode()
    print('Created Random Signature: ', random_signature)

    # Generate a new digest from the signature using pubkey
    existential_message = b64decode(encrypt_RSA('mykey.pem.pub', random_signature))
    print('Created existential attack message: ', existential_message)
    # Attempts to verify the digital signature
    if verify_sign('mykey.pem.pub', random_signature, existential_message):
        print('Valid signature detected')
    else:
        print('Signature verification failed miserably')








