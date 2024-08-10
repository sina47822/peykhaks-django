# peykhaks-django

## how to run this project to your server
first clone this project to your server 
for this job put ssh key in project or you need to access if its not public
then clone the project
```
git clone git@github.com:sina47822/peykhaks-django.git
```
if you need git to do this use blow job to catch this
```
git init /
git branch -m master /
git config --global user.name 'sina' /
git config --global user.email 'sinaa.afshar@gmail.com' /
```
you need to change name, email and branch if you want to use this project

## next
you need to change wsgi and manage.py to read setting from dev file
you can find manage.py in root project and wsgi in core files
## install env
after that for run the project you need to add virtual enviroment
```
python -m venv env
```
if your pip is newest version that is fine but if its not you need to upgrade pip to the latest version
then upgrade your pip whit this command
```
python -m pip install --upgrade pip
```
if you connect from iran internet pip latest version cant install and you neet to change pip server for do that you need to use command below
 I do this by using the -i and --trusted-host options
```
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade pip
```
for Permanent Fix
Since the release of pip 10.0, you should be able to fix this permanently just by upgrading pip itself:
```
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pip setuptools
```
You may want to add the trusted hosts and proxy to your config file.
pip.ini (Windows) or pip.conf (unix)

***Unix***
---
*Global*
/
    In a “pip” subdirectory of any of the paths set in the environment variable XDG_CONFIG_DIRS (if it exists), for example /etc/xdg/pip/pip.conf.
    This will be followed by loading /etc/pip.conf.
*User*
/
    $HOME/.config/pip/pip.conf, which respects the XDG_CONFIG_HOME environment variable.
    The legacy “per-user” configuration file is also loaded, if it exists: $HOME/.pip/pip.conf.
*Site*
/
    $VIRTUAL_ENV/pip.conf
    
***Windows***
---
*Global*
/
        On Windows 7 and later: C:\ProgramData\pip\pip.ini (hidden but writeable)
        On Windows Vista: Global configuration is not supported.
        On Windows XP: C:\Documents and Settings\All Users\Application Data\pip\pip.ini
*User*
/
    %APPDATA%\pip\pip.ini
    The legacy “per-user” configuration file is also loaded, if it exists: %HOME%\pip\pip.ini
*Site*
/
    %VIRTUAL_ENV%\pip.ini

```
[global]
index=https://my-company/nexus/repository/pypi-group/pypi
index-url=https://my-company/nexus/repository/pypi-group/simple
trusted-host=my-company
```
but you can configure this using pip config on user or global level, something like:
```
pip config --user set global.index https://my-company/nexus/repository/pypi-group/pypi
pip config --user set global.index-url https://my-company/nexus/repository/pypi-group/simple
pip config --user set global.trusted-host my-company
```
You could also add the -i and --trusted-host options to your requirements.txt like this:
```
-i https://sampleurl.com/pypi-remote/simple --trusted-host sample.host.com
```

then install all apps
```
pip install -r requirements.txt
```
after that use django app to run all the project
```
python manage.py makemigrations /
python manage.py migrate /
python manage.py createsuperuser
```
after that you can run server and enjoy
```
python manage.py runserver
```
