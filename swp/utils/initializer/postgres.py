from django.db import connections

from .base import DatabaseInitialiser, DatabaseInitializerException


class PostgresInitialiser(DatabaseInitialiser):
    temporary_database = 'template1'
    engine = 'postgres'

    def __init__(self, *args, **kwargs):
        try:
            import psycopg2
        except ImportError as error:
            raise DatabaseInitializerException(error, alias=self.alias, engine=self.engine)

        self.psycopg2 = psycopg2

        super(PostgresInitialiser, self).__init__(*args, **kwargs)

    def __enter__(self):
        connection = connections[self.alias]
        params = connection.get_connection_params()
        databasename = params.pop('database')

        # We have to connect to a different database before we can drop the existing one.
        params['database'] = getattr(self.command, 'temporary_postgres_database', self.temporary_database)

        # Close the current connection that
        # may be opened by django before.
        connection.close()

        if self.drop:
            self.drop_database(databasename, connection, params)

        self.create_database(databasename, connection, params)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def execute(self, command, databasename, pool, params):
        connection = None

        try:
            connection = pool.get_new_connection(params)

            connection.set_isolation_level(0)

            with connection.cursor() as cursor:
                cursor.execute(command % databasename)

        except self.psycopg2.Error as error:
            if error.pgcode == '42P04':
                self.stderr.write('Database %s already exists. Please make sure it is empty.' % databasename)

            elif error.pgcode == '42501':
                raise DatabaseInitializerException(
                    'Role "%(role)s" has no permission to create database "%(database)s". '
                    'Please add permission by running the following command in psql '
                    'console: "ALTER ROLE "%(role)s" WITH %(privilege)s;"' % {
                        'role': params.get('user'),
                        'database': databasename,
                        'privilege': 'CREATEDB',
                    },
                    alias=self.alias,
                    engine=self.engine,
                )

            elif error.pgcode:
                raise DatabaseInitializerException(
                    '[%s] %s' % (error.pgcode, error),
                    alias=self.alias,
                    engine=self.engine,
                )

            else:
                raise DatabaseInitializerException(error, alias=self.alias, engine=self.engine)

        finally:
            if connection is not None:
                connection.close()

    def drop_database(self, databasename, connection, params):
        if self.verbosity > 0:
            self.stdout.write('Dropping old database %s ...' % databasename)

        self.execute('DROP DATABASE IF EXISTS "%s"', databasename, connection, params)

    def create_database(self, databasename, connection, params):
        if self.verbosity > 0:
            self.stdout.write('Creating new database %s ...' % databasename)

        self.execute('CREATE DATABASE "%s"', databasename, connection, params)
