
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urllib
import urllib2
import logging
import json


class Transcode(object):
    """docstring for Transcode"""
    def __init__(self, ip, port, token):
        super(Transcode, self).__init__()

        self.ip = ip
        self.port = port
        self.token = str(token)

        self.url = "http://%s:%s/api" %(ip, port)

        # set the logger
        self.log_level = logging.DEBUG
        self.log_path = 'transcode.log'

        self.logger = logging.getLogger('transcode')
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

        self.logger.info('url:%s.' %(self.url))
        self.logger.info('transcode init over.')
        
    def transcode_system_status(self):
        

        try:
            params = {}
            params['token'] = self.token
            params['method'] = "transcode_system_status"
            params_string = json.dumps(params)
            self.logger.debug('transcode_system_status params:{0}'.format(params_string))

            ret = self.http_post(self.url, params_string)
            if ret == None:
                response = {}
                response['result'] = 'error'
                return response

            return ret

        except Exception,ex:
            response = {}
            response['result'] = 'error'
            return response


    # create transcode task
    def create_task(self):

        return None

    def http_post(self, url, data="", timeout=3):

        maxTryTimes = 1

        try_times = 0

        while try_times < maxTryTimes:
            try:
                req = urllib2.urlopen(url, data, timeout);
            except Exception,ex:
                try_times += 1
                self.logger.info("try_times:%s, post data:%s." %(try_times,data))

                if try_times >= maxTryTimes:
                    #self.logger.log_exception("[worker.__http_post] error: %s" %(ex))
                    return None

                continue
            
            return req.read()

        return None


if __name__ == "__main__":
    transcode = Transcode("0.0.0.0", 9999, "40dde18cc14211e6")

    print transcode.transcode_system_status()
