# Internal API Documentation

This document provides a rough overview of the API endpoints available in the SWP application.

Please note that this is an internal API and meant to be consumed by the application's [frontend](frontend.md) only and
not by external clients. It is subject to change and should not be considered stable. Refer to the source code
in `swp/api/` for more details.

## Endpoints

### Thinktank

- **List Thinktanks**: `GET /api/thinktank/`
    - Retrieves a list of thinktanks.
- **Retrieve Thinktank**: `GET /api/thinktank/{id}/`
    - Retrieves details of a specific thinktank.
- **Add Scraper to Thinktank**: `POST /api/thinktank/{id}/add-scraper/`
    - Adds a new scraper to a thinktank.

### Scraper

- **Retrieve Scraper**: `GET /api/scraper/{id}/`
    - Retrieves details of a specific scraper.
- **Update Scraper**: `PUT /api/scraper/{id}/`
    - Updates a scraper's details.
- **Activate Scraper**: `POST /api/scraper/{id}/activate/`
    - Activates a scraper.

### Monitor

- **List Monitors**: `GET /api/monitor/`
    - Retrieves a list of monitors.
- **Retrieve Monitor**: `GET /api/monitor/{id}/`
    - Retrieves details of a specific monitor.
- **Edit Monitor**: `GET /api/monitor/{id}/edit/`
    - Retrieves monitor details for editing.
- **Update Publication Count**: `POST /api/monitor/{id}/update-publication-count/`
    - Updates the publication count for a monitor.
- **Transfer to Zotero**: `POST /api/monitor/{id}/transfer-to-zotero/`
    - Transfers monitor data to Zotero.

### Publication

- **List Publications**: `GET /api/publication/`
    - Retrieves a list of publications.
- **Research Publications**: `GET /api/publication/research/`
    - Performs a research query on publications.
- **Export Publications to RIS**: `GET /api/publication/ris/`
    - Exports publications to RIS format.

### Pool

- **List Pools**: `GET /api/pool/`
    - Retrieves a list of pools.

### Publication List

- **List Publication Lists**: `GET /api/publication-list/`
    - Retrieves a list of publication lists.
- **Retrieve Publication List**: `GET /api/publication-list/{id}/`
    - Retrieves details of a specific publication list.
- **Add Publication to List**: `POST /api/publication-list/{id}/add/{publication_id}/`
    - Adds a publication to a list.
- **Remove Publication from List**: `POST /api/publication-list/{id}/remove/{publication_id}/`
    - Removes a publication from a list.
- **Export Publication List**: `GET /api/publication-list/{id}/export/`
    - Exports a publication list to RIS format.

## Authentication

The API uses session-based authentication. Ensure that you are authenticated to access the endpoints.

## Permissions

Access to certain endpoints is restricted based on user permissions. Ensure that your user account has the necessary
permissions to perform the desired operations.
