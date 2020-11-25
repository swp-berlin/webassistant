# SWP Webmonitor Backend

The main documentation on concepts and general usage can be found in the wiki
at https://swp.wiki.cosmocode.de/


## Setup

Below is a short description on how to set up the project to run it locally.


### Requirements

* Python 3.7
  - with virtualenv

* Postgres


### Code Setup

``` console
git clone git@gitlab.cosmocode.de:swp/swp.git
```

After cloning the repository, make sure to install the submodules as well.

``` console
git submodule update --init
```

The application should be setup within a Python virtual environment. Be sure to
use Python 3! Activate the environment and set up the dependencies.

``` console
python3 -m venv env
source env/bin activate
pip install -r requirements.txt
```


### Database Setup

Create a Postgres database. By default the database is named `swp`

``` console
su - postgres  # not needed on macOS when postgres is installed with brew
createuser -s -P swp
Enter password for new role: swp
Enter it again: swp
createdb -O swp swp
```

Initialize the database:

``` console
DJANGO_SETTINGS_MODULE=swp.settings.develop python manage.py migrate
```

To generate a superuser account use:

``` console
DJANGO_SETTINGS_MODULE=swp.settings.develop python manage.py createsuperuser
```


### Application Dependencies

Before the first start of the development server you have to run:

``` console
DJANGO_SETTINGS_MODULE=swp.settings.develop python manage.py compile-translations
```


### Development Server

You can run a local development server to test things like this:

``` console
DJANGO_SETTINGS_MODULE=swp.settings.develop python manage.py runserver
```
