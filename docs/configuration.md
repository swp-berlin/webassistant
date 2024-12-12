# Configuration

The application configured through Django's settings mechanism. Settings for different environment are stored in `swp/settings/` directory.
The settings are loaded based on the `DJANGO_SETTINGS_MODULE` environment variable.

  * `swp.settings.dev` - Settings for local development.
  * `swp.settings.staging` - Test settings.
  * `swp.settings.production` - Production settings. 


## Environment Variables

The settings files define sensible defaults, but some can be overridden by environment variables. The following environment variables are available:

| Environment Variable  | Default Value               | Description                           |
|-----------------------|-----------------------------|---------------------------------------|
| SECRET_KEY            |                             | Secret key for Django                 |
| DEBUG                 | False                       | Enable/disable debug mode             |
| SITE_ID               | 1                           | ID of the current site                |
| DATABASE_HOST         | 127.0.0.1                   | Database host address                 |
| DATABASE_NAME         | swp                         | Name of the database                  |
| DATABASE_USER         | swp                         | Database user                         |
| DATABASE_PASSWORD     | swp                         | Database password                     |
| PLAYWRIGHT_DEBUG      | False                       | Enable/disable Playwright debug mode  |
| SHELL_PLUS_PRINT_SQL  | False                       | Enable/disable SQL printing in shell  |
| MAIL_PREVIEW_ENABLED  | DEBUG                       | Enable/disable mail preview           |
| DEFAULT_FROM_EMAIL    | production@swp.cosmocode.de | Default email address for sending     |

It's recommended to use a `.env` file to set these variables. The `.env` file should be placed in the root of the project.
