# most of this is copied from: https://github.com/anujk3/fitbit-project/blob/111f79abdda94a1c73b3172437bd33b0ad937d5e/fitbit.py

from mongodb.connect_mongodb import mongodb_client
from bson import ObjectId
from datetime import datetime as dt

def save_tresholds_2_db(a,b,c):
    data = {}
    data["th_site_change"] = a
    data["th_battery_change"] = b
    data["th_insuline_level"] = c
    data["date"] = dt.now()
    treshold_db = mongodb_client.NS_extension
    collection_name = "treshold_values"
    treshold_db = treshold_db[collection_name]
    try:
        replacement_data = data
        id = treshold_db.find().distinct('_id')
        query = {"_id": id[0]}
        result = treshold_db.replace_one(query, replacement_data )
    except Exception as e:
        print(e)
        print("collection non existent, creating collection")
        treshold_db.insert_many([data])
        s = treshold_db.find()
        print([i for i in s])

if __name__ == "__main__":
    save_tresholds_2_db(36,20,20)