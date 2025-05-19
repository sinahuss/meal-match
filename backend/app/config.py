import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)


class Config:
    DEBUG = os.environ.get("FLASK_ENV") == "development"

    MONGO_URI = os.environ.get("MONGO_ATLAS_CONNECTION_STRING")
    MONGO_DBNAME = os.environ.get("MONGO_DB_NAME")
