#! /bin/bash
cd /home/zabo/zabo_api/zabo_api
python3 manage.py makemigrations
python3 manage.py migrate
cd ..
uwsgi --ini uwgi.ini &
cd nginx_config
ln -s 

service nginx start
