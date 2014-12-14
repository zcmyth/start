class Config(object):
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_POOL_RECYCLE = 1800


class PROD(Config):
    pass


class STG(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://iwx:f4EBvtNFrDh4uAbb@localhost/start'


class DEV(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://start:Gw6eZ79tu9DEe7YD@localhost/start'


class TESTING(Config):
    TESTING = True
    LIVESERVER_PORT = 8943
