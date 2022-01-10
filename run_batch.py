import schedule
import time
from mongodb.connect_mongodb import mongodb_client
from mongodb.get_tresholds_db import get_tresholds_db
from update_current_values import update_current_values
from mongodb.save_current_values_db import save_current_values_db
from ifttt.send_2_ifttt import send_2_ifttt

def run_batch():
    # GET TRESHOLDS FROM DB

    th_site_change, th_battery_level, th_insuline_level = get_tresholds_db()
    print("retrieved treshold values from db")
    print(th_site_change,th_battery_level,th_insuline_level)

    # #UPDATE CURRENT VALUES AND BOOLS
    bool_site_change, cannula_age = update_current_values("site_change", th_site_change)
    bool_battery_change, battery_level = update_current_values("battery_level", th_battery_level)
    bool_insuline_level, insuline_level = update_current_values("insuline_level",th_insuline_level)
    print("updated_current_values")
    print(cannula_age, battery_level, insuline_level,bool_site_change,bool_battery_change, bool_insuline_level)

    # SAVE CURRENT VALUES AND BOOLS IN DB

    save_current_values_db(cannula_age, battery_level, insuline_level,bool_site_change,bool_battery_change, bool_insuline_level)


    # IF ONE OF THE BOOLEANS = TRUE THEN SEND MESSAGE ABOUT REPLACEMENT
    if bool_site_change:
        message1 = "REPLACE CANNULA. "
    else:
        message1 = ""
    if bool_battery_change:
        message2 = "REPLACE BATTERY. "
    else:
        message2 = ""
    if bool_insuline_level:
        message3 = "REPLACE CARTRIDGE. "
    else:
        message3 = ""

    message = message1 + message2 + message3
    if message:
        send_2_ifttt(message, """cannula_age = {}
                                battery_level = {}
                                insuline_level = {}
                                """.format(cannula_age, battery_level, insuline_level), "")

        # ALSO PAUSE THE LOOP SO THERE IS NOT A REPEATED MESSAGE SENT
        switch_db = mongodb_client.NS_extension
        collection_name = "switch"
        switch_db = switch_db[collection_name]
        data = {}
        data["switch"] = False
        replacement_data = data
        id = switch_db.find().distinct('_id')
        query = {"_id": id[0]}
        result = switch_db.replace_one(query, replacement_data)

if __name__ == "__main__":
    schedule.every(1).minutes.at(":00").do(run_batch)
    switch_db = mongodb_client.NS_extension
    collection_name = "switch"
    switch_db = switch_db[collection_name]
    d = switch_db.find()
    d = [i for i in d]

    # IF FIRST RUN THEN PUT SWITCH ON
    if not d:
        data = {}
        data["switch"] = True
        switch_db.insert_many([data])
        d = switch_db.find() # and reload the database
        d = [i for i in d]

    # CHECK IF ALL BOOLS ARE FALSE, IF SO THEN START OR RESTART LOOP
    if not d[0]["switch"]:
        th_site_change, th_battery_level, th_insuline_level = get_tresholds_db()
        bool_site_change, cannula_age = update_current_values("site_change", th_site_change)
        bool_battery_change, battery_level = update_current_values("battery_level", th_battery_level)
        bool_insuline_level, insuline_level = update_current_values("insuline_level", th_insuline_level)
        if not bool_site_change and not bool_battery_change and not bool_insuline_level:
            d[0]["switch"] = True
    while d[0]["switch"]:
        schedule.run_pending()
        time.sleep(30)