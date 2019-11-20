# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from superjson import json
from sfm.fingerprint import fingerprint
from seedinvest_monitor.boto_ses import boto_ses
from seedinvest_monitor.model import Startup
from seedinvest_monitor.devops.config_init import config
from seedinvest_monitor.queue_item import QueueItem

sqs_client = boto_ses.client("sqs")


def handler(event, context):
    update_html_earilier_than = str(datetime.utcnow() - timedelta(seconds=int(config.HTML_UPDATE_INTERVAL_IN_SECONDS.get_value())))
    result_iterator = Startup.scan(
        Startup.html_download_at < update_html_earilier_than,
        limit=10,
        attributes_to_get=[
            "id",
            "html_download_at",
            "details_update_at",
        ],
    )
    sqs_entries = list()
    for startup in result_iterator:
        queue_item = QueueItem(
            type=QueueItem.Types.download_project_html,
            data=startup.attribute_values,
        )
        entry = {
            "Id": fingerprint.of_text(startup.id),
            "MessageBody": json.dumps(queue_item.to_dict()),
        }
        sqs_entries.append(entry)

    sqs_client.send_message_batch(
        QueueUrl=config.SQS_QUEUE_URL.get_value(),
        Entries=sqs_entries,
    )


if __name__ == "__main__":
    handler({}, {})
