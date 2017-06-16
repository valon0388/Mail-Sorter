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
from dateutil import tz

# Local imports
from logger import *
import server
import config
import message

logger = Logger(False, False)

# ###################################
#  Log
#
#  Local log method to specify the 
#  name of the class/file of the 
#  caller.
# ###################################
def log(level, statement):
    logger.log(level, "sorter -- {}".format(statement))


def sort(box, message, regexes):
    log(DEBUG, "func --> sort")
    log(DEBUG, "The regex for the box {}, is SUBJECT:{} & CONTENT: {}....".format(box, config.config[box]['subject_regex'], config.config[box]['content_regex']))
    log(INFO, "EMAIL -- FROM: {}, SUBJECT: {}".format(message.from_address, message.subject))
    if sort_sender(box, message, regexes[0]) is False:
        if sort_subject(box, message, regexes[1]) is False:
            if sort_content(box, message, regexes[2]) is False and message.body is not None:
                log(INFO, "Email Failed to match filter {} for sender, subject, or content...".format(box))


def sort_subject(box, message, regex):
    log(DEBUG, "func --> sort_subject({})".format(regex))
    log(DEBUG, "Email Subject: {}".format(message.subject))
    match = None
    try:
        match = regex.search(message.subject)
    except TypeError:
        log(ERROR, "TypeError: Subject is [{}]".format(message.subject))
    log(INFO, "Subject Match: {}".format(match))
    match = False if match is None else True

    if match:
        log(INFO, "SUBJECT MATCH FOUND!!!")
        message.move_message(box)
        message.remove_label('"inbox"')
        return True
    return False


def sort_sender(box, message, regex):
    log(DEBUG, "func --> sort_subject({})".format(regex))

    match = None

    try:
        log(INFO, "Email Sender: {}".format(message.from_address))
        log(DEBUG,"TESTING SENDER INPUT - TypeError: expected string or bytes-like object: {}".format(message.from_address))
        match = regex.search(message.from_address) 
        log(INFO, "Sender Match: {}".format(match))
    except TypeError:
        log(ERROR, "TypeError: sender is [{}]".format(message.from_address))

    match = False if match is None else True

    if match:
        log(DEBUG, "SENDER MATCH FOUND!!!")
        message.move_message(box)
        message.remove_label('"inbox"')
        return True
    return False


def sort_content(box, message, regex):
    log(DEBUG, "func --> sort_content({})".format(regex))

    match = regex.search(message.body)
    log(INFO, "Content Match: {}".format(match))
    match = False if match is None else True

    if match:
        message.move_message(box)
        message.remove_label("inbox")
        return True
    return False


# ###################################
# SORT_MAIL
#
# INBOX: Uses the regexs specified in the config to sort the
# inbox into the appropriate folders. Don't sort if starred.
# [BOXNAME]
# subject_regex='(buy|use|break|fix|trash|scratch|suck)|\ it'
# content_regex='change\.org'
#
# OTHER: For every other folder, mail will exclusively be
# sorted based on age. Anything >2 months and not
# starred will be archived.
# ################################### Note: Separate the logic of getting the mail and sorting the mail here
def sort_mail(server):
    log(DEBUG, "func --> sort_mail")
    inbox = '"inbox"'
    server.select_box(inbox)
    message_uids = server.get_mailbox_contents(inbox)
    sections = config.get_sections()
    choice = input("Options: all or one of the following [{}]? ".format(sections))
    log(DEBUG, choice)
    log(DEBUG, sections)

    if "\"{}\"".format(choice) in sections:
            choice = "\"{}\"".format(choice)
            log(INFO, "SORTING MAIL FOR LABEL: {}".format(choice))
            for i in range(10):
                print('.', end="")
                time.sleep(1)
            print('')
            regexes = config.get_regexes(choice)
            for email_uid in message_uids:
                email_contents = server.retrieve_message(email_uid)
                sort(choice, email_uid, email_contents, regexes)
    elif choice == "all":
        log(INFO, "SORTING MAIL FOR ALL FILTERS!!!")
        for label in sections:
            log(INFO, "SORTING MAIL FOR LABEL: {}".format(label))
            for i in range(10):
                print('.', end="")
                time.sleep(1)
            print('')
            regexes = config.get_regexes(label)
            for email_uid in message_uids:
                log(INFO, "========================================")
                message = server.retrieve_message(email_uid)
                sort(label, message, regexes)
                # #pp(email_contents)
            # email_contents = retrieve_message(message_uids[-1])
            # #pp(email_contents)
            # #pp("========================================")
    else:
        log(ERROR, "selection {} is not one of the provided options!!!".format(choice))