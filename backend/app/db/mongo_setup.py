from pymongo import MongoClient, IndexModel
from pymongo.server_api import ServerApi
import certifi

client = None
db = None

def init_db(app_config):
    global client, db
    if client is None:
        try:
            client = MongoClient(
                app_config["MONGO_URI"],
                server_api=ServerApi("1"),
                tlsCAFile=certifi.where(),
            )
            client.admin.command("ping")
            db = client[app_config["MONGO_DBNAME"]]
            print("Successfully connected to MongoDB Atlas!")
        except Exception as e:
            print(f"Error connecting to MongoDB Atlas: {e}")
            raise e
            db = None
    return db

def get_db_client():
    global client
    if client is None:
        raise Exception("MongoDB client not initialized")
    return client

def get_db_instance():
    global db
    if db is None:
        raise Exception("MongoDB database instance not initialized")
    return db

def ensure_indexes():
    try:
        db = get_db_instance()
        indexes = [
            IndexModel([("name", 1)]),
            IndexModel([("tags", 1)]),
            IndexModel([("cuisine_type", 1)]),
            IndexModel([("dish_type", 1)]),
            IndexModel([("servings", 1)]),
            IndexModel([
                ("name", "text"),
                ("description", "text"),
                ("search_keywords", "text")
            ])
        ]
        db.recipes.create_indexes(indexes)
        return list(db.recipes.index_information().values())
    except Exception as e:
        print(f"Error ensuring indexes: {e}")
        return {"error": str(e)}
