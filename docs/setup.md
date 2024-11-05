# Production Setup

The following document describes how to set up the application for production.

Assumed is a Debian-based system, but the instructions should be similar for other systems. The application is set up
in `/var/www/production`.

## Install dependencies

```bash
sudo apt-get update
sudo apt-get install -y $(cat apt-requirements.txt) 
```

## Create the database

```bash
sudo -i -u postgres
psql
  CREATE DATABASE swp;
  CREATE USER swp WITH PASSWORD 'swp';
  GRANT ALL PRIVILEGES ON DATABASE swp TO swp;
  \q
exit
```

## Install the application

```bash
cd /var/www
git clone https://github.com/swp-berlin/webassistant.git production
cd production
git submodule update --init --recursive
```

## Set up the application

```bash
cd /var/www/production
export PLAYWRIGHT_BROWSERS_PATH=/var/www/production/browsers
export DJANGO_SETTINGS_MODULE=swp.settings.production
python3 -m venv env
source env/bin/activate
npx npm install
pip install -r requirements.txt -U --no-input
python -m playwright install chromium
python manage.py migrate
python manage.py compile-translations
python manage.py generate-schemes
npm run build
python manage.py collectstatic --no-input
```

## Set up dependencies

FIXME:

* UWSGI und Celery Setup?
* Redis?
* ElasticSearch?



## Set up and start the services

```bash
ln -s /var/www/production/conf/systemd/celery@.service /etc/systemd/system/celery@production.service
ln -s /var/www/production/conf/systemd/celery@.service /etc/systemd/system/scraper@production.service
systemctl daemon-reload

systemctl enable swp@production.service
systemctl enable celery@production.service
systemctl enable scraper@production.service

systemctl start swp@production.service
systemctl start celery@production.service
systemctl start scraper@production.service
```

