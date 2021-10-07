import socket
import sys
import argparse
import select
import broadcastMsg_pb2


def basicIMclient(servername, nickname):
    print("servername: %s | nickname: %s" % (servername, nickname))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((servername, 9999))

    # here are the things we want to read from
    read_handles = [ sys.stdin, sock ]

    send_message = broadcastMsg_pb2.Message()
    send_message.nickname = nickname
    rcv_message = broadcastMsg_pb2.Message()

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
            # encode input along with nickname using proto buffer
            send_message.message = user_input
            # and let's send to the connected party
            sock.send(send_message.SerializeToString())

        if sock in ready_to_read_list:
            # we have new data from the network!
            data = sock.recv(1024)
            rcv_message = rcv_message.FromString(data)
            if len(data) == 0:
                print( "Bye!" )
                exit(0)
            print("%s: %s" % (rcv_message.nickname, rcv_message.message))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--servername', dest='servername', help='IP or hostname of the machine that is already running the BasicIM server', required=True)
    parser.add_argument('-n', '--nickname', dest='nickname', help='nickname or alias chosen by the user', required=True)
    args = parser.parse_args()

    basicIMclient(args.servername, args.nickname)