# -*- coding: utf-8 -*-

import gzip
from datetime import datetime
from dateutil.parser import parse

import requests
from attrs_mate import attr, AttrsClass
from .model import Startup


@attr.s
class QueueItem(AttrsClass):
    type = attr.ib()  # type: str
    data = attr.ib()  # type: dict

    class Types:
        download_project_html = "download_project_html"

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

    def process_download_project_html(self, sqs_client, record, config):
        receipt_handle = record["receiptHandle"]
        startup = Startup.get(
            hash_key=self.data["id"],
            attributes_to_get=[
                "id",
                "html_download_at",
            ]
        )
        dt_now = datetime.utcnow()
        dt_html_download_at = parse(startup.html_download_at)
        if (dt_now - dt_html_download_at).total_seconds() > config.HTML_UPDATE_INTERVAL_IN_SECONDS.get_value():
            url = startup.url
            html = requests.get(url).text
            compressed_raw_html = gzip.compress(html.encode("utf-8"))
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


QueueItem._init_method_mapper()
