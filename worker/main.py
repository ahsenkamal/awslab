import os
import json
import time
import random
import boto3
from dotenv import load_dotenv

load_dotenv()

QUEUE_URL = os.environ["QUEUE_URL"]
AWS_REGION = os.environ.get("AWS_REGION", "ap-south-1")
PROCESSING_SECONDS = float(os.environ.get("PROCESSING_SECONDS", "2"))

sqs = boto3.client("sqs", region_name=AWS_REGION)


def process_task(task: dict):
    task_id = task["task_id"]

    # Simulate CPU/IO work
    sleep_for = PROCESSING_SECONDS + random.uniform(0, 1.5)
    print(f"processing task={task_id} for {sleep_for:.2f}s", flush=True)

    time.sleep(sleep_for)

    print(f"completed task={task_id}", flush=True)


while True:
    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=5,
        WaitTimeSeconds=10,
        VisibilityTimeout=60,
    )

    messages = response.get("Messages", [])

    for message in messages:
        body = json.loads(message["Body"])

        try:
            process_task(body)

            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=message["ReceiptHandle"],
            )
        except Exception as e:
            print(f"failed task={body.get('task_id')} error={e}", flush=True)
