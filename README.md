# SWP WebAssistant

The WebAssistant allows monitoring websites (_thinktanks_) for the publication of new articles using configurable _scrapers_. Scrapers are executed using a headless Chrome browser. Found publications are saved in a PostgreSQL database and added to an ElasticSearch Index. _Monitors_ allow to define _filters_ that aggregate publications and automatically send Citavi .ris files to configured receivers by email.  

Please note that most of the application is in German only currently.


## Development setup

This repository comes with a Docker Compose setup that should help to set up the requirements to run the project locally. The following containers will be started

  * `swp` The main Django/React application, including Playwright and a headless Chrome browser. Restarts when code is changed.
  * `db` The PostgreSQL database, exposed to port `5432` in case you want to access it directly
  * `redis` The Redis message broker
  * `elasticsearch` A single node ElasticSearch instance
  * `celery` The Celery task queue
  * `bootstrap` Runs one-off tasks like updating translations, running database migrations etc.
  * `frontend` Runs nmp and webpack in watch mode to automatically rebuild the frontend when code is changed.

Please note that the Docker Compose setup is not recommended to be used for a live deployment, yet!


### Getting started

Build the docker image (this needs to be redone whenever major dependencies change)

    docker-compose build --no-cache

With the image built, Docker Compose can be used to start the services. 

    docker-compose up

Once the containers are running, you should create a superuser:

    docker-compose exec swp python manage.py createsuperuser

Finally you can log in at http://localhost:8000

### Management commands

The Docker Compose setup will generally automatically do any required actions when the code is changed or the application is used. However sometimes it may be necessary to manually trigger certain actions. This can be done by running the `manage.py` script in the `swp` container.

Rebuild the Elastic Search Index:

    docker-compose exec swp python manage.py search_index --rebuild

Run a specific scraper (identified by its ID):

    docker-compose exec swp python manage.py scrape <id>

More commands are listed when running manage.py without arguments:

    docker-compose exec swp python manage.py


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
the django development server by running the configuration. Code completion will only work if the
docker container has been started at least once.

To enable running django management commands right-click on the project root and click `Open Module Settings`.
Select the `mangage.py` located in the project root. Select `swp/settings/dev.py` as the settings file. You should now 
be able to run management commands via `Tools > Run manage.py Task`.

To have proper coding assistance regarding to import paths set the WebPack Config
in `Preferences > Languages & Frameworks > JavaScript > WebPack`.

To properly use our lint rules defined in `.eslintrc.js` for JavaScript and `.stylelintrc.js`
you have to activate these tools in the preferences.

 - To activate ESLint set the lint configuration in `Preferences > Languages & Frameworks >
JavaScript > Code Quality Tools > ESLint to automatic`.

 - To activate Stylelint go to `Preferences > Languages & Frameworks > Style Sheets > Stylelint`
and set it enabled.
