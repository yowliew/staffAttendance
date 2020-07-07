class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "mysecretKey_3441"

    DB_CONNECTION_STRING = "sqlite:///prod-data.db"
    DB_NAME = "prod-data-db"
    DB_USERNAME = "prod"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = True
    ORG_NAME = "THEEN FATT SDN.BHD."


class ProductionConfig(Config):
    ENV = "production"


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    DB_CONNECTION_STRING = "sqlite:///devl-data.db"
    DB_NAME = "devl-data-db"
    DB_USERNAME = "devl"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    ENV = "testing"
    TESTING = True
    DB_CONNECTION_STRING = "sqlite:///test-data.db"
    DB_NAME = "test-data-db"
    DB_USERNAME = "test"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = False
