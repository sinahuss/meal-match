from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi
from .config.dev import Config

mongo_client = None
db = None


def create_app(config_class=Config):
    global mongo_client, db

    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(
        app,
        resources={
            r"/api/*": {"origins": ["http://localhost:8080", "http://127.0.0.1:8080"]}
        },
    )

    if app.config.get("MONGO_URI") and app.config.get("MONGO_DBNAME"):
        try:
            if mongo_client is None:
                mongo_client = MongoClient(
                    app.config["MONGO_URI"],
                    server_api=ServerApi("1"),
                    tlsCAFile=certifi.where(),  # Handles SSL certificates for Atlas
                )
                # Ping to confirm connection
                mongo_client.admin.command("ping")
                print("Successfully connected to MongoDB Atlas!")
                db = mongo_client[app.config["MONGO_DBNAME"]]
            app.extensions["pymongo_db"] = db
        except Exception as e:
            print(f"Error connecting to MongoDB Atlas: {e}")
            # Optionally, app fails startup if DB connection fails
            # raise e
    else:
        print("MongoDB URI or DBNAME not configured. Skipping MongoDB initialization.")

    # Import and register blueprints (routes)
    from .api import bp

    app.register_blueprint(bp)

    @app.route("/health")
    def health_check():
        return "OK", 200

    return app
