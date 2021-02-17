import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "auckland"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "hawaii"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False
    DEBUG = False


class LocalConfig(Config):
    os.environ["FLASK_CONFIG"] = "local"
    SQLALCHEMY_ECHO = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://postgres:1234@localhost:5432/rabbit"
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
    os.environ["FLASK_CONFIG"] = "development"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL")


class ProductionConfig(Config):
    SERVICE_NAME = "rabbit"
    os.environ["FLASK_CONFIG"] = "production"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


config = dict(
    default=LocalConfig,
    local=LocalConfig,
    testing=TestConfig,
    development=DevelopmentConfig,
    production=ProductionConfig,
)
