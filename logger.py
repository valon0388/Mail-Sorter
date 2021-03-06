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

import pprint
import datetime
import os

# Log levels: if True, print
LOGINFO = True
LOGDEBUG = False
LOGERROR = True

# Level definitions
INFO = 0
DEBUG = 1
ERROR = 2
MOVE = 3

def singleton(cls):
    instances = {}

    def __init__(auto, logfile):
        return

    def getinstance(auto, logfile):
        if cls not in instances:
            instances[cls] = cls(auto, logfile)
        return instances[cls]
    return getinstance

@singleton
class Logger:
    p = pprint.PrettyPrinter(indent=4, width=80)
    pp = p.pprint

    def __init__(self, auto, logfile):
        self.auto = auto
        self.logfile = os.path.expanduser(logfile)

        try:
            self.file = open(logfile, 'a+')
        except FileNotFoundError:
            directory = os.path.split(logfile)[0]
            if not os.path.exists(directory):
                os.makedirs(directory)
            self.file = open(logfile, 'a+')

        self.log(DEBUG, "Initialized Logger")

    def write_log(self, statement):
        dt = datetime.datetime.today()
        if self.auto is True:
            self.file.write("[{}] {}\n".format(dt, statement))
        else:
            self.pp("[{}] {}".format(dt, statement))

    def log(self, level, logtext):
        if LOGINFO and level == INFO:
            # self.pp("INFO: {}".format(logtext))
            self.write_log("INFO: {}".format(logtext))
            return
        if LOGDEBUG and level == DEBUG:
            # self.pp("DEBUG: {}".format(logtext))
            self.write_log("DEBUG: {}".format(logtext))
            return
        if LOGERROR and level == ERROR:
            # self.pp("ERROR: {}".format(logtext))
            self.write_log("ERROR: {}".format(logtext))
            return
        if level == MOVE:
            # self.pp("MOVE: {}".format(logtext))
            self.write_log("MOVE: {}".format(logtext))
            return
        #self.pp("OTHER: {}".format(logtext))
        #self.write_log("OTHER: {}".format(logtext))
    
    def quit(self):
        self.write_log("Closing program on user exit")
        if self.auto is True:
            self.file.close()