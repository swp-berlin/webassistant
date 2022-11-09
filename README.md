# SWP Webmonitor

The webmonitor allows monitoring websites (_thinktanks_) for the publication of new articles using configurable _scrapers_. Scrapers are executed using a headless Chrome browser. found publications are saved in a PostgreSQL database and added to an ElasticSearch Index. _Monitors_ allow to define _filters_ that aggregate publications and automatically send Citavi .ris files to configured receivers by email.  

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

    docker compose build --no-cache

With the image built, Docker Compose can be used to start the services. 

    docker compose up

Once the containers are running, you should create a superuser:

    docker compose exec swp python manage.py createsuperuser

Once all containers are up, the application is available at http://localhost:8000

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
