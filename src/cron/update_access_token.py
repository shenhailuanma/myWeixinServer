#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import json
import urllib
import urllib2

from common.Database import Database

class update_access_token:

    def __init__(self, appid, appsecret):

        self.appid = appid
        self.appsecret = appsecret

        # set the logger
        self.log_level = logging.DEBUG
        self.log_path = '/var/log/update_access_token.log'

        self.logger = logging.getLogger('Token')
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



        self.database = Database()

        self.logger.debug('update_access_token init over.')

    def update(self):

        # get access_token from weixin
        access_token = self.get_access_token()
        
        # check the access_token if exist, if not to insert it.
        db_access_token = self.database.get_access_token(self.appid, self.appsecret)
        self.logger.debug('get_access_token from database:%s.' %(db_access_token))

        if db_access_token != None:
            # update access_token
            self.database.update_access_token(self.appid, self.appsecret, access_token)
        else:
            self.database.insert_access_token(self.appid, self.appsecret, access_token)






    def get_access_token(self):
        try:
            url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}".format(self.appid, self.appsecret)
            self.logger.debug('get_access_token request url:%s.' %(url))
            response = self.http_get(url, 5)
            if response != None:
                response_json = json.loads(response)
                if response_json.has_key('access_token') and len(response_json['access_token']) > 0:
                    return response_json['access_token']

            return None
        except Exception,ex:
            self.logger.error('get_access_token error:{0}'.format(str(ex)))
            return None

    def http_post(self, url, data="", timeout=5):

        try:

            maxTryTimes = 1

            try_times = 0

            while try_times < maxTryTimes:
                try:
                    headers = {}
                    headers['Accept'] = '*/*'
                    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
                    headers['Content-Type'] = 'application/json;text/plain;charset=UTF-8'
                    request = urllib2.Request(url=url, data=data, headers=headers)
                    request.add_header('Accept-encoding', 'gzip')

                    req = urllib2.urlopen(request,timeout=timeout)
                    

                    if req.info().get('Content-Encoding') == 'gzip':
                        self.logger.debug('Content-Encoding == gzip')
                        data = StringIO.StringIO(req.read())
                        gzipper = gzip.GzipFile(fileobj=data)
                        response = gzipper.read()
                    else:
                        response = req.read()

                except Exception,ex:
                    self.logger.error('urlopen error:{0}'.format(str(ex)))

                    try_times += 1
                    if try_times >= maxTryTimes:
                        return None
                    continue
                
                return response

            return None

        except Exception,ex:
            self.logger.error('urlopen error:{0}'.format(str(ex)))
            return None


    def http_get(self, url, timeout=5):
        return self.http_post(url, None, timeout)


if __name__ == "__main__":

    handle = update_access_token('wxb1efccbbb5bafcbb', '9d64356f48062e46159b4d179dea5c44')
    handle.update()