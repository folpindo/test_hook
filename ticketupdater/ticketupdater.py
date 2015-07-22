#/bin/env python

import sys
import os
import re
import MySQLdb
import ConfigParser as parser
import traceback

class TicketUpdater:

    def __init__(self, trac_name, config_file):

        self.trac_name = trac_name
        self.config_file = config_file
        self.config = None
        self.db = None

        if config_file is not None:

            if os.path.isfile(config_file):
                config = parser.ConfigParser()
                config.read(config_file)
                self.config = config
            else:
                print "Configuration file %s does not exist."

        self.host = "localhost"
        self.database = None
        self.database_user = None
        self.database_user_password = None

        connection_params_complete = False

        if config is not None:

            if config.has_section("common"):

                if config.has_option("common","database_user"):
                    database_user = config.get("common","database_user")
                    self.database_user = database_user

                if config.has_option("common","database_user_password"):
                    database_user_password = config.get("common","database_user_password")
                    self.database_user_password = database_user_password

                if config.has_option("common","host"):
                    host = config.get("common","host")
                    self.host = host

            if config.has_section(trac_name):
                if config.has_option(trac_name,"database"):
                    database = config.get(trac_name,"database")
                    self.database = database
        if database is not None and database_user is not None and database_user_password is not None:
             connection_params_complete = True

        if connection_params_complete:
             db = MySQLdb.connect(self.host,self.database_user,self.database_user_password,self.database)
             self.db = db

    def save_ticket_change(self,ticket_id,author,change_time,field,newvalue):
        if self.db is not None:
            db = self.db
            try:
                cursor = db.cursor();
                cursor.execute("""SELECT max(oldvalue) FROM ticket_change WHERE ticket=%s and field='comment' order by time desc limit 1""" % ticket_id)
                oldvalue = 1
                comment_count = cursor.fetchall()
                if comment_count is not None and comment_count[0][0] is not None:
                    last_comment = comment_count[0][0]
                    #checking for format like 12.13, where 12 is the comment being replied and 13 the last comment which replied
                    dotpos = last_comment.find('\.')
                    if dotpos is not -1:
                        oldvalue = str(int(last_comment[dotpos:])+1)
                    else:
                        oldvalue = str(int(comment_count[0][0]) + 1)
                cursor.execute("""INSERT INTO ticket_change  (ticket,time,author,field, oldvalue, newvalue) VALUES(%s, %s, %s, %s, %s, %s)""",(ticket_id, change_time, author, field, oldvalue, newvalue))
                db.commit()
            except Exception,e:
                db.rollback()
                print "There has been an error in the insert operation."
                print str(e)
                traceback.print_exc()

            db.close()
        else:
            print "Db object was not set."
