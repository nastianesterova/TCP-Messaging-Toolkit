import socket
import argparse

# Building an echo server.
# Echo service will listen on a user-specified port.
# When a client connects to your echo service on this port, your service will send back to the client
# any data it receives.
# Your service should continue to echo back until the client closes the connection.
# Your code should support "reverse" mode - the reverse of the received data is returned to the client.
# Your recv buffer should be at least 1024 bytes.
# After the client closes the connection, your echo service should go back to its wait state, where it awaits a
# new connection for a client.

def echo_service(port, reverse):
    print("Port: %d" % port)
    if(reverse):
        print("reverse")
    else:
        print("no reverse")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), port))
    s.listen(1)
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((socket.gethostname(), port))
        sock.send(b"hey")
        (clientsocket, address) = s.accept()
        z = clientsocket.recv(1024)
        if(reverse):
            print(z[::-1])
            clientsocket.send(z[::-1])
        else:
            print(z)
            clientsocket.send(z)


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

    echo_service(args.port, args.reverse)