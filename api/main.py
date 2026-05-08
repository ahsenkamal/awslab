import os
import json
import uuid
import time
import boto3
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

QUEUE_URL = os.environ["QUEUE_URL"]
AWS_REGION = os.environ.get("AWS_REGION", "ap-south-1")

sqs = boto3.client("sqs", region_name=AWS_REGION)
app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/submit")
def submit_task(payload: dict):
    task_id = str(uuid.uuid4())

    message = {
        "task_id": task_id,
        "payload": payload,
        "submitted_at": time.time(),
    }

    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message),
    )

    return {
        "task_id": task_id,
        "status": "queued",
    }
