#! /bin/bash
cd /home/zabo/zabo_api
python3 manage.py makemigrations
python3 manage.py migrate
uwsgi --ini uwsgi.ini &
cd /home/zabo/zabo_api/nginx_config
cp default2 /etc/nginx/sites-available/default2
cd /etc/nginx/sites-enabled
ln -s /etc/nginx/sites-available/default2 default2  

service nginx start
