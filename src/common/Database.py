#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import MySQLdb
from datetime import datetime
import time
import logging

from config import config

class Database:

    def __init__(self, host=None, user=None, passwd=None, database=None, log_level=None, log_path=None):

        if host != None:
            self.mysqlHost = host
        else:
            self.mysqlHost = config.mysqlHost

        if  user != None:   
            self.mysqlUser = user
        else:
            self.mysqlUser = config.mysqlUser

        if  passwd != None:
            self.mysqlPassword = passwd
        else:
            self.mysqlPassword = config.mysqlPassword

        if  database != None:
            self.mysqlDatabase = database
        else:
            self.mysqlDatabase = config.mysqlDatabase    

        try:
            # set the logger
            if  log_level != None:
                self.log_level = log_level
            else:
                self.log_level = config.Database_log_level

            if  log_path != None:
                self.log_path = log_path
            else:  
                self.log_path = config.Database_log_path

            self.logger = logging.getLogger('Database')
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

            

            self.local_db = MySQLdb.connect(host=self.mysqlHost,
                user=self.mysqlUser, passwd=self.mysqlPassword, db=self.mysqlDatabase,
                charset="utf8")

            self.logger.info('Database init over.')

        except Exception,ex:
            self.logger.info('Database error:%s.' %(ex))
            exit(-1)

    def __connect_to_db(self):

        try:

            # ping the db, check the connect if active
            self.local_db.ping()
        except Exception,ex:
            self.logger.warning("local_db timeout:%s, now to reconnect." %ex)
            self.local_db = MySQLdb.connect(host=self.mysqlHost,user=self.mysqlUser, passwd=self.mysqlPassword, db=self.mysqlDatabase,charset="utf8")


        # create a cursor
        cursor = self.local_db.cursor()

        cursor.execute("SET NAMES utf8")

        self.local_db.commit()

        return cursor


    def __escape_tuple(self, *input_tuple):
        '''
        [private] escape all args.
        '''
        escaped_arr = [];
        
        for i in input_tuple:
            escaped_arr.append(MySQLdb.escape_string(str(i)));
        
        return tuple(escaped_arr);


    def __add_one_name_and_value(self, inlist, name, value):
        one_in = {}
        one_in['name']  = name
        one_in['value'] = value
        inlist.append(one_in)




    def __string_set_list(self,set_list):

        try:
            string_set_list = ''

            '''
                set_list format:
                [{"name":"port", "value":9090},{"name":"server","value":"10.33.0.123"}]
            '''
            set_cnt = 0
            for set_one in set_list:
                if set_cnt == 0:
                    if isinstance(set_one['value'], basestring):
                        string_set_list = "{0}='{1}'".format(set_one['name'],set_one['value'])
                    else:
                        string_set_list = "{0}={1}".format(set_one['name'],set_one['value'])
                    set_cnt += 1
                else:
                    if isinstance(set_one['value'], basestring):
                        string_set_list = "{0},{1}='{2}'".format(string_set_list, set_one['name'], set_one['value'])
                    else:
                        string_set_list = "{0},{1}={2}".format(string_set_list, set_one['name'],set_one['value'])

            return 'success',string_set_list
        except Exception,ex:
            return 'error',str(ex)


    def __string_where_list(self,where_list):

        try:
            string_where_list = ''

            '''
                where_list format:
                [{"name":"port", "value":9090},{"name":"server","value":"10.33.0.123"}]
            '''
            where_cnt = 0
            for where_one in where_list:
                if where_cnt == 0:
                    if isinstance(where_one['value'], basestring):
                        string_where_list = "{0}='{1}'".format(where_one['name'],where_one['value'])
                    else:
                        string_where_list = "{0}={1}".format(where_one['name'],where_one['value'])
                    where_cnt += 1
                else:
                    if isinstance(where_one['value'], basestring):
                        string_where_list = "{0} and {1}='{2}'".format(string_where_list, where_one['name'], where_one['value'])
                    else:
                        string_where_list = "{0} and {1}={2}".format(string_where_list, where_one['name'],where_one['value'])

            return 'success',string_where_list
        except Exception,ex:
            return 'error',str(ex)

    def __string_value_list(self,value_list):

        try:
            string_name_list = ''
            string_value_list = ''

            '''
                value_list format:
                [{"name":"port", "value":9090},{"name":"server","value":"10.33.0.123"}]
            '''
            value_cnt = 0
            for value_one in value_list:

                if value_cnt == 0:
                    string_name_list = "{0}".format(value_one['name'])
                    if isinstance(value_one['value'], basestring):
                        string_value_list = "'{0}'".format(value_one['value'])
                    else:
                        string_value_list = "{0}".format(value_one['value'])
                    value_cnt += 1
                else:
                    string_name_list = "{0},{1}".format(string_name_list, value_one['name'])
                    if isinstance(value_one['value'], basestring):
                        string_value_list = "{0},'{1}'".format(string_value_list, value_one['value'])
                    else:
                        string_value_list = "{0}, {1}".format(string_value_list, value_one['value'])

            return 'success',string_name_list,string_value_list
        except Exception,ex:
            return 'error',str(ex),str(ex)



    def db_update_common(self, table_name, set_list, where_list):
        result = 'error'

        try:

            result,set_list_string = self.__string_set_list(set_list)
            if result != 'success':
                self.logger.error("db_update_common, __string_set_list error:%s" %set_list_string)
                return result,set_list_string    


            result,where_list_string = self.__string_where_list(where_list)
            if result != 'success':
                self.logger.error("db_update_common, __string_where_list error:%s" %where_list_string)
                return result,where_list_string  


            conn = None;
            conn = self.__connect_to_db()
            
            sql = "UPDATE {0} SET {1} WHERE {2};".format(table_name, set_list_string, where_list_string)

            self.logger.debug("[db_update_common]%s" %(sql));
            conn.execute(sql);
            self.local_db.commit();

            if conn is not None:
                conn.close(); 

            result = 'success'
            return result,'success'
        except Exception,ex:
            if conn is not None:
                conn.close()
            self.local_db.rollback()

            msg = "error:%s." %(str(ex))
            self.logger.warning("db_update_common, %s" %msg)
            return result,msg    

    def db_delete_common(self, table_name, where_list):
        result = 'error'

        try:

            result,where_list_string = self.__string_where_list(where_list)
            if result != 'success':
                self.logger.error("db_delete_common, __string_where_list error:%s" %where_list_string)
                return result,where_list_string  


            conn = None;
            conn = self.__connect_to_db()
            
            sql = "DELETE FROM {0} WHERE {1};".format(table_name,  where_list_string)

            self.logger.debug("[db_delete_common]%s" %(sql));
            conn.execute(sql);
            self.local_db.commit();

            if conn is not None:
                conn.close(); 

            result = 'success'
            return result,'success'
        except Exception,ex:
            if conn is not None:
                conn.close()
            self.local_db.rollback()

            msg = "error:%s." %(str(ex))
            self.logger.warning("db_delete_common, %s" %msg)
            return result,msg  

    def db_insert_common(self, table_name, value_list):
        result = 'error'

        try:

            result, name_list_string, value_list_string = self.__string_value_list(value_list)
            if result != 'success':
                self.logger.error("db_insert_common, __string_where_list error:%s" %name_list_string)
                return result,name_list_string  


            conn = None;
            conn = self.__connect_to_db()
            
            sql = "INSERT INTO {0}({1})  VALUES({2});".format(table_name, name_list_string, value_list_string)

            self.logger.debug("[db_insert_common]%s" %(sql));
            conn.execute(sql);
            self.local_db.commit();

            if conn is not None:
                conn.close(); 

            result = 'success'
            return result,'success'
        except Exception,ex:

            self.local_db.rollback()

            msg = "error:%s." %(str(ex))
            self.logger.warning("db_insert_common, %s" %msg)
            return result,msg            


    def get_access_token(self, appid, appsecret):

        try:
            result = None
            conn = None
            conn = self.__connect_to_db()

            sql = "SELECT access_token FROM access_token WHERE appid='{0}' AND appsecret='{1}';".format(appid, appsecret)
            self.logger.debug("[get_access_token] sql:%s" %(sql))

            conn.execute(sql)
            dataset = conn.fetchall()

            for row in dataset:
                result = row[0]

            if conn is not None:
                conn.close(); 
            
            return result

        except Exception,ex:
            self.local_db.rollback()
            msg = "error:%s." %(str(ex))
            self.logger.warning("get_access_token, %s" %msg)
            return None


    def update_access_token(self, appid, appsecret, access_token):

        where_list = []
        self.__add_one_name_and_value(where_list, "appid", appid)
        self.__add_one_name_and_value(where_list, "appsecret", appsecret)

        set_list = []
        self.__add_one_name_and_value(set_list, "access_token", access_token)
        self.__add_one_name_and_value(set_list, "update_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        result,msg = self.db_update_common('access_token', set_list, where_list)
        return result,msg

    def insert_access_token(self, appid, appsecret, access_token):

        value_list = []
        self.__add_one_name_and_value(value_list, "appid", appid)
        self.__add_one_name_and_value(value_list, "appsecret", appsecret)
        self.__add_one_name_and_value(value_list, "access_token", access_token)
        self.__add_one_name_and_value(value_list, "update_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        result,msg = self.db_insert_common('access_token', value_list)
        return result,msg


    def get_weather_data(self, city):

        try:
            result = None
            conn = None
            conn = self.__connect_to_db()

            sql = "SELECT data FROM weather_data WHERE city='{0}';".format(city)
            self.logger.debug("[get_weather_data] sql:%s" %(sql))

            conn.execute(sql)
            dataset = conn.fetchall()

            for row in dataset:
                result = row[0]

            if conn is not None:
                conn.close(); 
            
            return result

        except Exception,ex:
            msg = "error:%s." %(str(ex))
            self.logger.warning("get_weather_data, %s" %msg)
            return None

    def update_weather_data(self, city, data):

        where_list = []
        self.__add_one_name_and_value(where_list, "city", city)

        set_list = []
        self.__add_one_name_and_value(set_list, "data", data)
        self.__add_one_name_and_value(set_list, "update_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        result,msg = self.db_update_common('weather_data', set_list, where_list)
        return result,msg

    def insert_weather_data(self, city, data):

        value_list = []
        self.__add_one_name_and_value(value_list, "city", city)
        self.__add_one_name_and_value(value_list, "data", data)
        self.__add_one_name_and_value(value_list, "update_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        result,msg = self.db_insert_common('weather_data', value_list)