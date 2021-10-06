import select
import socket
import sys
import signal


def runServer():
    # create a socket FOR INCOMING CONNECTIONS
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # tell the computer on what port to listen to
    s.bind(('', 9999))

    # listens for multiple connections
    s.listen()

    # wait until we ACCEPT a connection from another host
    # and return a socket ("conn") we can use to talk to it

    client_conns = []

    while True:
        conn, addr = s.accept()
        print("Connection address: %s %d" % addr)
        client_conns.append((conn, addr))

if __name__ == '__main__':
    runServer()