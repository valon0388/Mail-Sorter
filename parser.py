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





# ##################################
#
#
#
# ################################## DONE & TESTED
def get_first_text_block(email_message):
    log(INFO, "func --> get_first_text_block")
    maintype = email_message.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
            elif maintype == 'text':
                return email_message.get_payload()


# ##################################
# PARSE_EMAIL
#
# Parses the mail returned from the retrieve_email
# function.
#
# ################################## DONE & TESTED
def parse_email(raw_email, raw_body):
    log(INFO, "func --> parse_email")
    email_contents = {"header": {"from": "", "to": "", "cc": "", "date": "", "subject": ""}, "message": ""}
    email_contents["message"] = email.message_from_string(raw_email)
    email_contents["header"]["from"] = email_contents["message"]["From"]
    email_contents["header"]["to"] = email_contents["message"]["to"]
    email_contents["header"]["cc"] = email_contents["message"]["cc"]
    email_contents["header"]["date"] = email_contents["message"]["date"]
    email_contents["header"]["subject"] = email_contents["message"]["subject"]
    # pp("=======================================")
    log(INFO, "=======================================")

    emailText = raw_body
    emailThing = parser.parsestr(emailText)

    if emailThing.is_multipart():
        # pp("EMAIL MESSAGE IS MULTIPART: {}".format(emailThing.is_multipart()))
        log(DEBUG, "EMAIL MESSAGE IS MULTIPART: {}".format(emailThing.is_multipart()))
        for part in emailThing.get_payload():
            part = part.get_payload()
    else:
        # pp("EMAIL MESSAGE IS MULTIPART: {}".format(emailThing.is_multipart()))
        log(DEBUG, "EMAIL MESSAGE IS MULTIPART: {}".format(emailThing.is_multipart()))
        message = emailThing.get_payload()
    email_contents["message"] = emailThing.get_payload()
    # pp(email.message_from_string(raw_email).get_payload(decode=True))
    return email_contents