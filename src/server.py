#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import json
import urllib
import urllib2
from datetime import datetime

import bottle

from wechat_sdk import WechatBasic 
from weather import weather

from common.Database import Database

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


        # weixin about
        self.appid      = 'wxb1efccbbb5bafcbb'
        self.appsecret  = '9d64356f48062e46159b4d179dea5c44'
        self.token      = 'shenhailuanma'
        self.access_token = ''
        self.signature  = None
        self.echostr    = None
        self.timestamp  = None
        self.nonce      = None

        self.wechat     = WechatBasic(token=self.token, appid=self.appid, appsecret=self.appsecret)

        self.weather    = weather()

        # database
        self.database   = Database()

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
        def index_get():
            try:
                # get the post data
                self.logger.debug('handle a GET request: /, ')

                # e.g :  /?signature=04d39d841082682dc7623945528d8086cc9ece97&echostr=8242236714827861439&timestamp=1440564411&nonce=2061393952

                # get the data
                self.logger.debug('handle the request data: %s' %(bottle.request.query_string))
                #self.logger.debug('handle the request signature:%s' %(bottle.request.query.signature))
                #self.logger.debug('handle the request echostr:%s' %(bottle.request.query.echostr))
                #self.logger.debug('handle the request timestamp:%s' %(bottle.request.query.timestamp))
                #self.logger.debug('handle the request nonce:%s' %(bottle.request.query.nonce))

                return bottle.request.query.echostr
            except Exception,ex:
                return "%s" %(ex)


            return "Hello, this is myWeixinServer."


        @bottle.route('/', method="POST")
        def index_post():
            try:
                response = ''

                self.logger.debug('handle a POST request: /, ')
                self.logger.debug('handle the request data: %s' %(bottle.request.query_string))

                post_data = bottle.request.body.getvalue()
                self.logger.debug('handle the request post data: %s' %(post_data))

                echostr     = bottle.request.query.echostr
                signature   = bottle.request.query.signature
                timestamp   = bottle.request.query.timestamp
                nonce       = bottle.request.query.nonce

                if self.wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
                    self.logger.debug('check_signature ok.')

                    self.wechat.parse_data(post_data)

                    message = self.wechat.get_message()

                    if message.type == 'text':
                        if message.content == 'wechat':
                            response = self.wechat.response_text(u'^_^')
                        elif u'天气' in message.content:
                            city = u'北京'
                            data = self.database.get_weather_data(city)
                            self.logger.debug('get the weather response:{0}'.format(data))
                            response = self.wechat.response_text(data)
                        else:
                            response = self.wechat.response_text(u'文字')

                    elif message.type == 'image':
                        response = self.wechat.response_text(u'图片')
                    elif message.type == 'video':
                        self.logger.debug('message.media_id:%s' %(message.media_id))
                        response = self.wechat.download_media(message.media_id)
                        self.logger.debug('message.media_id:%s over' %(message.media_id))
                        #response = self.wechat.response_text(u'视频')
                    elif message.type == 'voice':
                        response = self.wechat.response_text(u'音频')
                    elif message.type == 'location':
                        response = self.wechat.response_text(u'位置')
                    else:
                        response = self.wechat.response_text(u'未知')


                

                return response
            except Exception,ex:
                self.logger.debug('error:%s' %(ex))
                return "%s" %(ex)

        @bottle.route('/images/:filename')
        def send_image(filename=None):
            # FIXME: the param 'root' should be define in other place, now just for test.
            root_path = "%s/images" %(self.dir_path)
            return bottle.static_file(filename, root=root_path)

        @bottle.route('/videos/:filename')
        def send_video(filename=None):
            # FIXME: the param 'root' should be define in other place, now just for test.
            root_path = "%s/videos" %(self.dir_path)
            return bottle.static_file(filename, root=root_path)


        @bottle.error(404)
        def error404(error):
            return "Nothing here, sorry."

        #################
        #API
        #################
        @bottle.route('/api/gettime')
        def gettime():
            return "%s" %(datetime.now())

        @bottle.route('/api/get/access_token')
        def update_access_token():
            access_token = self.get_access_token()

            return "%s" %(access_token)


    def run(self):
        bottle.run(host=self.ip, port=self.port, debug=True)


    def get_access_token(self):
        try:
            access_token = self.database.get_access_token(self.appid, self.appsecret)
            return access_token
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
    server = Server('0.0.0.0', 80, logging.DEBUG)
    server.run()

else:
    #os.chdir(os.path.dirname(__file__))
    server = Server('0.0.0.0', 9000, logging.DEBUG)
    application = bottle.default_app()