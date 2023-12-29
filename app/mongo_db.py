import json
import os

from pymongo import MongoClient


def connect_to_db(app):
    file = None
    try:
        env = os.environ.get("ENV") or "dev"  # "dev"
        file = f"mongo_db.{env}.json"

        with open(f"{os.getcwd()}/configs/{file}") as f:
            data = json.loads(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(
            f"File {file} was not found in configs folder!")

    mongo_params = {
        'host': data["host"],
        'port': int(data["port"])
    }

    app.mongodb_client = MongoClient(**mongo_params)
    app.accounts_db = app.mongodb_client[data["database"]]
