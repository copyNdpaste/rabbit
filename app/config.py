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
    os.environ["FLASK_ENV"] = "local"
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

    # AWS_ACCESS_KEY = "AKIAVTIDZALHLIYC5U5J"
    # AWS_SECRET_ACCESS_KEY = "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"


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
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


config = dict(
    default=LocalConfig,
    local=LocalConfig,
    testing=TestConfig,
    development=DevelopmentConfig,
    production=ProductionConfig,
)
