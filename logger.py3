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