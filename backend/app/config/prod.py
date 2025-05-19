from .base import Config

class ProdConfig(Config):
    DEBUG = False
    TESTING = False
