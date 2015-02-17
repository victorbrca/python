"""
Disables alert definition on JON server

Usage: python jon_alerts.py [disable|enable]
"""
import sys,os,time
import requests,json
from jon_credentials import *

# Sets up URL, credentials and json
endpoint = 'http://' + RHQ_HOST + ':7080/rest/'
auth = RHQ_USER,RHQ_PASSWORD
headers = {'accept':'application/json','content-type': 'application/json'}

# Gets arguments
if len(sys.argv) < 2:
    print "Disables/enables all alerts in JON"
    print "\t\tUsage: jon_alerts.py [disable|enable]\n"
    quit()
else:
    option = (sys.argv[1])

def disable_alert(alert_name,alert_id):
    disable_alert = {'enabled':False,'dampeningCategory':'ONCE'}
    print "Disabling alert %s (ID: %s)" % (alert_name,alert_id)
    req = requests.put(endpoint+'alert/definition/%s' % (alert_id),json.dumps(disable_alert),headers=headers,auth=auth)
    check_status = req.json()['enabled']
    if check_status == False:
        print "\t\t\t\t\t\t\- disabled\n"
    else:
        print "\t\t\t\t\t\t\- ERROR, did NOT disable\n"


def enable_alert(alert_name,alert_id):
    enable_alert = {'enabled':True,'dampeningCategory':'ONCE'}
    print "Enabling alert %s (ID: %s)" % (alert_name,alert_id)
    req = requests.put(endpoint+'alert/definition/%s' % (alert_id),json.dumps(enable_alert),headers=headers,auth=auth)
    check_status = req.json()['enabled']
    if check_status == True:
        print "\t\t\t\t\t\t\- enabled\n"
    else:
        print "\t\t\t\t\t\t\- ERROR, did NOT enable\n"


# Use a dictionary list of alerts by 'name':id
# alerts = {
#     'memory':10435,
#     'cpu':10423,
# }

alerts = {

}

if option == "disable":
    for name in alerts:
        disable_alert(name, alerts[name])
elif option == "enable":
    for name in alerts:
        enable_alert(name, alerts[name])
else:
    print "I don't know that option"