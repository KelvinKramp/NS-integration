# GET TRESHOLDS FROM DB
from mongodb.get_tresholds_db import get_tresholds_db
th_site_change, th_battery_level, th_insuline_level = get_tresholds_db()
print("retrieved treshold values from db")

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
if battery_level:
    message = message + "REPLACE CARTRIDGE. "

send_2_ifttt(message, """cannula_age = {}
                        battery_level = {}
                        insuline_level = {}
                        """.format(cannula_age, battery_level, insuline_level), "")