class Config(object):
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_POOL_RECYCLE = 1800

    PAYPAL_CONFIG = {
        'API_USERNAME': 'sdk-three_api1.sdk.com',
        'API_PASSWORD': 'QFZCWN5HZM8VBG7Q',
        'API_SIGNATURE': 'A-IzJhZZjhg29XQ2qnhapuwxIDzyAZQ92FRP5dqBzVesOkzbdUONzmOU',
        'API_ENVIRONMENT': 'SANDBOX'
    }
    LOGGING_PATH = '/home/zhangchun/start.log'
    LOGGING_SIZE = 10 * 1024 * 1024 # 10 mb


class PROD(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Z8Rj2KXFwF3KNFEL@173.194.226.116/start'
    PAYPAL_CONFIG = {
        'API_USERNAME': 'caviarcomm_api1.gmail.com',
        'API_PASSWORD': 'R49929E743HPG8DN',
        'API_SIGNATURE': 'A7f14DCoZRpIuf60c3wN2qUdd9nGANyyqtfk-MyDfwteO6Ac.G30m3Hq',
        'API_ENVIRONMENT': 'PRODUCTION'
    }
    LOGGING_PATH = '/home/zhangchun88_gmail_com/start.log'


class STG(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://start:Z6Rj2KXFwF3KNFEL@localhost/start'
    PAYPAL_CONFIG = {
        'API_USERNAME': 'sdk-three_api1.sdk.com',
        'API_PASSWORD': 'QFZCWN5HZM8VBG7Q',
        'API_SIGNATURE': 'A-IzJhZZjhg29XQ2qnhapuwxIDzyAZQ92FRP5dqBzVesOkzbdUONzmOU',
        'API_ENVIRONMENT': 'SANDBOX'
    }


class DEV(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://start:Gw6eZ79tu9DEe7YD@localhost/start'


class TESTING(Config):
    TESTING = True
    LIVESERVER_PORT = 8943
