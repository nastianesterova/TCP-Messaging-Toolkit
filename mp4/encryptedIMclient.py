import socket
import sys
import argparse
import select
import struct
import binascii
#import automator
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from encrypted_package_pb2 import EncryptedPackage, PlaintextAndMAC, IM


def basicIMclient(servername, nickname):
    #print("servername: %s | nickname: %s" % (servername, nickname))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((servername, 9999))

    # here are the things we want to read from
    read_handles = [ sys.stdin, sock ]

    # first, take IM
    im = IM()
    im.nickname = nickname
    
    while True:
        ready_to_read_list, _, _ = select.select(read_handles, [], [])
        
        if sys.stdin in ready_to_read_list:
            # new data from STDIN
            user_input = input()
            if user_input.lower().strip() == "exit":
                exit(0)
            elif len(user_input) != 0:
                # encode input along with nickname using proto buffer
                im.message = user_input
                serialized_im = im.SerializeToString()

                # then we create a structure to hold the serialized IM along with a MAC
                plaintext = PlaintextAndMAC()
                plaintext.paddedPlaintext = pad(serialized_im,AES.block_size)
                plaintext.mac = b'12345'        # I'll let you figure this out
                serialized_plaintext = plaintext.SerializeToString()

                # next, we create a structure to hold the encrypted plaintext+MAC along with an IV
                encrypted_package = EncryptedPackage()
                encrypted_package.iv = b'12345' # I'll let you figure this out
                #encrypted_package.encryptedMessage = do_encryption(key,serialized_plaintext)
                encrypted_package.encryptedMessage = serialized_plaintext # this needs to be encrypted; see above line
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
            data = sock.recv(1280)
            rcv_message = rcv_message.FromString(data)
            if len(data) == 0:
                exit(0)
            print("%s: %s" % (rcv_message.nickname, rcv_message.message))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--servername', dest='servername', help='IP or hostname of the machine that is already running the BasicIM server', required=True)
    parser.add_argument('-n', '--nickname', dest='nickname', help='nickname or alias chosen by the user', required=True)
    parser.add_argument('-c', '--confiendtiality-key', dest='confkey', help='confidentiality key used for AES-256-CBC', required=True)
    parser.add_argument('-a', '--authenticity-key', dest='authkey', help='key used to compute the SHA-256-based HMAC', required=True)
    parser.add_argument('-p', '--port', dest='port', help='port client will connect on', required=True)
    args = parser.parse_args()

    try:
        basicIMclient(args.servername, args.nickname)
    except KeyboardInterrupt:
        exit(0)