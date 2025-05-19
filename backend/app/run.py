import os
from app import create_app
from app.config.dev import DevConfig
from app.config.prod import ProdConfig
from app.config.test import TestConfig

env = os.getenv("FLASK_ENV", "development")
config_map = {
    "development": DevConfig,
    "production": ProdConfig,
    "testing": TestConfig
}

config_class = config_map.get(env, DevConfig)
app = create_app(config_class)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
