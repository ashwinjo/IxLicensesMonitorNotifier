"""
This script will read the license details from database and send license expiration details every week.
License expiring in 1 week, 15 days, 1 month , 6 months
"""

from datetime import datetime, timedelta
from tabulate import tabulate
from sendEmail import send_email
import config
import IxOSRestAPICaller as ixOSRestCaller
from RestApi.IxOSRestInterface import IxRestSession


def licenseChecker(records=None):    
    expiring_in_15_days = []
    expiring_in_7_days = []
    expiring_in_30_days = []
    expiring_in_60_days = []
    already_expired = []
    
    # Convert string to datetime object
    for record in records[0]:
        
        current_date = datetime.now().date()
        target_date = datetime.strptime(record["expiryDate"], "%d-%b-%Y").date()
        delta = target_date - current_date
        
        if record["isExpired"] == "True":
            already_expired.append((record['chassisIp'], record["activationCode"], record["quantity"], 
              record["description"] ,record["expiryDate"], record["isExpired"]))
        if delta >= timedelta(days=7) and delta < timedelta(days=15):
            expiring_in_7_days.append((record['chassisIp'], record["activationCode"], record["quantity"], 
              record["description"] ,record["expiryDate"], record["isExpired"]))
        elif delta >= timedelta(days=15) and delta < timedelta(days=30):
            expiring_in_15_days.append((record['chassisIp'], record["activationCode"], record["quantity"], 
              record["description"] ,record["expiryDate"], record["isExpired"]))
        elif delta >= timedelta(days=30) and delta < timedelta(days=60):
            expiring_in_30_days.append((record['chassisIp'], record["activationCode"], record["quantity"], 
              record["description"] ,record["expiryDate"], record["isExpired"]))
        elif delta >= timedelta(days=60) and delta < timedelta(days=180):
            expiring_in_60_days.append((record['chassisIp'], record["activationCode"], record["quantity"], 
              record["description"] ,record["expiryDate"], record["isExpired"]))

    messages_list = tabulate_results_as_string_message([expiring_in_7_days, expiring_in_15_days, 
                                               expiring_in_30_days, expiring_in_60_days, 
                                               already_expired])

    send_email(message =  '<br/>'.join(messages_list))

def tabulate_results_as_string_message(list_of_expiry):
    
    messages_list = []
    m = {0: "==== Expiring in 7 - 14 days ====", 
     1: "==== Expiring in 15 - 29 days ====" , 
     2: "==== Expiring in 30 - 59 days ====", 
     3: "==== Expiring in 60 - 90 days ====", 
     4:"==== Expired ===="}
    for idx, exp in enumerate(list_of_expiry):
        table_string = tabulate(exp, headers=['chassisIP', "activationCode", "quantity", "description", "expiryDate","isExpired"], tablefmt="html")
        t = "<br/>" + m[idx] + "<br/>" + table_string + "<br/>"
        messages_list.append(t)
    return messages_list
    

def get_chassis_licensing_data():
    """This is a call to RestAPI to get chassis licensing data
    """
    list_of_licenses = []
    if config.CHASSIS_LIST:
        for chassis in config.CHASSIS_LIST:
            try:
                session = IxRestSession(
                    chassis["ip"], chassis["username"], chassis["password"], verbose=False)
                out = ixOSRestCaller.get_license_activation(session, chassis["ip"], "NA")
                list_of_licenses.append(out)
            except Exception:
                a = [{
                'chassisIp': chassis["ip"],
                'typeOfChassis': 'NA',
                'hostId': 'NA',
                'partNumber': 'NA',
                'activationCode': 'NA',
                'quantity': 'NA',
                'description': 'NA',
                'maintenanceDate': 'NA',
                'expiryDate': 'NA',
                'isExpired': 'NA',
                'lastUpdatedAt_UTC': 'NA'
                }]
                list_of_licenses.append(a)
    licenseChecker(records = list_of_licenses)

if __name__ == "__main__":
    get_chassis_licensing_data()