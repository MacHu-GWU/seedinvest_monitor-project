# -*- coding: utf-8 -*-

from superjson import json

from seedinvest_monitor.boto_ses import boto_ses
from seedinvest_monitor.queue_item import QueueItem
from seedinvest_monitor.devops.config_init import config

sqs_client = boto_ses.client("sqs")


def handler(event, context):
    records = event["Records"]
    for record in records:
        queue_item = QueueItem.from_dict(json.loads(record["body"]))
        queue_item.process(
            sqs_client=sqs_client,
            record=record,
            config=config,
        )


if __name__ == "__main__":
    test_event_download_project_html = {
        "Records": [
            {
                "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
                "receiptHandle": "MessageReceiptHandle",
                "body": "{\"type\": \"download_project_html\", \"data\": {\"id\": \"hitch\", \"html_download_at\": \"1970-01-01 00:00:00\", \"details_update_at\": \"1970-01-01 00:00:00\"}}",
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1523232000000",
                    "SenderId": "123456789012",
                    "ApproximateFirstReceiveTimestamp": "1523232000001"
                },
                "messageAttributes": {},
                "md5OfBody": "7b270e59b47ff90a553787216d55d91d",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:MyQueue",
                "awsRegion": "us-east-1"
            }
        ]
    }

    test_event_parse_project_html = {
        "Records": [
            {
                "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
                "receiptHandle": "MessageReceiptHandle",
                "body": "{\"type\": \"parse_project_html\", \"data\": {\"id\": \"hitch\", \"html_download_at\": \"1970-01-01 00:00:00\", \"details_update_at\": \"1970-01-01 00:00:00\"}}",
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1523232000000",
                    "SenderId": "123456789012",
                    "ApproximateFirstReceiveTimestamp": "1523232000001"
                },
                "messageAttributes": {},
                "md5OfBody": "7b270e59b47ff90a553787216d55d91d",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:MyQueue",
                "awsRegion": "us-east-1"
            }
        ]
    }
    handler(test_event_parse_project_html, {})
