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
    client_conns = []
    
    while True:
        # select will choose between getting data from network or server accepting new client connection
        # ready_to_read_list contains item(s) ready for processing/reading
        ready_to_read_list, _, _ = select.select(client_conns + [s], [], [])
        
        # check if a client is trying to connect
        if s in ready_to_read_list:
            (clientsocket, address) = s.accept() # server accepts client connection. It will not wait.
            #print("Client accepted at address %s %d" % address)
            client_conns.append(clientsocket) # add client to list of connected clients
            #print("Total clients: %d" % len(client_conns))
            ready_to_read_list.remove(s)

        for connection in ready_to_read_list:
            # there is data in the network ready to read
            # receive the data from network
            z = connection.recv(1280)
            if len(z) == 0:
                # recv returned 0 bytes
                #print("A client disconnected.")
                client_conns.remove(connection)
            else:
                for other_conn in client_conns:
                    if other_conn is not connection:
                        other_conn.send(z)
                #print(z)


if __name__ == '__main__':
    runServer()