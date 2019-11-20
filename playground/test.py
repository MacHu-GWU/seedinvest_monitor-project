import requests
from pathlib_mate import PathCls as Path

p = Path("test.html")

url = "https://www.seedinvest.com/have.need/pre.seed/founders"
res = requests.get(url)

p.write_bytes(res.content)