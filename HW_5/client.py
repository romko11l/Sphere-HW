#! /home/roman/anaconda3/bin/python3

import socket
import sys
import time


if __name__ == '__main__':
    """./client.py vk_id=139336630&format=json"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("", 10001))
        time.sleep(7)
        sock.send(bytes(sys.argv[1], encoding='UTF-8'))
        data = sock.recv(2048)
        print(data.decode("utf-8"))
    except ConnectionResetError:
        data = client.recv(2048)
        print(data.decode("utf-8"))
