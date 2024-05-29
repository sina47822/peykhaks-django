# peykhaks-django

# how to run this project to your server
first clone this project to your server 
for this job put ssh key in project or you need to access if its not public
then clone the project
'''
git clone git@github.com:sina47822/peykhaks-django.git
'''
if you need git to do this use blow job to catch this
'''
git init /
git branch -m master /
git config --global user.name 'sina' /
git config --global user.email 'sinaa.afshar@gmail.com' /
'''
you need to change name, email and branch if you want to use this project

# next
you need to change wsgi and manage.py to read setting from dev file
you can find manage.py in root project and wsgi in core files
# install env
after that for run the project you need to add virtual enviroment
'''
python -m venv env
'''
then upgrade your pip
'''
python -m pip install --upgrade pip
'''
then install all apps
'''
pip install -r requirements.txt
'''
after that use django app to run all the project
'''
python manage.py makemigrations /
python manage.py migrate /
python manage.py createsuperuser
'''
after that you can run server and enjoy
'''
python manage.py runserver
'''
