# -*- coding: utf-8 -*-

import os
from attrs_mate import attr, AttrsClass
from troposphere_mate import NOTHING
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, BinaryAttribute, MapAttribute
from seedinvest_monitor.devops.config_init import config

if not config.is_aws_lambda_runtime():
    os.environ["AWS_DEFAULT_PROFILE"] = config.AWS_PROFILE_FOR_PYTHON.get_value()


# @attr.s
# class Details(AttrsClass):
#     issuer = attr.ib(default=NOTHING)
#     issuer = attr.ib(default=NOTHING)
#     issuer = attr.ib(default=NOTHING)
#     issuer = attr.ib(default=NOTHING)
#     issuer = attr.ib(default=NOTHING)
#     issuer = attr.ib(default=NOTHING)
#     issuer = attr.ib(default=NOTHING)
#     issuer = attr.ib(default=NOTHING)
#     issuer = attr.ib(default=NOTHING)
#     issuer = attr.ib(default=NOTHING)
#     issuer = attr.ib(default=NOTHING)
#     issuer = attr.ib(default=NOTHING)
#     issuer = attr.ib(default=NOTHING)
#     issuer = attr.ib(default=NOTHING)
#     issuer = attr.ib(default=NOTHING)


class Startup(Model):
    class Meta:
        table_name = config.DYNAMODB_TABLE_STARTUP.get_value()

    id = UnicodeAttribute(hash_key=True)
    project_create_at = UnicodeAttribute(null=True)
    raw_html = BinaryAttribute(null=True)
    html_download_at = UnicodeAttribute(null=True)
    details = MapAttribute(null=True)
    details_update_at = UnicodeAttribute(null=True)


class Event(Model):
    class Meta:
        table_name = "event"

    id = UnicodeAttribute(hash_key=True)
    value = NumberAttribute(null=True)


if __name__ == "__main__":
    res = Event.query(hash_key="a1")
    print(list(res))

    res = Event.scan(Event.time > "2019-03-01")
    print(list(res))

    event = Event(id="a1", value=3)
    event.save()
    try:
        event = Event.get("a2")
    except Event.DoesNotExist:
        print(1)
    event.update(actions=[Event.value.set(3)])
