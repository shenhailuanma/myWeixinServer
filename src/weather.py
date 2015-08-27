#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib2

class weather:

    def __init__(self):
        self.api_url = u'http://wthrcdn.etouch.cn/weather_mini?city='

    def get_weather_by_city(self, city):
        url = self.api_url + city
        ret = self.http_get(url)

        if ret == None:
            ret = 'no data.'

        return ret

    def http_post(self, url, data="", timeout=5):

        maxTryTimes = 1

        try_times = 0

        while try_times < maxTryTimes:
            try:
                headers = {}
                headers['Accept'] = '*/*'
                headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
                headers['Content-Type'] = 'application/json;text/plain;charset=UTF-8'
                request = urllib2.Request(url=url, data=data, headers=headers)
                

                req = urllib2.urlopen(request,timeout=timeout)
            except Exception,ex:
                if try_times >= maxTryTimes:
                    return None
                continue
            
            return req.read()

        return None

    def http_get(self, url, timeout=5):
        return self.http_post(url, timeout)
