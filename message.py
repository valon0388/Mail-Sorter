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


# Local imports
from logger import *
import server

AUTOMOVE = True


class Message:
    to_address = ""
    from_address = ""
    subject = ""
    message = ""
    uid = 00
    labels = [None, None]

    logger = Logger(False, False)

    def __init__(self, parsed_message, uid, server):
        self.log(DEBUG, "Message Init")
        self.to_address = parsed_message['header']['to'] if 'to' in parsed_message['header'] else 'None'
        self.from_address = parsed_message['header']['from'] if 'from' in parsed_message['header'] else 'None'
        self.subject = parsed_message['header']['subject'] if 'subject' in parsed_message['header'] else 'None'
        self.sent_date = parsed_message['header']['date'] if 'date' in parsed_message['header'] else 'None'
        self.cc = parsed_message['header']['cc'] if 'cc' in parsed_message['header'] else 'None'
        self.body = parsed_message['message'] if 'message' in parsed_message else 'None'
        self.uid = uid
        self.labels = self.get_message_labels()
        self.server = server


    # ###################################
    #  Log
    #
    #  Local log method to specify the 
    #  name of the class/file of the 
    #  caller.
    # ###################################
    def log(self, level, statement):
        self.logger.log(level, "message -- {}".format(statement))

    # ###################################
    # GET_MESSAGE_LABELS
    #
    # Gets all the labels on a specified message and outputs
    # them for later use.
    # ###################################
    def get_message_labels(self):
        self.log(INFO, "func --> get_message_labels")
        self.log(INFO, '')  # Get from the bash script and the python script it calls.


    # ###################################
    # REMOVE_ALL_LABELS
    #
    # Removes all labels from a specified message.
    # ################################### Needs Testing
    def remove_all_labels(self):
        self.log(INFO, "func --> remove_all_labels")
        labels = self.get_message_labels()
        for label in labels:
            self.remove_label(label)


    # ###################################
    # REMOVE_LABEL
    #
    # Removes specific labels from a specified message.
    # ################################### Done & Tested
    def remove_label(self, label):
        self.log(INFO, "func --> remove_label")
        self.log(DEBUG, "LABEL: {}".format(label))
        if label == '"inbox"' or label == "inbox":
            # pp("+=============================================SKIPPING")
            self.log(DEBUG, "+=============================================SKIPPING")
            return
        options = {'Y': True, 'N': False, 'n': False}
        # pp(email_message)
        choice = input("Would you like to remove the label {} from this email [UID:{}]?".format(label, self.uid))
        try:
            if options[choice]:
                self.log(INFO, 'LISTING LABELS FOR UID: {}'.format(self.uid))
                response = self.server.mail.uid('FETCH', self.uid, '(X-GM-LABELS)')
                self.log(INFO, response)
                self.log(INFO, 'REMOVE LABEL')
                response = self.server.mail.uid('STORE', self.uid, '-X-GM-LABELS', label)
                self.log(INFO, response)
                self.log(INFO, 'LISTING LABELS FOR UID: {}'.format(self.uid))
                response = self.server.mail.uid('FETCH', self.uid, '(X-GM-LABELS)')
                self.log(INFO, response)
        except KeyError:
            self.log(DEBUG, 'Item %s not found' % choice)


    # ###################################
    # ADD_LABEL
    #
    # Adds a label to a specified message
    # ################################### Done & Tested
    def add_label(self, label):
        self.log(INFO, "func --> add_label")
        options = {'Y': True, 'N': False, 'n': False}
        choice = input("Would you like to add the label {} to this email [UID:{}]: From: {} Subject:{}?".format(label, self.uid, self.from_address, self.subject))
        try:
            if options[choice]:
                self.log(INFO, 'LISTING LABELS FOR UID: {}'.format(self.uid))
                response = self.server.mail.uid('FETCH', self.uid, '(X-GM-LABELS)')
                self.log(INFO, response)
                self.log(INFO, 'ADD LABEL')
                response = self.server.mail.uid('STORE', self.uid, '+X-GM-LABELS', label)
                self.log(INFO, response)
                self.log(INFO, 'LISTING LABELS FOR UID: {}'.format(self.uid))
                response = self.server.mail.uid('FETCH', self.uid, '(X-GM-LABELS)')
                self.log(INFO, response)
        except KeyError:
            self.log(INFO, 'Item %s not found' % choice)


    # ================MESSAGES==================
    # ###################################
    # MOVE_MESSAGE
    #
    # Moves a message from one label to another by removing
    # the source label and adding the destination label.
    # ###################################
    def move_message(self, destination):
        self.log(INFO, "func --> move_message")
        options = {'Y': True, 'N': False, 'n': False}
        if AUTOMOVE is False:
            choice = input("Would you like to move this email [UID[{}] to {}? ".format(self.uid, destination))
        else:
            choice = 'Y'

        try:
            self.log(INFO, options[choice])
            if options[choice]:
                self.log(INFO, 'MOVE')
                self.log(INFO, "MOVING  MESSAGE UID[{}]".format(self.uid))
                response = self.server.mail.uid('COPY', self.uid, destination)
                self.log(INFO, response)
                if response[0] == 'OK':
                    self.log(INFO, self.server.mail.uid('STORE', self.uid, '+FLAGS', '(\\Deleted)'))
                    self.log(INFO, 'ORIGINAL DELETED')
                    self.log(INFO, self.server.mail.expunge())
                    self.log(INFO, "MAIL MOVED")
                else:
                    self.log(INFO, 'ERROR: FAILED TO MOVE MAIL')
            else:
                self.log(INFO, 'LEAVE')
        except KeyError:
            self.log(INFO, 'Item %s not found' % choice)


    # ###################################
    # TRASH_MESSAGE
    #
    # Moves a message to the trash by removing all labels and
    # then adding the trash label.
    # ################################### DONE
    def trash_message(self):
        self.log(INFO, "func --> trash_message")
        self.remove_all_labels()
        self.move_message('Trash')
        self.delete_message()


    # ###################################
    # DELETE_MESSAGE
    #
    # Moves a message to the trash and then marks it for
    # deletion. (To delete, you have to do it this way with gmail)
    # ###################################
    def delete_message(self):
        self.log(INFO, "func --> delete_message")
        options = {'Y': True, 'N': False, 'n': False}
        choice = input("Would you like to delete this email [UID[{}]: From: {} Subject:{}] to {}? ".format(self.uid, self.from_address, self.subject))

        try:
            self.log(INFO, options[choice])
            if options[choice]:
                self.log(INFO, 'DELETE')
                self.log(INFO, "DELETING  MESSAGE UID[{}]: From: {} Subject:{}".format(self.uid, self.from_address, self.subject))
                self.log(INFO, self.server.mail.uid('STORE', self.uid, '+FLAGS', '(\\Deleted)'))
                self.log(INFO, self.server.mail.expunge())
            else:
                self.log(INFO, 'KEEP')
        except KeyError:
            self.log(INFO, 'Item %s not found' % choice)


    # ###################################
    # ARCHIVE_MESSAGE
    #
    # Adds the label "[Gmail]/All Mail" to a specified email. This
    # adds it to the archive while preserving all labels currenlty
    # on the email.
    # ###################################
    def archive_message(self, uid, email_message):
        self.log(INFO, "func --> archive_message")
        self.move_message('"[Gmail]/All Mail"')


    # ###################################
    # STARRED
    #
    # Takes in an email uid and returns True or False based on
    # whether or not it is starred. True == starred.
    #
    # ###################################
    # NOTE: Use the 'XM-'
    def starred(self):
        self.log(INFO, "func --> starred")
        starLabel = '"[Gmail]/Starred"'
        self.sort_mail(starLabel)
