import socket
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', dest='port', help='port on which service will listen on', required=True, type=int)
    parser.add_argument('-r', '--reverse', dest='reverse', help='reverse the message sent through server', action='store_true')
    args = parser.parse_args()
    
    print("Welcome!")
    print("Listening on port %d" % args.port)
    if args.reverse is True:
        print("You specified the -r or --reverse option")
    else:
        print("You did not specify the -r or --reverse option")