import os

if "Users" in os.getcwd():
    from dotenv import load_dotenv
    load_dotenv()
    connection_string = os.environ["mongoDB_URI"]
    # get configuration settings firebase
else:
    connection_string = os.environ["mongoDB_URI"]
