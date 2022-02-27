import os

# MAKE DIFFERENCE BETWEEN PRODUCTION AND DEVELOPMENT ENVIRONMENT
if "Users" in os.getcwd():
    BASE = "http://127.0.0.1:8080/"
    api_url_part = "api/"
    # get configuration settings firebase
else:
    BASE = "http://OFFICIAL LINK/"
    api_url_part = "api/"

