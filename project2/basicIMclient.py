import socket
import sys
import argparse
import select


def basicIMclient(s, n):
    print("servername: %s | nickname: %s" % (s, n))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((s, 9999))

    # here are the things we want to read from
    read_handles = [ sys.stdin, sock ]

    while True:
        # this statement is super important... it's the crux of the whole
        # thing.  In a nutshell, it waits/blocks until there's data to
        # read from ANY (and potentially more than one) of the elements
        # defined in read_handles
        ready_to_read_list, _, _ = select.select(read_handles, [], [])

        # if we get here, then there's something to read.  we just need
        # to figure out what
        
        if sys.stdin in ready_to_read_list:
            # we have new data from STDIN...
            # ...so let's actually read it!
            user_input = input()
            # and let's send to the connected party
            sock.send( (user_input + "\n").encode('utf-8') )

        if sock in ready_to_read_list:
            # we have new data from the network!
            # ... so let's print it out
            data = sock.recv(1024)
            if len(data) == 0:
                print( "Bye!" )
                exit(0)
            print( data )


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--servername', dest='servername', help='IP or hostname of the machine that is already running the BasicIM server', required=True)
    parser.add_argument('-n', '--nickname', dest='nickname', help='nickname or alias chosen by the user', required=True)
    args = parser.parse_args()

    basicIMclient(args.servername, args.nickname)