import urllib2
from BeautifulSoup import BeautifulSoup
import re, sys

# Gets arguments
if len(sys.argv) < 2:
    print "Searches online man pages for command"
    print "\t\tUsage: whatis.py [command]\n"
    quit()
else:
    command = (sys.argv[1])

sections = ['1', '2', '3', '4', '5', '6', '7', '8']

for section in sections:
    url = "http://linux.die.net/man/%s/%s" % (section, command)
    try:
        urllib2.urlopen(url)
    except urllib2.HTTPError:
            if section == "8":
                print "Page not found"
    else:
        soup = BeautifulSoup(urllib2.urlopen("%s" % url))
        oneline = soup.fetch('p')[0].getText().splitlines()[0]
        whatis = re.sub(r'Synopsis.*$', '', oneline)
        print whatis
        break
