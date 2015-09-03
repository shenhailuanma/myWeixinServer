#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging

class config:

    # server configs
    server_log_path = '/var/log/myWeixinServer.log'


    # database configs
    mysqlHost = 'localhost'
    mysqlUser = 'root'
    mysqlPassword = 'tvierocks'
    mysqlDatabase = 'myweixin'
    Database_log_path = server_log_path
    Database_log_level = logging.DEBUG





