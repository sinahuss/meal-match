from flask import Flask
from flask_cors import CORS
from .config.dev import DevConfig
from .db import mongo_setup
from app.api import register_blueprints


def create_app(config_class=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": app.config.get(
                    "CORS_ORIGINS", ["http://localhost:8080", "http://127.0.0.1:8080"]
                )
            }
        },
    )

    if app.config.get("MONGO_URI") and app.config.get("MONGO_DBNAME"):
        try:
            db = mongo_setup.init_db(app.config)
            app.extensions["pymongo_db"] = db
            mongo_setup.ensure_indexes()
        except Exception as e:
            print(f"Error connecting to MongoDB Atlas: {e}")
            # Optionally, app fails startup if DB connection fails
            # raise e
    else:
        print("MongoDB URI or DBNAME not configured. Skipping MongoDB initialization.")

    # Import and register blueprints
    register_blueprints(app)

    @app.route("/health")
    def health_check():
        db_status = "OK" if mongo_setup.get_db_instance() is not None else "Unavailable"
        return f"Flask App: OK, MongoDB: {db_status}", 200

    return app
