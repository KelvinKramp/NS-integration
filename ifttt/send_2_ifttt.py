import requests
import json
import os

# MAKE DIFFERENCE BETWEEN PRODUCTION AND DEVELOPMENT ENVIRONMENT
if "Users" in os.getcwd():
    from dotenv import load_dotenv
    load_dotenv()
    IFTTT_key = os.environ["IFTTT_key"]
    # get configuration settings firebase
else:
    IFTTT_key = os.environ["IFTTT_key"]

def send_2_ifttt(a,b,c):
    response = { "value1" : a, "value2" : b, "value3" : c }
    r = requests.post("https://maker.ifttt.com/trigger/{event}/with/key/{IFTTT_key}".format(event="nightscout_extension", IFTTT_key = IFTTT_key), data=response)
    print(r.text)

if __name__ == "__main__":
    send_2_ifttt(1,2,3)