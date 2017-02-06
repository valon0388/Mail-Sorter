#! /usr/bin/env python3

# v1.00

import imaplib
import pprint
import email
import time
import configparser as cp
import logging
import subprocess
import socket
import re
from email.parser import Parser
from os.path import isfile
from datetime import datetime
from dateutil.parser import parse,tz
from dateutil import tz

from logger import *

# Record all dates in UTC as they don't observer DST
runtime = datetime.utcnow()
runtime = runtime

mail = ''


# ###################################
# CONNECT
#
# Connects to the mail server specified in the config and
# instantiates the mail object.
# ################################### Done & Tested
def connect():
    log(INFO, "func --> connect")
    global mail
    log(DEBUG, ['Server: ', config['AUTHENTICATION']['server']])
    mail = imaplib.IMAP4_SSL(config['AUTHENTICATION']['server'])


# ###################################
# AUTHENTICATE
#
# Authenticates with the mail server using the username
# and password specified in the config.
# ################################### Done & Tested
def authenticate():
    log(INFO, "func --> authenticate")
    global mail
    log(DEBUG, ["Login information: ", config['AUTHENTICATION']['user'], config['AUTHENTICATION']['pass']])
    mail.login(config['AUTHENTICATION']['user'], config['AUTHENTICATION']['pass'])




# =================LABELS===================
# ###################################
# GET_ALL_LABELS
#
# Grabs all the labels from the mail server and returns them
# in an array.
# ###################################
def get_all_labels():
    log(INFO, "func --> get_all_labels")
    global mail
    labels_tuple = mail.list()
    labels_list = []
    for item in labels_tuple[1]:
        # pp(item)
        item = item.decode("utf-8").split("\"")[3]
        if item != '[Gmail]':
            labels_list.append(item)
    # pp(labels_list)
    log(DEBUG, labels_list)
    return labels_list


# ###################################
# RETRIEVE_MESSAGE
#
# Grabs the message from GMAIL and sends to parse_email
# which returns the email_contents in a readable format.
#
# ################################### DONE & TESTED
def retrieve_message(email_uid):
    log(INFO, "func --> retrieve_message")
    global mail
    result, data_one = mail.uid("FETCH", email_uid, '(BODY[HEADER.FIELDS (MESSAGE-ID FROM TO CC DATE SUBJECT)])')
    if result == 'OK':
        # pp("GOT MESSAGE HEADERS[{}]".format(email_uid))
        log(DEBUG, "GOT MESSAGE HEADERS[{}]".format(email_uid))
    else:
        # pp("FAILED TO GET MESSAGE HEADERS[{}]".format(email_uid))
        log(DEBUG, "FAILED TO GET MESSAGE HEADERS[{}]".format(email_uid))
        exit(1)
    result, data_two = mail.uid("FETCH", email_uid, '(BODY[TEXT])')
    if result == 'OK':
        # pp("GOT MESSAGE BODY[{}]".format(email_uid))
        log(DEBUG, "GOT MESSAGE BODY[{}]".format(email_uid))
    else:
        # pp("FAILED TO GET MESSAGE BODY[{}]".format(email_uid))
        log(2, "GOT MESSAGE BODY[{}]".format(email_uid))
        exit(1)
    log(DEBUG, data_two)
    if data_one[0] is not None:
        raw_email = data_one[0][1].decode("utf-8")
    else:
        raw_email = "None"
    if data_two[0] is not None:
        raw_body = data_two[0][1].decode("ISO-8859-1")
    else:
        raw_body = "None"
    return parse_email(raw_email, raw_body)


# =================MAILBOX===================
# ###################################
# GET_MAILBOX_CONTENTS
#
# Returns all the uids of the specified label.
# ################################### Label is not used, replace "ALL"?
def get_mailbox_contents(label):
    log(INFO, "func --> get_mailbox_contents")
    global mail
    result, data = mail.uid('search', None, "ALL")  # search and return UIDs
    if result == 'OK':
        # pp("YOU'VE GOT MAIL!!!")
        log(INFO, "YOU'VE GOT MAIL!!!")
    else:
        # pp("NO MAIL FOR YOU!!!")
        log(INFO, "NO MAIL FOR YOU!!!")
        exit(1)
    return data[0].split()


# ###################################
# GET_OLD_UIDS
#
# Returns an array of the uid of every message >= 2
# months old that are in the specified label.
# ###################################
def get_old_uids(label):
    log(INFO, "func --> get_old_uids")
    log(INFO, "")


# ###################################
# GET_OLD_UIDS
#
# Returns an array of the uid of every message >= 2
# months old that are in the specified label.
# ###################################
def get_old_uids(label):
    log(INFO, "func --> get_old_uids")
    log(INFO, "")


# ###################################
# ARCHIVE_ALL
#
# Archives every message in the passed uid array.
# ################################### Done?
def archive_all(uid_array):  # uid_array is defined as follows [[uid, email_message], [uid, email_message], etc...]
    log(INFO, "func --> archive_all")
    for item in uid_array:
        archive_message(item[0], item[1])