#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from datetime import timedelta
import MySQLdb

from common.Database import Database


class clean_up_database:


    def __init__(self, mysqlHost, mysqlUser, mysqlPassword, mysqlDatabase):

        # save days
        self.save_days = 5

        # set the logger
        self.log_level = logging.DEBUG
        self.log_path = '/var/log/clean_up_database.log'

        self.logger = logging.getLogger('clean_up_database')
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

        # connect database
        self.local_db = None
        self.mysqlHost = mysqlHost
        self.mysqlUser = mysqlUser
        self.mysqlPassword = mysqlPassword
        self.mysqlDatabase = mysqlDatabase

        self.logger.debug("mysqlHost:%s, mysqlUser:%s, mysqlPassword:%s, mysqlDatabase:%s." 
            %(mysqlHost, mysqlUser, mysqlPassword, mysqlDatabase))

        self.local_db = MySQLdb.connect(host=mysqlHost,user=mysqlUser, passwd=mysqlPassword, db=mysqlDatabase,charset="utf8")


        self.logger.debug('clean_up_database init over.')

    def clean(self):

        now_date = datetime.now()

        delete_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
        # clean t_ms_report
        self.clean_t_ms_report_by_time(delete_date)

        # clean t_camera_log
        self.clean_t_camera_log_by_time(delete_date)


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

    def clean_t_ms_report_by_time(self, delete_date):
        try:

            sql = "DELETE FROM t_ms_report WHERE update_time < '{0}';".format(delete_date)
            conn = None;
            conn = self.__connect_to_db()

            self.logger.debug("[clean_t_ms_report_by_time]%s" %(sql));
            conn.execute(sql);

            self.local_db.commit();

            if conn is not None:
                conn.close(); 


        except Exception,ex:
            self.local_db.rollback()
            self.logger.warning("clean_t_ms_report_by_time, %s" %ex)

    def clean_t_camera_log_by_time(self, delete_date):
        try:

            sql = "DELETE FROM t_camera_log WHERE create_time < '{0}';".format(delete_date)
            conn = None;
            conn = self.__connect_to_db()

            self.logger.debug("[clean_t_camera_log_by_time]%s" %(sql));
            conn.execute(sql);
            
            self.local_db.commit();

            if conn is not None:
                conn.close(); 


        except Exception,ex:
            self.local_db.rollback()
            self.logger.warning("clean_t_camera_log_by_time, %s" %ex)










if __name__ == "__main__":

    handle = clean_up_database('10.25.123.74', 'tvie', 'tvierocks', 'mauna')
    handle.clean()