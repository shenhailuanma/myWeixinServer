#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import json
import urllib
import urllib2

from common.Database import Database
from weather import weather

class update_weather_data:

    def __init__(self, city):

        self.city = city

        # set the logger
        self.log_level = logging.DEBUG
        self.log_path = '/var/log/update_weather_data.log'

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
        self.weather  = weather()

        self.logger.debug('update_weather_data init over.')

    def update(self):
        try:

            # get weather data use weather class
            data = self.weather.get_weather_by_city(city)
            
            # check the weather data if exist, if not to insert it.
            db_weather_data = self.database.get_weather_data(city)
            self.logger.debug('weather_data from database:%s.' %(db_weather_data))

            if db_weather_data != None:
                # update weather data
                
            else:
                # insert weather data


        except Exception,ex:
            self.logger.error('update_weather_data error:{0}'.format(str(ex)))


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


    city_list = [u"北京",u"上海"]
    handle = update_weather_data(city_list)
    #for city in city_list:
    #    handle = update_weather_data(city)
    #    handle.update()