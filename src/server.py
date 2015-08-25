#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import json

from datetime import datetime

import bottle


__author__ = 'shenhailuanma'
__version__ = '0.1.0'


class Server:
    def __init__(self, ip='0.0.0.0', port=9000, log_level=logging.DEBUG):

        self.ip   = ip
        self.port = port

        self.author  = __author__
        self.version = __version__

        self.file_path = os.path.realpath(__file__)
        self.dir_path  = os.path.dirname(self.file_path)


        # mark system start time
        self.system_initialized = datetime.now()


        # set the logger
        self.log_level = logging.DEBUG
        self.log_path = 'myWeixinServer.log'

        self.logger = logging.getLogger('myWeixinServer')
        self.logger.setLevel(self.log_level)

        # create a handler for write the log to file.
        fh = logging.FileHandler(self.log_path)
        fh.setLevel(self.log_level)

        # create a handler for print the log info on console.
        ch = logging.StreamHandler()
        ch.setLevel(self.log_level)

        # set the log format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # add the handlers to logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        self.logger.info('init over.')

    
        #######  web test ######
        @bottle.route('/')
        @bottle.route('/index')
        def index():
            return "Hello, this is myWeixinServer."

        @bottle.error(404)
        def error404(error):
            return "Nothing here, sorry."

        #################
        #API
        #################
        @bottle.route('/api/gettime')
        def gettime():
            return "%s" %(datetime.now())



    def run(self):
        bottle.run(host=self.ip, port=self.port, debug=True)



if __name__ == "__main__":
    server = Server('0.0.0.0', 9000, logging.DEBUG)
    server.run()

else:
    #os.chdir(os.path.dirname(__file__))
    server = Server('0.0.0.0', 9000, logging.DEBUG)
    application = bottle.default_app()