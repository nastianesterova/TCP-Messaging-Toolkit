import socket
import sys
import argparse
import select
import broadcastMsg_pb2


def basicIMclient(servername, nickname):
    #print("servername: %s | nickname: %s" % (servername, nickname))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((servername, 9999))

    # here are the things we want to read from
    read_handles = [ sys.stdin, sock ]

    send_message = broadcastMsg_pb2.Message()
    send_message.nickname = nickname
    rcv_message = broadcastMsg_pb2.Message()

    while True:
        ready_to_read_list, _, _ = select.select(read_handles, [], [])
        
        if sys.stdin in ready_to_read_list:
            # new data from STDIN
            user_input = input()
            if user_input.lower().strip() == "exit":
                exit(0)
            elif len(user_input) != 0:
                # encode input along with nickname using proto buffer
                send_message.message = user_input
                sock.send(send_message.SerializeToString())

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
    args = parser.parse_args()

    basicIMclient(args.servername, args.nickname)