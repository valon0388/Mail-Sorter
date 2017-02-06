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


# Log levels: if True, print
LOGINFO = True
LOGDEBUG = True
LOGERROR = True

# Level definitions
INFO = 0
DEBUG = 1
ERROR = 2
MOVE = 3


def log(level, logtext):
    if LOGINFO and level == INFO:
        pp("INFO: {}".format(logtext))
        return
    if LOGDEBUG and level == DEBUG:
        pp("DEBUG: {}".format(logtext))
        return
    if LOGERROR and level == ERROR:
        pp("ERROR: {}".format(logtext))
        return
    if level == MOVE:
        pp("MOVE: {}".format(logtext))
        return
    pp("OTHER: {}".format(logtext))