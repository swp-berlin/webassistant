class DatabaseInitializerException(Exception):

    def __init__(self, *args, alias, engine, **kwargs):
        self.alias = alias
        self.engine = engine

        super(DatabaseInitializerException, self).__init__(*args, **kwargs)


class DatabaseInitialiser(object):

    def __init__(self, command, alias, drop, verbosity, interactive, config):
        self.command = command
        self.alias = alias
        self.drop = drop
        self.verbosity = verbosity
        self.interactive = interactive
        self.config = config

        self.stdout = command.stdout
        self.stderr = command.stderr

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError
