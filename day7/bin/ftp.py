#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.client import Ftp_client


if __name__ == '__main__':
    run = Ftp_client()
    run.login_in()

    if run.login_flag:
        run.cmd()
