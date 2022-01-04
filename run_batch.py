import schedule
import time
from mongodb.connect_mongodb import mongodb_client

def run_batch():
    # GET TRESHOLDS FROM DB
    from mongodb.get_tresholds_db import get_tresholds_db
    th_site_change, th_battery_level, th_insuline_level = get_tresholds_db()
    print("retrieved treshold values from db")
    print(th_site_change,th_battery_level,th_insuline_level)

    # #UPDATE CURRENT VALUES AND BOOLS
    from update_current_values import update_current_values
    bool_site_change, cannula_age = update_current_values("site_change", th_site_change)
    bool_battery_change, battery_level = update_current_values("battery_level", th_battery_level)
    bool_insuline_level, insuline_level = update_current_values("insuline_level",th_insuline_level)
    print("updated_current_values")
    print(cannula_age, battery_level, insuline_level,bool_site_change,bool_battery_change, bool_insuline_level)

    # SAVE CURRENT VALUES AND BOOLS IN DB
    from mongodb.save_current_values_db import save_current_values_db
    save_current_values_db(cannula_age, battery_level, insuline_level,bool_site_change,bool_battery_change, bool_insuline_level)

    # RUN SAVED VALUES CHECK
    from ifttt.send_2_ifttt import send_2_ifttt
    message = ""
    if bool_site_change:
        message = "REPLACE CANNULA. "
    if battery_level:
        message = message + "REPLACE BATTERY. "
    if insuline_level:
        message = message + "REPLACE CARTRIDGE. "

    if bool_site_change or bool_battery_change or bool_insuline_level:
        send_2_ifttt(message, """cannula_age = {}
                                battery_level = {}
                                insuline_level = {}
                                """.format(cannula_age, battery_level, insuline_level), "")
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
    if not d:
        data = {}
        data["switch"] = True
        switch_db.insert_many([data])
    else:
        pass
    while d[0]["switch"]:
        schedule.run_pending()
        time.sleep(30)