#! /usr/bin/env python3

# v1.00

import configparser as cp
import re
from os.path import isfile

from logger import *

config_file = 'sorter.conf'
config = cp.ConfigParser()

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
def get_regexes(box):
    log(INFO, "func --> get_regexes")
    from_pattern = '{}'.format(config[box]['from_regex'])
    from_regex = re.compile(from_pattern)

    subject_pattern = '{}'.format(config[box]['subject_regex'])
    subject_regex = re.compile(subject_pattern)

    content_pattern = '{}'.format(config[box]['content_regex'])
    content_regex = re.compile(content_pattern)

    return [from_regex, subject_regex, content_regex]


# ###################################
# GET_SECTIONS
#
# Grabs the sections from the config file and returns the
# array.
# ###################################
def get_sections():
    sections = config.sections()
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
def get_config():
    log(INFO, "func --> get_config")
    if isfile(config_file):
        config.read(config_file)
        config.sections()
    else:
        save_config(True)


# ###################################
# SAVE_CONFIG
#
# Saves the config that is currently being used to the file
# mailSorter.conf. If there is no config, saves a default file.
# ################################### Done & Tested
def save_config(default=False):
    log(INFO, "func --> save_config")
    if default:
        config['AUTHENTICATION'] = {
            'server': 'thing.google.com',
            'user': 'bonkers',
            'pass': 'piquel'
        }
        config['FOLDEREX'] = {
            'subject_regex': '(buy|suck)\ it',
            'content_regex': 'change\.org'
        }
    with open(config_file, 'w') as config_link:
        config.write(config_link)