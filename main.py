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

from logger import *
import config
import server
import sorter

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
    server.connect()
    server.authenticate()
    # --------------Perform Mail Operations------------------------------
    labels = server.get_all_labels()
    sorter.sort_mail()  # '"Social"'
    # --------------Close Connection----------------------------------------
    server.mail.close()
    server.mail.logout()


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
