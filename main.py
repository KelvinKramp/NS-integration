from mongodb.connect_mongodb import mongodb_client
from bson.objectid import ObjectId
c = mongodb_client.database
db = c.treatments
result =  db.find({"_id" : ObjectId("609d740bcd5dd7000428fe3e")})
for result_object in result:
    print(result_object)   # result_object is a dict that holds JSON object
    result_object['_id']  # Mongo ObjectId of the result_object
    # result_object["<field_name>"]  # Value stored in a field named <fieldname>