import requests
import json
from datetime import datetime as dt
from datetime import timedelta
from dateutil import parser
import pytz
import os

count = None
timer = 1
if "Users" in os.getcwd():
    from dotenv import load_dotenv
    load_dotenv()
    NIGHTSCOUT_HOST = os.environ["NIGHTSCOUT_HOST"]
    # get configuration settings firebase
else:
    NIGHTSCOUT_HOST = os.environ["NIGHTSCOUT_HOST"]

def update_current_values(x, treshold, number_days_look_back = 20):
    # SET VARIABLES
    utc = pytz.UTC
    datetime_now = utc.localize(dt.now())
    start_date = (datetime_now - timedelta(number_days_look_back)).strftime("%Y-%m-%d")
    end_date = datetime_now.strftime("%Y-%m-%d")
    if x == "site_change":
        api_request_par = "treatments.json"
    elif x == "battery_level":
        api_request_par = "devicestatus/"
        search = "battery"
    elif x == "insuline_level":
        api_request_par = "devicestatus/"
        search = "reservoir"
    update_list = []
    global count

    # LOOP OVER DIFFERENT SIZES OF DATABASE REQUESTS UNTILL REQUESTED OUTCOME FOUND
    while len(update_list) == 0:

        # INCREASE DATANASE REQIEST SIZE WITH 300%
        if count == None:
            count = 50
        else:
            count = count *3

        # ADJUST API REQUEST
        url = '{0}/api/v1/{1}?find\[created_at\]\[\$gte\]=`date --date="{2} -4 hours" -Iminutes`&find\[created_at\]\[\$lte\]=`date --date="{3} +1 days" -Iminutes.&count={4}`'.format(
            NIGHTSCOUT_HOST, api_request_par, start_date, end_date, count)
        res = requests.get(url)
        d = json.loads(res.text)

        # LOOP OVER DICTIONARY OF RESULTS TO FIND DIFFERENT VARIABLES
        if x == "site_change":
            for i in d:
                if i["eventType"] == "Site Change":
                    try:
                        date = parser.parse(i["created_at"])
                        t=(date, None)
                        update_list.append(t)
                    except KeyError as e:
                        pass
        elif x == "battery_level":
            for i in d:
                if "pump" in i:
                    try:
                        date = parser.parse(i["created_at"])
                        battery_level = i["pump"]["battery"]["percent"]
                        t = (date, battery_level)
                        update_list.append(t)
                    except KeyError as e:
                        pass
        elif x == "insuline_level":
            for i in d:
                if "pump" in i:
                    try:
                        date = parser.parse(i["created_at"])
                        reservoir = i["pump"]["reservoir"]
                        t = (date, reservoir)
                        update_list.append(t)
                    except KeyError as e:
                        pass

        # IF TRIED 5 TIMES WITH INCREASING COUNT RESULTS OF DATABASE THEN RETURN NONE
        timer =+1
        if timer ==5:
            return True, None
        else:
            pass
        if len(update_list) > 0:
            break


    # GET MOST RECENT RESULTS FROM THE RESULTS LIST BY PARSING DATE
    if len(update_list) == 1:
        last_date_change = update_list[0]
    else:
        last_date_change = max(update_list)

    # CALCULATE TIME DIFFERENCE BETWEEN NOW AND LATEST UPDATE
    diff = datetime_now - last_date_change[0]
    houres = diff.total_seconds() // 3600
    minutes = (diff.total_seconds()//60)%60
    houres = format(int(houres), '02d')
    minutes = format(int(minutes), '02d')
    time = houres+":"+minutes+"h"

    # CREATE DICTIONARY OF RESULTS OF DIFFERENT CURRENT VALUES AND RETURN RELEVANT RESULT
    outcome = {"site_change": [int(houres), time], "battery_level": [last_date_change[1], last_date_change[1]], "insuline_level":[last_date_change[1], last_date_change[1]]}
    # print(x)
    # print(outcome[x][0])
    # print(treshold)
    if outcome[x][0] > int(treshold):
        return True, outcome[x][1]
    else:
        return False, outcome[x][1]

if __name__ == "__main__":
    print(update_current_values("site_change", 20))