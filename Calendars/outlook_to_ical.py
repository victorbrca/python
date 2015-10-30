"""
# Name:          outlook_to_cal.py
# Usage: 
# Description:   Downloads Outlook main calendar for 2x weeks into an ical file
# Created:       2015-10-30
# Copyright 2014, Victor Mendonca - http://wazem.org
#                                 - https://github.com/victorbrca
# License: Released under the terms of the GNU GPL license v3
"""

"""
=> Packages needed
     -------------------------------
    |      Linux       |    pip     |
    |-------------------------------|
    | python-icalendar | icalendar  |
    |    pyexchange    | pyexchange |
     -------------------------------

=> Comments
    The script is configured to download events for the next 2x weeks and save 
    it in a file with ical formatting. 

    Dates are saved in EST, however you can change it if you need. 

=> Before Starting
    Change the following values before starting:
        # Webmail address and credentials
            URL = u'https://[webmail_URL]/EWS/Exchange.asmx'
            USERNAME = u'[user_name]'
            PASSWORD = u"[password]"
        # Header for ical file
            cal.add('prodid', '-//[my header]//mxm.dk//')
    Optional:
        # Set to look for 2x weeks events. Change if needed
            twoweekDelta = timedelta(days=14)
        # Change to create the ical file in a directory of choice
            f=open("calendar.ical", 'wb')
"""

from pyexchange import Exchange2010Service, ExchangeNTLMAuthConnection
from datetime import datetime, timedelta
from pytz import timezone

from icalendar import Calendar, Event, vCalAddress, vText
import tempfile, os

URL = u'https://[webmail_URL]/EWS/Exchange.asmx'
USERNAME = u'[user_name]'
PASSWORD = u"[password]"

# Set up the connection to Exchange
connection = ExchangeNTLMAuthConnection(url=URL,
                                        username=USERNAME,
                                        password=PASSWORD)

service = Exchange2010Service(connection)

def display(cal):
    return cal.to_ical().replace('\r\n', '\n').strip()

eastern = timezone('US/Eastern')

nowDate = datetime.now()
twoweekDelta = timedelta(days=14)
meetingsToGetDate = nowDate + twoweekDelta
meetingsToGetStr = meetingsToGetDate.strftime('%Y, %m, %d, %H, %M, %S')
NowStr = nowDate.strftime('%Y, %m, %d, %H, %M, %S')

eventList = service.calendar().list_events(
    start=timezone("US/Eastern").localize(datetime.strptime(NowStr, '%Y, %m, %d, %H, %M, %S')),
    end=timezone("US/Eastern").localize(datetime.strptime(meetingsToGetStr, '%Y, %m, %d, %H, %M, %S')),
    details=True
)

cal = Calendar()

cal.add('prodid', '-//[my header]//mxm.dk//')
cal.add('version', '2.0')
cal.add('tzid', 'Eastern Standard Time')

for getEvent in eventList.events:
    iCalevent = Event()
    iCalevent['uid'] = getEvent.id
    startUTC = getEvent.start
    startEST = startUTC.astimezone(eastern)
    iCalevent['dtstart'] = startEST.strftime('%Y%m%dT%H%M%S')
    endUTC = getEvent.end
    endEST = endUTC.astimezone(eastern)
    iCalevent['dtend'] = endEST.strftime('%Y%m%dT%H%M%S')
    iCalevent['summary'] = getEvent.subject
    #getEvent.text_body
    mailto = "MAILTO:" + getEvent.organizer[1]
    iCalorganizer = vCalAddress(mailto)
    iCalorganizer.params['cn'] = vText('%s') % str(getEvent.organizer[0])
    iCalevent['organizer'] = iCalorganizer
    iCalevent['location'] = getEvent.location
    cal.add_component(iCalevent)

f=open("calendar.ical", 'wb')
f.write(cal.to_ical())
f.close()