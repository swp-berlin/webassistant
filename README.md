# SWP Webmonitor Backend

The main documentation on concepts and general usage can be found in the wiki
at https://swp.wiki.cosmocode.de/


## Setup

Below is a short description on how to set up the project to run it locally.


### Requirements

* Python 3.7
  - with virtualenv

* nodejs 14.15 (LTS)
  * with npm 6

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

Frontend code needs dependencies as well. Those are installed with npm:

``` console
npx npm install
```

Frontend assets are compiled with webpack. Use the watch task for development:

``` console
npm run watch
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
DJANGO_SETTINGS_MODULE=swp.settings.dev python manage.py migrate
```

To generate a superuser account use:

``` console
DJANGO_SETTINGS_MODULE=swp.settings.dev python manage.py createsuperuser
```


### Application Dependencies

Before the first start of the development server you have to run:

``` console
DJANGO_SETTINGS_MODULE=swp.settings.dev python manage.py generate-schemes
```

As well as the following to generate all translation files:

``` console
DJANGO_SETTINGS_MODULE=swp.settings.dev python manage.py compile-translations
```

#### Fixtures

You will probably want to install the predefined groups:

``` console
python manage.py loaddata groups
```

Afterwards, you may load generic test accounts for development purposes:

| User | Password | Group | is_staff | is_superuser |
| ---- | -------- | ----- | -------- | ------------ |
| admin@localhost | admin | - | + | + |
| swp-manager@localhost | swp-manager | swp-manager | + | - |
| swp-editor@localhost | swp-editor | swp-editor | + | - |

``` console
python manage.py loaddata test-users
```

> **NOTE** These are totally optional and included mainly for automated tests.


### Development Server

You can run a local development server to test things like this:

``` console
DJANGO_SETTINGS_MODULE=swp.settings.dev python manage.py runserver
```


### Production Server

Please copy .env.default, adjust the configuration parameters and install apt requirements.

``` console
cp conf/.env.example .env
while read apt ; do apt install "$apt" ; done < apt-requirements.txt
```


## IDE Configuration

### IntelliJ IDEA

To have proper coding assistance regarding to import paths set the WebPack Config
in Preferences > Languages & Frameworks > JavaScript > WebPack.

To properly use our lint rules defined in .eslintrc.js for JavaScript and .stylelintrc.js
you have to activate these tools in the preferences.

To activate ESLint set the lint configuration in Preferences > Languages & Frameworks >
JavaScript > Code Quality Tools > ESLint to automatic.

To activate Stylelint go to Preferences > Languages & Frameworks > Style Sheets > Stylelint
and set it enabled.
