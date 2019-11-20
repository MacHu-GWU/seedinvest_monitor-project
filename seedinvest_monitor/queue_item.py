# -*- coding: utf-8 -*-

import gzip
from datetime import datetime
from dateutil.parser import parse

import requests
from superjson import json
from attrs_mate import attr, AttrsClass
from .model import Startup
from .crawler import html_parser


@attr.s
class QueueItem(AttrsClass):
    type = attr.ib()  # type: str
    data = attr.ib()  # type: dict

    _method_mapper = dict()

    @classmethod
    def _init_method_mapper(cls):
        for attr in cls.__dict__.keys():
            if attr.startswith("process_"):
                item_type = attr.replace("process_", "")
                cls._method_mapper[item_type] = attr

    def process(self, **kwargs):
        method_name = self._method_mapper[self.type]
        getattr(self, method_name)(**kwargs)

    class Types:
        download_project_html = "download_project_html"
        parse_project_html = "parse_project_html"

    def process_download_project_html(self, sqs_client, record, config):
        receipt_handle = record["receiptHandle"]
        startup = Startup.get(
            hash_key=self.data["id"],
            attributes_to_get=[
                "id",
                "html_download_at",
                "details_update_at",
            ]
        )
        dt_now = datetime.utcnow()
        dt_html_download_at = parse(startup.html_download_at)
        if (dt_now - dt_html_download_at).total_seconds() > int(config.HTML_UPDATE_INTERVAL_IN_SECONDS.get_value()):
            url = startup.url
            content = requests.get(url).content
            compressed_raw_html = gzip.compress(content)
            html_download_at = str(datetime.utcnow())
            startup.update(
                actions=[
                    Startup.compressed_raw_html.set(compressed_raw_html),
                    Startup.html_download_at.set(html_download_at),
                ]
            )

        sqs_client.delete_message(
            QueueUrl=config.SQS_QUEUE_URL.get_value(),
            ReceiptHandle=receipt_handle,
        )

        # send parse scheduled job back to queue
        queue_item = QueueItem(
            type=QueueItem.Types.parse_project_html,
            data=startup.attribute_values,
        )
        sqs_client.send_message(
            QueueUrl=config.SQS_QUEUE_URL.get_value(),
            MessageBody=json.dumps(queue_item.to_dict()),
        )


    def process_parse_project_html(self, sqs_client, record, config):
        receipt_handle = record["receiptHandle"]
        startup = Startup.get(
            hash_key=self.data["id"],
            attributes_to_get=[
                "id",
                "compressed_raw_html",
                "details_update_at",
            ]
        )
        dt_now = datetime.utcnow()
        dt_details_update_at = parse(startup.details_update_at)
        # if (dt_now - dt_details_update_at).total_seconds() > int(config.HTML_UPDATE_INTERVAL_IN_SECONDS.get_value()):
        details_data = html_parser.parse_project_page(startup.raw_html)
        details_data["issuer"] = startup.id
        details_data["issuer_url"] = startup.url
        details_update_at = str(datetime.utcnow())
        startup.update(
            actions=[
                Startup.details.set(details_data),
                Startup.details_update_at.set(details_update_at)
            ]
        )

        sqs_client.delete_message(
            QueueUrl=config.SQS_QUEUE_URL.get_value(),
            ReceiptHandle=receipt_handle,
        )

QueueItem._init_method_mapper()
