# Sheikh 1003367 - Lab 7 RSA


from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256
from base64 import b64decode,b64encode


def generate_RSA(bits=1024):
    key = RSA.generate(bits, e=1613136604210069224422792925)
    print(key.e)
    private_key = key
    public_key = key.publickey()
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
    return integer_val.to_bytes((integer_val.bit_length() + 7) // 8, byteorder='little')

def convert_to_int(b64bytes):
    return int.from_bytes(b64decode(b64bytes), byteorder='little')

def multiply_with_mod(public_key_file, ciphertext1, ciphertext2):
    # Both ciphers are currently in base64 format
    rsa_pubkey = RSA.importKey(open(public_key_file, 'r').read())
    m = convert_to_bytes((convert_to_int(ciphertext1) * convert_to_int(ciphertext2)) % rsa_pubkey.n)
    return b64encode(m)




if __name__=="__main__":
    priv_key, pub_key = generate_RSA(1024)
    print('-- Private Key deets')
    print('n is', priv_key.n)
    print('d is', priv_key.d)

    print('-- Public Key deets')
    print('n is', pub_key.n)
    print('e is', pub_key.e)








