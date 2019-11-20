# -*- coding: utf-8 -*-

import typing
from attrs_mate import attr, AttrsClass


@attr.s
class DownloadEvent(object):
    url = attr.ib() # type: str


@attr.s
class LbdEvent(AttrsClass):
    event_type = attr.ib() # type: str
    event_data = attr.ib() # type: typing.Union[DownloadEvent]

    class EventType:
        download = "download"
