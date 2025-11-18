# Production Setup

The following document describes how to set up the application for production.

Assumed is a Debian-based system, but the instructions should be similar for other systems. The application is set up
in `/var/www/production`. The Python version has to be installed in version 3.11. If not otherwise stated commands have to be executed by root-User

## Install dependencies

```bash
apt-get update
apt-get install -y $(cat apt-requirements.txt)
```

* ElasticSearch
```bash
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
apt-get install apt-transport-https
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
apt-get update && apt-get install elasticsearch
```

* nodejs
```bash
apt-get update
apt-get install -y ca-certificates curl gnupg
mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_14.x buster main" | tee /etc/apt/sources.list.d/nodesource.list
apt-get update && apt-get install nodejs
```

## Create the database

```bash
sudo -i -u postgres
psql
  CREATE DATABASE swp;
  CREATE USER swp WITH PASSWORD 'swp';
  GRANT ALL PRIVILEGES ON DATABASE swp TO swp;
  \c swp
  CREATE EXTENSION IF NOT EXISTS citext;
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

## Set up and start the services

```bash
cp /var/www/production/conf/nginx/swp-production /etc/nginx/sites-enabled/swp-production
cp /var/www/production/conf/systemd/swp@.service /etc/systemd/system/
cp /var/www/production/conf/systemd/celery@.service /etc/systemd/system/
cp /var/www/production/conf/systemd/pollux@.service /etc/systemd/system/
cp /var/www/production/conf/systemd/scraper@.service /etc/systemd/system/
cp /var/www/production/conf/.env.example /var/www/production/.env

systemctl daemon-reload

systemctl enable swp@production.service
systemctl enable celery@production.service
systemctl enable pollux@production.service
systemctl enable scraper@production.service

systemctl start swp@production.service
systemctl start celery@production.service
systemctl start pollux@production.service
systemctl start scraper@production.service
```
