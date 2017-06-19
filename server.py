#! /usr/bin/env python3

# v1.01

# This file is part of MailSorter.

# MailSorter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# MailSorter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with MailSorter.  If not, see <http://www.gnu.org/licenses/>.

import imaplib
import datetime

# Local imports
from logger import *
from parser import Parser
from message import Message

class Server():

    # Record all dates in UTC as they don't observer DST
    runtime = datetime.datetime.utcnow()
    runtime = runtime

    mail = ''

    # ###################################
    #  init
    #
    #  Loads the server connection information and calls the    
    #  connect and authenticate functions.
    #
    # ###################################
    def __init__(self, server, user, password):
        self.logger = Logger(False, False)
        self.log(DEBUG, "Server Init!!")
        self.connect(server)
        self.authenticate(user, password)

    # ###################################
    #  Log
    #
    #  Local log method to specify the 
    #  name of the class/file of the 
    #  caller.
    # ###################################
    def log(self, level, statement):
        self.logger.log(level, "server -- {}".format(statement))


    # ###################################
    # CONNECT
    #
    # Connects to the mail server specified in the config and
    # instantiates the mail object.
    # ################################### Done & Tested
    def connect(self, server):
        self.log(INFO, "func --> connect")
        self.log(DEBUG, "Server: {}".format(server))
        # self.mail = imaplib.IMAP4_SSL(config.config['AUTHENTICATION']['server'])
        self.mail = imaplib.IMAP4_SSL(server)


    # ###################################
    # AUTHENTICATE
    #
    # Authenticates with the mail server using the username
    # and password specified in the config.
    # ################################### Done & Tested
    def authenticate(self, user, password):
        self.log(INFO, "func --> authenticate")
        self.log(DEBUG, "Login information: user:{} password:{}".format(user, password))
        self.mail.login(user, password)


    # =================LABELS===================
    # ###################################
    # GET_ALL_LABELS
    #
    # Grabs all the labels from the mail server and returns them
    # in an array.
    # ###################################
    def get_all_labels(self):
        self.log(INFO, "func --> get_all_labels")
        labels_tuple = self.mail.list()
        labels_list = []
        for item in labels_tuple[1]:
            # pp(item)
            item = item.decode("utf-8").split("\"")[3]
            if item != '[Gmail]':
                labels_list.append(item)
        # pp(labels_list)
        self.log(DEBUG, labels_list)
        return labels_list

    # ###################################
    # RETRIEVE_MESSAGE
    #
    # Grabs the message from GMAIL and sends to parse_email
    # which returns the email_contents in a readable format.
    #
    # ################################### DONE & TESTED
    def retrieve_message(self, email_uid):
        self.log(INFO, "func --> retrieve_message")
        
        #Fetch the mail headers from GMAIL
        result, data_one = self.mail.uid("FETCH", email_uid, '(BODY[HEADER.FIELDS (MESSAGE-ID FROM TO CC DATE SUBJECT)])')
        if result == 'OK':
            self.log(DEBUG, "GOT MESSAGE HEADERS[{}]".format(email_uid))
        else:
            self.log(DEBUG, "FAILED TO GET MESSAGE HEADERS[{}]".format(email_uid))
            exit(1)

        #Fetch the body of the message(including the attachement)
        result, data_two = self.mail.uid("FETCH", email_uid, '(BODY[TEXT])')
        if result == 'OK':
            self.log(DEBUG, "GOT MESSAGE BODY[{}]".format(email_uid))
        else:
            self.log(DEBUG, "GOT MESSAGE BODY[{}]".format(email_uid))
            exit(1)
        self.log(DEBUG, data_two)
        
        if data_one[0] is not None:
            raw_email = data_one[0][1].decode("utf-8")
        else:
            raw_email = "None"
        if data_two[0] is not None:
            raw_body = data_two[0][1].decode("ISO-8859-1")
        else:
            raw_body = "None"
        
        parser = Parser()
        parsed_message = parser.parse_email(raw_email, raw_body)

        return Message(parsed_message, email_uid, self)

    # =================MAILBOX===================
    # ###################################
    # GET_MAILBOX_CONTENTS
    #
    # Returns all the uids of the specified label.
    # ################################### Label is not used, replace "ALL"?
    def get_mailbox_contents(self, label):
        self.log(INFO, "func --> get_mailbox_contents")
        
        result, data = self.mail.uid('search', None, "ALL")  # search and return UIDs
        if result == 'OK':
            self.log(INFO, "YOU'VE GOT MAIL!!!")
        else:
            self.log(INFO, "NO MAIL FOR YOU!!!")
            exit(1)
        return data[0].split()


    # ###################################
    # GET_OLD_UIDS
    #
    # Returns an array of the uid of every message >= 2
    # months old that are in the specified label.
    # ###################################
    def get_old_uids(self, label):
        self.log(INFO, "func --> get_old_uids")
        self.log(INFO, "")


    # ###################################
    # ARCHIVE_ALL
    #
    # Archives every message in the passed uid array.
    # ################################### Done?
    def archive_all(self, uid_array):  # uid_array is defined as follows [[uid, email_message], [uid, email_message], etc...]
        self.log(INFO, "func --> archive_all")
        for item in uid_array:
            archive_message(item[0], item[1])

    def close(self):
        self.mail.close()

    def logout(self):
        self.mail.logout()

    def select_box(self, box):
        self.mail.select(box)
