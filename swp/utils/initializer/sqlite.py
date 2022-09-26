import os

from .base import DatabaseInitialiser


class SQLiteInitialiser(DatabaseInitialiser):

    def __enter__(self):
        databasefile = self.config['NAME']

        if self.drop and os.path.isfile(databasefile):
            if self.verbosity > 0:
                self.stdout.write('Removing old database file %s ...' % databasefile)

            os.remove(databasefile)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
