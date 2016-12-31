#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.server import Ftpserver


if __name__ == '__main__':
    server_ftp = Ftpserver()

    while True:
        server_ftp.run()
