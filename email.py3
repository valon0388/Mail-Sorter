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
from dateutil.parser import parse,tz
from dateutil import tz

from logger import *


class Email:
    to_address = ""
    from_address = ""
    subject = ""
    message = ""
    uid = 00
    labels = [None, None]


    def  __init__():
        log(DEBUG, "Hello INIT!!")


# ###################################
# GET_MESSAGE_LABELS
#
# Gets all the labels on a specified message and outputs
# them for later use.
# ###################################
def get_message_labels(uid, email_message):
    log(INFO, "func --> get_message_labels")
    log(INFO, '')  # Get from the bash script and the python script it calls.


# ###################################
# REMOVE_ALL_LABELS
#
# Removes all labels from a specified message.
# ################################### Needs Testing
def remove_all_labels(uid, email_message):
    log(INFO, "func --> remove_all_labels")
    labels = get_message_labels(uid, email_message)
    for label in labels:
        remove_label(uid, email_message, label)


# ###################################
# REMOVE_LABEL
#
# Removes specific labels from a specified message.
# ################################### Done & Tested
def remove_label(uid, label):
    log(INFO, "func --> remove_label")
    log(DEBUG, "LABEL: {}".format(label))
    if label == '"inbox"' or label == "inbox":
        # pp("+=============================================SKIPPING")
        log(DEBUG, "+=============================================SKIPPING")
        return
    options = {'Y': True, 'N': False, 'n': False}
    # pp(email_message)
    choice = input("Would you like to remove the label {} from this email [UID:{}]?".format(label, uid))
    try:
        if options[choice]:
            log(INFO, 'LISTING LABELS FOR UID: {}'.format(uid))
            response = mail.uid('FETCH', uid, '(X-GM-LABELS)')
            log(INFO, response)
            log(INFO, 'REMOVE LABEL')
            response = mail.uid('STORE', uid, '-X-GM-LABELS', label)
            log(INFO, response)
            log(INFO, 'LISTING LABELS FOR UID: {}'.format(uid))
            response = mail.uid('FETCH', uid, '(X-GM-LABELS)')
            log(INFO, response)
    except KeyError:
        log(DEBUG, 'Item %s not found' % choice)


# ###################################
# ADD_LABEL
#
# Adds a label to a specified message
# ################################### Done & Tested
def add_label(uid, email_message, label):
    log(INFO, "func --> add_label")
    options = {'Y': True, 'N': False, 'n': False}
    choice = input("Would you like to add the label {} to this email [UID:{}]: From: {} Subject:{}?".format(label, uid, email_message['from'], email_message['subject']))
    try:
        if options[choice]:
            log(INFO, 'LISTING LABELS FOR UID: {}'.format(uid))
            response = mail.uid('FETCH', uid, '(X-GM-LABELS)')
            log(INFO, response)
            log(INFO, 'ADD LABEL')
            response = mail.uid('STORE', uid, '+X-GM-LABELS', label)
            log(INFO, response)
            log(INFO, 'LISTING LABELS FOR UID: {}'.format(uid))
            response = mail.uid('FETCH', uid, '(X-GM-LABELS)')
            log(INFO, response)
    except KeyError:
        log(INFO, 'Item %s not found' % choice)


# ================MESSAGES==================
# ###################################
# MOVE_MESSAGE
#
# Moves a message from one label to another by removing
# the source label and adding the destination label.
# ###################################
def move_message(uid, destination):
    log(INFO, "func --> move_message")
    options = {'Y': True, 'N': False, 'n': False}
    if AUTOMOVE is False:
        choice = input("Would you like to move this email [UID[{}] to {}? ".format(uid, destination))
    else:
        choice = 'Y'

    try:
        log(INFO, options[choice])
        if options[choice]:
            log(INFO, 'MOVE')
            log(INFO, "MOVING  MESSAGE UID[{}]".format(uid))
            response = mail.uid('COPY', uid, destination)
            log(INFO, response)
            if response[0] == 'OK':
                log(INFO, mail.uid('STORE', uid, '+FLAGS', '(\\Deleted)'))
                log(INFO, 'ORIGINAL DELETED')
                log(INFO, mail.expunge())
                log(INFO, "MAIL MOVED")
            else:
                log(INFO, 'ERROR: FAILED TO MOVE MAIL')
        else:
            log(INFO, 'LEAVE')
    except KeyError:
        log(INFO, 'Item %s not found' % choice)


# ###################################
# TRASH_MESSAGE
#
# Moves a message to the trash by removing all labels and
# then adding the trash label.
# ################################### DONE
def trash_message(uid, email_message):
    log(INFO, "func --> trash_message")
    remove_all_labels(uid, email_message)
    move_message(uid, email_message, 'Trash')
    delete_message(uid, email_message)


# ###################################
# DELETE_MESSAGE
#
# Moves a message to the trash and then marks it for
# deletion. (To delete, you have to do it this way with gmail)
# ###################################
def delete_message(uid, email_message):
    log(INFO, "func --> delete_message")
    options = {'Y': True, 'N': False, 'n': False}
    choice = input("Would you like to delete this email [UID[{}]: From: {} Subject:{}] to {}? ".format(uid, email_message['From'], email_message['Subject']))

    try:
        log(INFO, options[choice])
        if options[choice]:
            log(INFO, 'DELETE')
            log(INFO, "DELETING  MESSAGE UID[{}]: From: {} Subject:{}".format(uid, email_message['From'], email_message['Subject']))
            log(INFO, mail.uid('STORE', uid, '+FLAGS', '(\\Deleted)'))
            log(INFO, mail.expunge())
        else:
            log(INFO, 'KEEP')
    except KeyError:
        log(INFO, 'Item %s not found' % choice)


# ###################################
# ARCHIVE_MESSAGE
#
# Adds the label "[Gmail]/All Mail" to a specified email. This
# adds it to the archive while preserving all labels currenlty
# on the email.
# ###################################
def archive_message(uid, email_message):
    log(INFO, "func --> archive_message")
    move_message(uid, email_message, '"[Gmail]/All archive_message(uid, email_message)Mail"')


# ###################################
# STARRED
#
# Takes in an email uid and returns True or False based on
# whether or not it is starred. True == starred.
#
# ###################################
# NOTE: Use the 'XM-'
def starred():
    log(INFO, "func --> starred")
    starLabel = '"[Gmail]/Starred"'
    sort_mail(starLabel)