# -*- coding: utf-8 -*-

from superjson import json
from seedinvest_monitor.model import Startup

data = list()
cursor = Startup.scan(attributes_to_get=["id", "details"])
for startup in cursor:
    data.append(startup.details.as_dict())
json.dump(data, "data.json", pretty=True, overwrite=True)
