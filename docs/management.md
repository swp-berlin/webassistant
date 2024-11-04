# Management Commands Documentation

This document provides an overview of the custom management commands available in the SWP application. These commands
are used to perform various administrative tasks.

## Translation Commands

These commands are used to manage translations in the application and build JSON catalogs for the frontend.

### update-translations

- **Description**: Creates and cleans translation files for every domain and configured language.
- **Usage**: `python manage.py update-translations [-l <language>] [-d <domain>]`
- **Options**:
    - `-l`: Specify languages to update.
    - `-d`: Specify domains to update.

### compile-translations

- **Description**: Compiles translation files, avoiding message files in the virtualenv directory.
- **Usage**: `python manage.py compile-translations [--directory <directory>] [--no-catalog]`
- **Options**:
    - `--directory`: Directory to compile translations in.
    - `--no-catalog`: Skip generating translation catalogs.

### generate-translation-catalogs

- **Description**: Generates JavaScript translation catalogs for each language.
- **Usage**: `python manage.py generate-translation-catalogs [--directory <directory>]`
- **Options**:
    - `--directory`: Directory to save the generated catalogs.

### generate-schemes

- **Description**: Generates various JSON schemes.
- **Usage**: `python manage.py generate-schemes`
- **Schemes**:
    - `choices`
    - `scraper-types`

### generate-choices-scheme

- **Description**: Generates a JSON scheme for various choice fields. Called by `generate-schemes`.
- **Usage**: `python manage.py generate-choices-scheme`

### generate-scraper-types-scheme

- **Description**: Generates a JSON scheme for scraper types. Called by `generate-schemes`.
- **Usage**: `python manage.py generate-scraper-types-scheme`


## Scraping Commands

These commands are used to manage the scraping process in the application.

### scrape

- **Description**: Initiates the scraping process for a specific item.
- **Usage**: `python manage.py scrape <pk>`
- **Arguments**:
    - `pk`: The primary key of the item to scrape.


### sync-zotero-items

- **Description**: Synchronizes Zotero items with the local database.
- **Usage**: `python manage.py sync-zotero-items [--dry_run]`
- **Options**:
    - `--dry_run`: Simulate the synchronization process without making changes.

### update-publication-counts

- **Description**: Updates publication counts for monitors.
- **Usage**: `python manage.py update-publication-counts [--database <alias>] [--dry-run]`
- **Options**:
    - `--database`: Database alias to use.
    - `--dry-run`: Show how many monitors would be updated without making changes.

### schedule-monitors

- **Description**: Schedules monitors for execution.
- **Usage**: `python manage.py schedule-monitors [--dry-run]`
- **Options**:
    - `--dry-run`: Simulate scheduling without sending emails.
