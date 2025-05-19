import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)


class Config:
    DEBUG = False
    TESTING = False

    MONGO_URI = os.environ.get("MONGO_ATLAS_CONNECTION_STRING")
    MONGO_DBNAME = os.environ.get("MONGO_DB_NAME")

    CORS_ORIGINS = ["http://localhost:8080", "http://127.0.0.1:8080"]
