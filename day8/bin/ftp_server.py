#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import os, sys, socketserver
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.server import MyServer
from conf import setting

if __name__ == '__main__':
    # ip_port = tuple((modules.GetConfig('server','ip'),int(modules.GetConfig('server','port'))))
    print('FTP server 已启动...')
    server = socketserver.ThreadingTCPServer((setting.SERVER_IP, setting.SERVER_PORT), MyServer)
    server.serve_forever()
