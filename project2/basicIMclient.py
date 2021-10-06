import socket
import argparse


def basicIMclient(s, n):
    pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--servername', dest='servername', help='IP or hostname of the machine that is already running the BasicIM server', required=True)
    parser.add_argument('-n', '--nickname', dest='nickname', help='nickname or alias chosen by the user', required=True)
    args = parser.parse_args()

    basicIMclient(args.servername, args.nickname)