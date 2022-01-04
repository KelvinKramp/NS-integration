# most of this is copied from: https://github.com/anujk3/fitbit-project/blob/111f79abdda94a1c73b3172437bd33b0ad937d5e/fitbit.py

from mongodb.connect_mongodb import mongodb_client

def get_tresholds_db():
    try:
        treshold_db = mongodb_client.NS_extension
        collection_name = "treshold_values"
        treshold_db = treshold_db[collection_name]
        d = treshold_db.find()
        d= [i for i in d][0]
        return d["th_site_change"], d["th_battery_change"],d["th_insuline_level"]
    except Exception as e:
        print(e)
        return None, None, None


if __name__ == "__main__":
    print(get_tresholds_db())