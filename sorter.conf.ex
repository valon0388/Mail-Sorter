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


[AUTHENTICATION]
server = imap.gmail.com
user = HHHHHHHHHH@gmail.com
pass = YYYYYYYYYYYYYYYYYYYYYYYY

["Social"]
from_regex = info@e.twitter.com|messages-noreply@linkedin.com
subject_regex = Facebook|Twitter|Meetup|Google\ \+
content_regex = SOCIAL

["Bills"]
from_regex = bill@service.com|isp@moneygoeshere.com
subject_regex = Your bill is ready to view|Payment Confirmation
content_regex = BILLS

["Finance"]
from_regex = BANK@example.com
subject_regex = FINANCE
content_regex = FINANCE

["ForumsandGroups"]
from_regex = groups-noreply@linkedin.com
subject_regex = FORUMSANDGROUPS
content_regex = FORUMSANDGROUPS

["Games"]
from_regex = GAMES
subject_regex = GAMES
content_regex = GAMES

["Receipts"]
from_regex = Your (.com order of|purchase protected)
subject_regex = Receipts
content_regex = Order Details|Your Receipt

["Junk"]
from_regex = delete@this.com|stuff@youdontwant.com
subject_regex = (buy|rent)\ this
content_regex = JUNK


