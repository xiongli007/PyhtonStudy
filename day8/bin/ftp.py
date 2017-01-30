#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.client import Ftp_client


if __name__ == '__main__':
    run = Ftp_client()
    run.run()



# import socket
#
#
# ip_port = ('localhost',9999)
# sk = socket.socket()
# sk.connect(ip_port)
# sk.settimeout(5)
#
# while True:
#     data = sk.recv(1024)
#     print('receive:',data.decode())
#     inp = input('please input:')
#     sk.sendall(inp.encode())
#     if inp == 'exit':
#         break
#
# sk.close()