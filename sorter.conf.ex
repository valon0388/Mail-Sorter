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


