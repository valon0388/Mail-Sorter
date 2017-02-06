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




def sort(box, email_uid, email_contents, regexes):
    log(INFO, "func --> sort")
    log(INFO, "The regex for the box {}, is SUBJECT:{} & CONTENT: {}....".format(box, config[box]['subject_regex'], config[box]['content_regex']))
    log(INFO, "EMAIL -- FROM: {}, SUBJECT: {}".format(email_contents['header']['from'], email_contents['header']['subject']))
    if sort_sender(box, email_uid, email_contents['header']['from'], regexes[0]) is False:
        if sort_subject(box, email_uid, email_contents['header']['subject'], regexes[1]) is False:
            if sort_content(box, email_uid, email_contents['message'], regexes[2]) is False:
                log(INFO, "Email Failed to match filter {} for sender, subject, or content...".format(box))


def sort_subject(box, email_uid, subject, regex):
    log(INFO, "func --> sort_subject({})".format(regex))
    # pp("-------Email Contents------")
    log(INFO, "Email Subject: {}".format(subject))
    match = regex.search(subject)
    log(INFO, "Match: {}".format(match))
    match = False if match is None else True

    if match:
        # pp("SUBJECT MATCH FOUND!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        move_message(email_uid, box)
        remove_label(email_uid, '"inbox"')
        # quit() ##HERE
        return True
    return False


def sort_sender(box, email_uid, sender, regex):
    log(INFO, "func --> sort_subject({})".format(regex))

    log(INFO, "Email Sender: {}".format(sender))
    match = regex.search(sender)
    log(INFO, "Match: {}".format(match))
    match = False if match is None else True

    if match:
        # pp("SENDER MATCH FOUND!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        move_message(email_uid, box)
        remove_label(email_uid, '"inbox"')
        # quit() ##HERE
        return True
    return False


def sort_content(box, email_uid, message, regex):
    log(INFO, "func --> sort_content({})".format(regex))

    match = regex.search(message)
    log(INFO, "Match: {}".format(match))
    match = False if match is None else True

    if match:
        move_message(email_uid, box)
        remove_label(email_uid, "inbox")
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
def sort_mail():
    log(INFO, "func --> sort_mail")
    global mail
    inbox = '"inbox"'
    mail.select(inbox)
    message_uids = get_mailbox_contents(inbox)
    sections = get_sections()
    pp("Would you like to sort  for all labels or just one? ")
    choice = input("Options: all or one of the following [{}]? ".format(sections))
    pp(choice)
    pp(sections)

    if "\"{}\"".format(choice) in sections:
            choice = "\"{}\"".format(choice)
            log(INFO, "SORTING MAIL FOR LABEL: {}".format(choice))
            for i in range(10):
                print('.', end="")
                time.sleep(1)
            print('')
            regexes = get_regexes(choice)
            for email_uid in message_uids:
                email_contents = retrieve_message(email_uid)
                sort(choice, email_uid, email_contents, regexes)
    elif choice == "all":
        log(INFO, "SORTING MAIL FOR ALL FILTERS!!!")
        for label in sections:
            log(INFO, "SORTING MAIL FOR LABEL: {}".format(label))
            for i in range(10):
                print('.', end="")
                time.sleep(1)
            print('')
            regexes = get_regexes(label)
            for email_uid in message_uids:
                email_contents = retrieve_message(email_uid)
                sort(label, email_uid, email_contents, regexes)  # HERE -- need to search through labels in config
                # #pp(email_contents)
                # #pp("========================================")
            # email_contents = retrieve_message(message_uids[-1])
            # #pp(email_contents)
            # #pp("========================================")
    else:
        pp("ERROR: selection {} is not one of the provided options!!!".format(choice))