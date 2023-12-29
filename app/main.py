from fastapi import FastAPI, HTTPException
import uvicorn
import os
import json

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


if __name__ == "__main__":
    service_url, service_port = get_url()
    uvicorn.run(app, host=service_url, port=service_port)
