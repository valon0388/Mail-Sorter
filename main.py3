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

from logger import *


# ###################################
#  MAIN
#
#  First function run in program.
# ###################################
def main():
    log(DEBUG, "func --> main")
    # --------------Pre-Connect Checks------------------------------------
    is_connected()
    get_config()
    # --------------Connect and Authentication-----------------------
    connect()
    authenticate()
    # --------------Perform Mail Operations------------------------------
    labels = get_all_labels()
    sort_mail()  # '"Social"'
    # --------------Close Connection----------------------------------------
    mail.close()
    mail.logout()


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


if __name__ == "__main__":
    main()
