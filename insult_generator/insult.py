import urllib, sys, re
from BeautifulSoup import BeautifulSoup

filterme = ""

# Gets arguments
if len(sys.argv) > 1:
    if (sys.argv[1]) == "-f":
        filterme = True
    elif (sys.argv[1]) == "-h":
        print "Prints random insults"
        print "Usage: insult.py {-f (filter bad words)}"
        quit()
    else:
        print "I don't know that option"
        print "Usage: insult.py {-f} (filter bad words)"
        quit()


html = urllib.urlopen("http://www.insultgenerator.org").read()
soup = BeautifulSoup(html)
texts = soup.findAll(text=True)
insult = soup.findAll(attrs={'class' : 'wrap'})[0].getText()

if filterme:
    with open('lib/swear', 'r') as swearDB:
        swearwords = swearDB.read().splitlines()
        for swear in swearwords:
            if swear in insult:
                count = len(swear) #4
                masked = ''
                for letter in list(swear):
                    if count == len(swear) or count == 1:
                        masked += letter
                    else:
                        masked += '*'
                    count -= 1
                insult = insult.replace(swear, masked)

       
print insult