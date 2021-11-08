import socket
from typing import Text
import numpy as np
import sys
import argparse
import select
import struct
import binascii
#import automator
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import HMAC, SHA256
from encrypted_package_pb2 import EncryptedPackage, PlaintextAndMAC, IM


def basicIMclient(servername, nickname, confkey, authkey, port):
    #print("servername: %s | nickname: %s" % (servername, nickname))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((servername, port))

    # here are the things we want to read from
    read_handles = [ sys.stdin, sock ]

    # first, take IM
    send_im = IM()
    send_im.nickname = nickname
    
    while True:
        ready_to_read_list, _, _ = select.select(read_handles, [], [])
        # if sys.stdin in ready_to_read_list
        # that means there is data in stdin to be read (aka the user must have hit enter)
        if sys.stdin in ready_to_read_list:
            # new data from STDIN
            user_input = input()
            if user_input.lower().strip() == "exit":
                exit(0)
            elif len(user_input) != 0:
                # encode input along with nickname using proto buffer
                send_im.message = user_input
                serialized_im = send_im.SerializeToString()

                # then we create a structure to hold the serialized IM along with a MAC
                plaintext_and_mac = PlaintextAndMAC()
                plaintext_and_mac.paddedPlaintext = pad(serialized_im, AES.block_size)
                # create SHA256 based mac using authkey
                h = HMAC.new(authkey.encode('utf-8'), digestmod=SHA256)
                h.update(plaintext_and_mac.paddedPlaintext)
                plaintext_and_mac.mac = h.digest()
                serialized_plaintext_and_mac = plaintext_and_mac.SerializeToString()

                # next, we create a structure to hold the encrypted plaintext+MAC along with an IV
                encrypted_package = EncryptedPackage()
                encrypted_package.iv = np.random.bytes(16)
                # To force the keys to be exactly 256 bits long, you can use the SHA-256
                # hash function on the arguments passed to -c and -a.
                cipher_key = HMAC.new(confkey.encode('utf-8'), digestmod=SHA256).digest()
                cipher = AES.new(cipher_key, AES.MODE_CBC, encrypted_package.iv)
                encrypted_package.encryptedMessage = cipher.encrypt(pad(serialized_plaintext_and_mac, 16))
                serialized_encrypted_package = encrypted_package.SerializeToString()
                
                # now that we have our final data structure to send over the wire
                #(serialized_encrypted_package), we need to send it.  First, we'll send
                # the length, and then the serialized structure
                length_of_encrypted_package = len(serialized_encrypted_package)
                packed_length_of_encrypted_package = struct.pack('!L',length_of_encrypted_package) # note this takes up 4 bytes (not 2)!

                sock.send( packed_length_of_encrypted_package )
                sock.send( serialized_encrypted_package )


        if sock in ready_to_read_list:
            # we have new data from the network!
            data_len_packed = sock.recv(4,socket.MSG_WAITALL)
            if len(data_len_packed) == 0:
                print("Server disconnected.")
                exit(0)
            data_len = struct.unpack('!L',data_len_packed)[0]
            serialized_encrypted_package = sock.recv(data_len,socket.MSG_WAITALL)
            try:
                encrypted_package = EncryptedPackage()
                encrypted_package.ParseFromString(serialized_encrypted_package)
                # need to obtain plaintext and mac from encrypted package
                #print( 'iv is %s' % binascii.hexlify(encrypted_package.iv))
                cipher_key = HMAC.new(confkey.encode('utf-8'), digestmod=SHA256).digest()
                cipher2 = AES.new(cipher_key, AES.MODE_CBC, encrypted_package.iv)
                serialized_plaintext_and_mac = unpad(cipher2.decrypt(encrypted_package.encryptedMessage), 16)
            except Exception as e:
                print( 'cannot decode EncryptedPackage: %s' % e )
            else:
                # deserialize plaintext and mac
                plaintext_and_mac = PlaintextAndMAC()
                try:
                    plaintext_and_mac.ParseFromString(serialized_plaintext_and_mac)
                except Exception as e:
                    print('cannot deserialize plaintext and mac: %s' % e)
                else:
                    # verify mac
                    h = HMAC.new(authkey.encode('utf-8'), digestmod=SHA256)
                    h.update(plaintext_and_mac.paddedPlaintext)
                    if h.digest() == plaintext_and_mac.mac:
                        # obtain serialized IM from plaintext_and_mac structure
                        serialized_im = unpad(plaintext_and_mac.paddedPlaintext, AES.block_size)
                        recv_im = IM()
                        recv_im.ParseFromString(serialized_im)
                        print("%s: %s" % (recv_im.nickname, recv_im.message))
                    else:
                        print("The message or key is not authentic.")
            


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--servername', dest='servername', help='IP or hostname of the machine that is already running the BasicIM server', required=True)
    parser.add_argument('-n', '--nickname', dest='nickname', help='nickname or alias chosen by the user', required=True)
    parser.add_argument('-c', '--confiendtiality-key', dest='confkey', help='confidentiality key used for AES-256-CBC', required=True)
    parser.add_argument('-a', '--authenticity-key', dest='authkey', help='key used to compute the SHA-256-based HMAC', required=True)
    parser.add_argument('-p', '--port', dest='port', help='port client will connect on', required=True, type=int)
    args = parser.parse_args()

    try:
        basicIMclient(args.servername, args.nickname, args.confkey, args.authkey, args.port)
    except KeyboardInterrupt:
        exit(0)