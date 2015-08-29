#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys;
# set the default encoding to utf-8
# reload sys model to enable the getdefaultencoding method. 
reload(sys);
# using exec to set the encoding, to avoid error in IDE.
exec("sys.setdefaultencoding('utf-8')");
assert sys.getdefaultencoding().lower() == "utf-8";


import os
import urllib
import urllib2
import logging
import json

from datetime import datetime
import gzip
import StringIO


class weather:

    def __init__(self):
        self.api_url = u'http://wthrcdn.etouch.cn/weather_mini'

        # set the logger
        self.log_level = logging.DEBUG
        self.log_path = 'weather.log'

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

    def get_weather_by_city(self, city):

        try:
            self.logger.debug('weather api_url:{0}'.format(self.api_url))
            params = {}
            params['city'] = u'北京'
            #params_string = urllib.urlencode(params)
            #self.logger.debug('weather params:{0}'.format(params_string))

            #get_url = "{0}?{1}".format(self.api_url, params_string)
            get_url = u'http://wthrcdn.etouch.cn/weather_mini?city=%E5%8C%97%E4%BA%AC'
            #get_url = u'http://php.weather.sina.com.cn/xml.php?city=%B1%B1%BE%A9&password=DJOYnieT8234jlsK&day=0'

            self.logger.debug('weather api url:{0}'.format(get_url))

            ret = self.http_post(get_url,None,1)
            if ret == None:
                return 'no data.'

            ret_json = json.loads(ret)

            month = datetime.now().strftime("%m")
            date = ret_json['data']['forecast'][0]['date']
            ganmao = ret_json['data']['ganmao']
            high = ret_json['data']['forecast'][0]['high']
            low  = ret_json['data']['forecast'][0]['low']
            day_type = ret_json['data']['forecast'][0]['type']

            response = u"今天是{0}月{1},{2},{3},{4},{5}".format(month, date,day_type, high, low, ganmao)
  
            return response
        except Exception,ex:
            self.logger.error('get_weather_by_city error:{0}'.format(str(ex)))
            return str(ex)


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
