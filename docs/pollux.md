# Pollux Import

Pollux uses the internal [API](api.md) to fetch publications and import them into their database. They run clean-up routines on the imported data which we want to profit from.

That's why a Pollux import task is run via Celery Beat. The task communicates with the Pollux SRU API to reimport SWP publication data. Currently, the publication date and author names are updated from Pollux data.

The task is only configured to run on the production environment and runs hourly, processing up to 3600 publications with one publication per second. Publications are tried only once per day until they were successfully imported.
