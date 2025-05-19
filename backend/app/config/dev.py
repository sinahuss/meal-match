from .base import Config

class DevConfig(Config):
    DEBUG = True
    TESTING = False
