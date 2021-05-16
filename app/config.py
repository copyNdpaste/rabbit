import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "rabbit"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "rabbit"
    REDIS_URL = os.environ.get("REDIS_URL") or "redis://localhost:6379/0"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    FCM_KEY = os.environ.get("FCM_KEY") or "rabbit"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False
    DEBUG = False


class LocalConfig(Config):
    os.environ["FLASK_ENV"] = "local"
    SQLALCHEMY_ECHO = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://rabbit:password@localhost:5432/bium"
    )


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL") or "sqlite:///:memory:"
    )

    WTF_CSRF_ENABLED = False


class DevelopmentConfig(Config):
    DEBUG = True
    SERVICE_NAME = "rabbit"
    os.environ["FLASK_ENV"] = "development"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL")
    AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")


class ProductionConfig(Config):
    SERVICE_NAME = "rabbit"
    os.environ["FLASK_ENV"] = "production"
    SQLALCHEMY_DATABASE_URI = os.environ.get("PROD_DATABASE_URL")
    AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")


config = dict(
    default=LocalConfig,
    local=LocalConfig,
    testing=TestConfig,
    development=DevelopmentConfig,
    production=ProductionConfig,
)
