# SWP Webmonitor Backend

The main documentation on concepts and general usage can be found in the wiki
at https://swp.wiki.cosmocode.de/


## Setup

Below is a short description on how to set up the project to run it locally.


### Requirements

* Python 3.8
  - with virtualenv

* nodejs 14.15 (LTS)
  * with npm 6

* Postgres

* Elasticsearch 8.4.3


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


### Elasticsearch Setup

Start the elasticsearch server:

```console
docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:8.4.3
```

To obtain the elastic user password, run the following command and set the `ELASTICSEARCH_PASSWORD` variable in your
`.env` file:

``` console
docker exec -it elasticsearch bin/elasticsearch-reset-password -u elastic
```

To initially create and build indices, run the following:

``` console
DJANGO_SETTINGS_MODULE=swp.settings.dev python manage.py search_index --rebuild
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

You will probably want to install these predefined entities:

``` console
python manage.py loaddata groups sites
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

In order for scrapers to be run in development you have to start celery as well.
Celery needs a running redis server, make sure to start it first.

``` console
DJANGO_SETTINGS_MODULE=swp.settings.dev celery -A swp worker -B -Q celery,scraper -l INFO --purge
```


### Production Server

Please copy .env.default, adjust the configuration parameters and install apt requirements.

``` console
cp conf/.env.example .env
while read apt ; do apt install "$apt" ; done < apt-requirements.txt
```


## IDE Configuration

### IntelliJ IDEA

To set up the project in IntelliJ IDEA 
- select `File > New > Project from existing Sources...`. 
- In the Dialog that pops up select the folder you have cloned the repository into. 
- When prompted to select the Project SDK use the `+` sign in the top left corner to select `New Python SDK...`. 
- Select `Docker Compose` in the left menu and select `swp` as the Service on the right side.

Add a run configuration go to `Run > Edit Configurations...`. Click the `+` in the top left corner of the dialog
and select `Django`. Use `0.0.0.0` as the Host. Select `Use SDK of module`. Edit the environment
variables and set `DJANGO_SETTINGS_MODULE` to `swp.settings.dev`. You should now be able to start
the django development server by running the configuration.

To enable running django management commands right-click on the project root and click `Open Module Settings`.
Select the `mangage.py` located in the project root. You should now be able to run management commands 
via `Tools > Run manage.py Task`.

To have proper coding assistance regarding to import paths set the WebPack Config
in `Preferences > Languages & Frameworks > JavaScript > WebPack`.

To properly use our lint rules defined in `.eslintrc.js` for JavaScript and `.stylelintrc.js`
you have to activate these tools in the preferences.

 - To activate ESLint set the lint configuration in `Preferences > Languages & Frameworks >
JavaScript > Code Quality Tools > ESLint to automatic`.

 - To activate Stylelint go to `Preferences > Languages & Frameworks > Style Sheets > Stylelint`
and set it enabled.
