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

import email
from email.parser import Parser as MailParser

# Local imports
from logger import *

class Parser():

    def __init__(self):
        self.logger = Logger(False, False)

    # ###################################
    #  Log
    #
    #  Local log method to specify the 
    #  name of the class/file of the 
    #  caller.
    # ###################################
    def log(self, level, statement):
        self.logger.log(level, "parser -- {}".format(statement))


    # ##################################
    #
    #
    #
    # ################################## DONE & TESTED
    def get_first_text_block(self, email_message):
        self.log(INFO, "func --> get_first_text_block")
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
    def parse_email(self, raw_email, raw_body):
        self.log(INFO, "func --> parse_email")
        email_contents = {"header": {"from": "", "to": "", "cc": "", "date": "", "subject": ""}, "message": ""}
        email_contents["message"] = email.message_from_string(raw_email)
        email_contents["header"]["from"] = email_contents["message"]["From"]
        email_contents["header"]["to"] = email_contents["message"]["to"]
        email_contents["header"]["cc"] = email_contents["message"]["cc"]
        email_contents["header"]["date"] = email_contents["message"]["date"]
        email_contents["header"]["subject"] = email_contents["message"]["subject"]
        # pp("=======================================")
        self.log(INFO, "=======================================")

        emailText = raw_body
        mailparser = MailParser()
        emailThing = mailparser.parsestr(emailText)

        if emailThing.is_multipart():
            # pp("EMAIL MESSAGE IS MULTIPART: {}".format(emailThing.is_multipart()))
            self.log(DEBUG, "EMAIL MESSAGE IS MULTIPART: {}".format(emailThing.is_multipart()))
            for part in emailThing.get_payload():
                part = part.get_payload()
        else:
            # pp("EMAIL MESSAGE IS MULTIPART: {}".format(emailThing.is_multipart()))
            self.log(DEBUG, "EMAIL MESSAGE IS MULTIPART: {}".format(emailThing.is_multipart()))
        email_contents["message"] = emailThing.get_payload()
        # pp(email.message_from_string(raw_email).get_payload(decode=True))
        return email_contents
