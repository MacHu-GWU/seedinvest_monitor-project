# -*- coding: utf-8 -*-

import gzip
from datetime import datetime

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

    def process(self):
        method_name = self._method_mapper[self.type]
        getattr(self, method_name)()

    def process_download_project_html(self):
        startup = Startup.get(self.data["id"])
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


QueueItem._init_method_mapper()
