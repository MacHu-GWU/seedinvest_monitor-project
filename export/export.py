# -*- coding: utf-8 -*-

import pandas as pd
from superjson import json
from seedinvest_monitor.model import Startup

json_data = list()
df_data = list()
df_columns = set()

cursor = Startup.scan(attributes_to_get=["id", "details"])
for startup in cursor:
    details_data = startup.details.as_dict()
    json_data.append(details_data)
    for key in details_data:
        df_columns.add(key)
    df_data.append(details_data)

df_columns = list(df_columns)
df_columns.sort()

json.dump(json_data, "startups-data.json", pretty=True, overwrite=True)
df = pd.DataFrame(df_data, columns=df_columns)
df.to_excel("startups-data.xlsx", sheet_name="data", index=False)
