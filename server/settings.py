class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = 'change me later'

    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    PAYPAL_CONFIG = {
        'API_USERNAME': 'sdk-three_api1.sdk.com',
        'API_PASSWORD': 'QFZCWN5HZM8VBG7Q',
        'API_SIGNATURE': 'A-IzJhZZjhg29XQ2qnhapuwxIDzyAZQ92FRP5dqBzVesOkzbdUONzmOU',
        'API_ENVIRONMENT': 'SANDBOX'
    }
    LOGGING_PATH = '/home/zhangchun/start.log'
    LOGGING_SIZE = 10 * 1024 * 1024  # 10 mb
    WECHAT_CONSUMER_KEY = 'wx520c15f417810387'
    WECHAT_SECRET = 'fa74abefd7b192bae334ab3a65d1b55d'


class PROD(Config):
    SQLALCHEMY_DATABASE_URI = 'cloudsql://root:Z8Rj2KXFwF3KNFEL@173.194.226.116/start'
    PAYPAL_CONFIG = {
        'API_USERNAME': 'ningxu_api1.startnewyork.us',
        'API_PASSWORD': 'FCREEEALP8TFYRJM',
        'API_SIGNATURE': 'A0BABM-XIr4X5mHXjHPE-yS3etrvAP-P9O5PGOknXKkHTx6pBMFwI8ji',
        'API_ENVIRONMENT': 'PRODUCTION'
    }
    LOGGING_PATH = '/home/zhangchun88_gmail_com/start.log'


class DEV(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://start:Gw6eZ79tu9DEe7YD@localhost/start'


class TESTING(Config):
    TESTING = True
    LIVESERVER_PORT = 8943
