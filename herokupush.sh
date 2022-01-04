#!/bin/sh
#pip freeze > requirements.txt
git add .
git commit -m "update"
git push heroku master
# git push origin master
# heroku pg:reset --confirm suridice2
#heroku run python db_connection/database_setup.py
heroku logs --tail