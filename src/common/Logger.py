#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

class Logger:

    def __init__(self, log_path, level):

        # set the logger
        self.log_level = level
        self.log_path = log_path

        self.logger = logging.getLogger('weather')
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

        self.logger.info('weather init over.')

    

