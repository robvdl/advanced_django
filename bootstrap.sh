#!/bin/bash

virtualenv -p python3 env
. env/bin/activate

pip install -U pip
pip install -r dataserver/requirements.txt

dataserver/manage.py migrate
dataserver/manage.py loaddata teams persons projects sites types sensors measurements
dataserver/manage.py createsuperuser
