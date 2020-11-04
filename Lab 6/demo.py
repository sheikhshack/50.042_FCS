# Sheikh Salim 1003367
#50.042 FCS Lab 6 template

# This is the demo for the present algo

import ecb
import dhke_template


# first we setup dhke
while True:
    print('Negotiating shared key of length 80 ...')
    p, alpha = dhke_template.dhke_setup(80)
    sender_private_key = dhke_template.gen_priv_key(p)
    sender_public_key = dhke_template.get_pub_key(alpha, sender_private_key, p)

    rcvr_private_key = dhke_template.gen_priv_key(p)
    rcvr_public_key = dhke_template.get_pub_key(alpha, rcvr_private_key, p)

    sender_shared_key = dhke_template.get_shared_key(rcvr_public_key, sender_private_key, p)
    rcvr_shared_key = dhke_template.get_shared_key(sender_public_key, rcvr_private_key, p)
    assert (sender_shared_key == rcvr_shared_key)

    # making sure key generated is length 80
    if sender_shared_key.bit_length() == 80:
        print('Negotiation successful \n')
        break

print('###### Details of key exchange as such ######')
print('Sender private key: ', sender_private_key)
print('Sender public key: ', sender_public_key)
print('Receiver private key: ', rcvr_private_key)
print('Receiver public key: ', rcvr_public_key)
print('Shared key given by: ', rcvr_shared_key, '===', sender_shared_key)
print()



# now we have keys ready, we proceed to do encryption
print('###### Entering encryption stage ######')

plaintext_message_sender = '(From message_to_send.txt) Hey there delilah, whats it like in New York City?'
print('Sender plaintext as such: ', plaintext_message_sender)
ecb.ecb('message_to_send.txt', 'encrypted_message.txt', sender_shared_key, 1)
print('Encrypted file generated: encrypted_message.txt')

print()
print('Simulating transmission of encrypted message over to receiver')
print()


# sender then proceeds to transmit the encrypted message to receiver here
############## WOOOOOOOOOOOOOOOOOOOOOOOSHHHHHHHHHH #######################
# receiver now receives the transmitted message
print('###### Entering decryption stage ######')
ecb.ecb('encrypted_message.txt', 'message_received_deciphered.txt', rcvr_shared_key, 0)
print('Decrypted file generated: message_received_deciphered.txt')

