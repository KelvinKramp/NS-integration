# Health Dashboard

Dashboard containing 

![alt text](https://github.com/KelvinKramp/health-dashboard/blob/master/images/Healthdashboard%20overview.png)

## Preperation

Follow this tutorial to create mongoDB database (when choosing username and password use only letters to prevent difficulties in connecting with the database later):
https://codingandfun.com/store-financial-data-into-a-mongodb-database/

Follow Stephen Hsu's tutorial to create fitbit developer access and get clientid, clientsecret, accestoken and refreshtoken:
https://towardsdatascience.com/collect-your-own-fitbit-data-with-python-ff145fa10873

## Installation

Copy this respository to your local harddrive.

```bash
git clone https://github.com/KelvinKramp/health-dashboard.git
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install necessary modules.

```bash
pip install requirements.txt
```


Add cliend_id and client_secret to new file with name "secrets.json" in root directory with format:
```bash
    {"CLIENT_ID":"XXXX",
    "CLIENT_SECRET":"12345XXXX12345xxxxx"}
    """)
```

Add new file with name "connection_string.py" in root directory with mongo DB connection string from the first tutorial in format:
```bash
connection_string = "mongodb+srv://USERNAME:PASSWORD@cluster0.boaqd.mongodb.net/database?retryWrites=true&w=majority"
```

## Usage

```python
python main.py
```
## Weight

For weight, BMI, fatpercentage, etc. assessment copy csv file with weights and name "weights.csv" to your firebase database.


## To do
* Transform into webapp with Heroku.
* Incorporate glucose levels from freestyle libre via xdrip.
* Incorporate fitness activity.
* Create medium article. 

## Code sources
Fitbit module:
https://github.com/orcasgit/python-fitbit.readthedocs

Fitbit API Python Client Implementation
For documentation: http://python-fitbit.readthedocs.org/

More detailed information python fitbit api:
https://python-fitbit.readthedocs.io/en/latest/#fitbit-api

## To do
New ideas are welcome! [k.h.kramp@gmail.com](https://mailto:k.h.kramp@gmail.com).

Follow me on [medium](https://k-h-kramp.medium.com/).