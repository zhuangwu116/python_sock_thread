# -*- coding: utf-8 -*-

import socket

HOST = '127.0.0.1'
PORT = 3214

s = socket.socket()

try:
    s.connect((HOST,PORT))
    data = "nihao!"
    while data:
        s.sendall(data.encode('utf-8'))
        data = s.recv(1024)
        print("Receive from Server:\n",data.decode('utf-8'))
        data = raw_input('Please input an info:\n')

except socket.error as err:
    print(err)
finally:
    s.close()
