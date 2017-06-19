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

import configparser as cp
import re
from os.path import isfile

# Local imports
from logger import *


class Config():

    def __init__(self):
        self.config_file = 'sorter.conf'
        self.config = cp.ConfigParser()

        self.logger = Logger(False, False)
        self.sections = self.get_config()

    # ###################################
    #  Log
    #
    #  Local log method to specify the 
    #  name of the class/file of the 
    #  caller.
    # ###################################
    def log(self, level, statement):
        self.logger.log(level, "config -- {}".format(statement))

    # ###################################
    # GET_REGEXES
    #
    # Grabs the regex patterns from the config file, compiles
    # them and returns them in an array with the corresponding
    # order:
    #
    # 0: From
    # 1: Subject
    # 2: Content
    # ###################################
    def get_regexes(self, box):
        self.log(INFO, "func --> get_regexes")
        from_pattern = '{}'.format(self.config[box]['from_regex'])
        from_regex = re.compile(from_pattern)

        subject_pattern = '{}'.format(self.config[box]['subject_regex'])
        subject_regex = re.compile(subject_pattern)

        content_pattern = '{}'.format(self.config[box]['content_regex'])
        content_regex = re.compile(content_pattern)

        return [from_regex, subject_regex, content_regex]


    # ###################################
    # GET_SECTIONS
    #
    # Grabs the sections from the config file and returns the
    # array.
    # ###################################
    def get_sections(self):
        sections = self.config.sections()
        sections.remove("AUTHENTICATION")
        return sections


    #  ================SETUP==================
    # ###################################
    #  GET_CONFIG
    #
    #  Grabs the configuration information from mailSorter.conf
    #  If mailSorter.conf doesn't exist, uses save_config() to
    #  generate and save a default config and use that.
    # ################################### Done & Tested
    def get_config(self):
        self.log(INFO, "func --> get_config")
        if isfile(self.config_file):
            self.config.read(self.config_file)
            self.config.sections()
        else:
            self.save_config(True)


    # ###################################
    # SAVE_CONFIG
    #
    # Saves the config that is currently being used to the file
    # mailSorter.conf. If there is no config, saves a default file.
    # ################################### Done & Tested
    def save_config(self, default=False):
        self.log(INFO, "func --> save_config")
        if default:
            self.config['AUTHENTICATION'] = {
                'server': 'thing.google.com',
                'user': 'bonkers',
                'pass': 'piquel'
            }
            self.config['FOLDEREX'] = {
                'subject_regex': '(buy|suck)\ it',
                'content_regex': 'change\.org'
            }
        with open(config_file, 'w') as config_link:
            self.config.write(config_link)
