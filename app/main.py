import uvicorn
import os
import json


from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from mongo_db import connect_to_db
from schemas import Account

app = FastAPI()


def get_url():
    file = None
    try:
        env = os.environ.get("ENV") or "dev"
        file = f"config.{env}.json"

        print(f"Used the following FastAPI config: {file}")

        with open(f"{os.getcwd()}/configs/{file}") as f:
            data = json.loads(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(
            f"File {file} was not found in configs folder!")

    url = data['service_url']
    port = data['service_port']

    return url, port


@app.get("/ping")
def ping():
    return {"status": "active"}


@app.post("/accounts", response_model=Account)
def create_account(account_data: Account):
    try:
        # Check if accountNumber is already occupied
        existing_account = app.accounts_collection.find_one(
            {"accountNumber": account_data.accountNumber})
        if existing_account:
            raise HTTPException(
                status_code=400, detail="AccountNumber already exists")

        # Insert the account data into the collection
        result = app.accounts_collection.insert_one(account_data.dict())
        inserted_id = result.inserted_id

        # Return all information about the created account
        created_account = app.accounts_collection.find_one(
            {"_id": inserted_id})
        return created_account
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.on_event("startup")
def startup_db_client():
    connect_to_db(app)

    # Verify MongoDB connection
    if hasattr(app, 'mongodb_client') and app.mongodb_client is not None:
        print("MongoDB connection is established.")
    else:
        print("MongoDB connection is not established.")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


if __name__ == "__main__":
    service_url, service_port = get_url()
    uvicorn.run(app, host=service_url, port=service_port)
