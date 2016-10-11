#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import os,sys,logging


def log(log_file_name):
    '''
    日志记录
    :param log_file_name: 日志文件
    :return:
    '''
    handler = logging.FileHandler(log_file_name, "a", encoding="UTF-8")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s", '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
    return root_logger
