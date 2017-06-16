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

import socket
import argparse
import signal
import sys
import datetime

# Local imports
from logger import *
import config
from server import Server
import sorter


parser = argparse.ArgumentParser(description='Parse flags such as -a --auto for autosort, -v --verbose for verbose logging, -s --sort for specific folder sort, -l --log to specify a log file')
parser.add_argument('-a', '--auto',       type=bool,    default=False,                                  help='True|False Automatically sort all emails without human intervention?')
parser.add_argument('-v', '--verbose',    type=bool,    default=False,                                  help='True|False Automatically sort all emails without human intervention?')
parser.add_argument('-s', '--sort',       type=str,     default="all",                                  help='True|False Automatically sort all emails without human intervention?')
parser.add_argument('-l', '--log',        type=str,     default="~/.config/MailSorter/MailSorter.log",  help='True|False Automatically sort all emails without human intervention?')
args = parser.parse_args()

logger = Logger(args.auto, args.log)

# ###################################
#  Log
#
#  Local log method to specify the 
#  name of the class/file of the 
#  caller.
# ###################################
def log(level, statement):
    logger.log(level, "main -- {}".format(statement))

# ###################################
#  MAIN
#
#  First function run in program.
# ###################################
def main():
    log(DEBUG, "func --> main")
    # --------------Pre-Connect Checks------------------------------------
    is_connected()
    config.get_config()
    # --------------Connect and Authentication-----------------------
    server = Server(config.config['AUTHENTICATION']['server'], config.config['AUTHENTICATION']['user'], config.config['AUTHENTICATION']['pass'])
    # --------------Perform Mail Operations------------------------------
    labels = server.get_all_labels()
    sorter.sort_mail(server)  # '"Social"'
    # --------------Close Connection----------------------------------------
    server.close()
    server.logout()


def is_connected():
    # Detect network connection
    REMOTE_SERVER = "www.google.com"
    log(DEBUG, "func --> is_connected")
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(REMOTE_SERVER)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        # pp("INTERNET CONNECTION DETECTED")
        s.close()
        return True
    except:
        pass
    # pp("INTERNET CONNECTION NOT DETECTED")
    exit(1)
    return False

def quit(posOne, posTwo):
    logger.quit()
    sys.exit(0)

signal.signal(signal.SIGINT, quit)


if __name__ == "__main__":
    main()
