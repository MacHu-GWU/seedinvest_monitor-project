# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx
import requests
from pathlib_mate import Path
from sfm.fingerprint import fingerprint
from seedinvest_monitor.crawler import html_parser


def get_html(url):
    fpath = Path(__file__).change(new_basename="{}.html".format(fingerprint.of_text(url)))
    if fpath.exists():
        html = fpath.read_text(encoding="utf-8")
    else:
        # i am lazy, I don't want to login, session_id is the key
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            # "cookie": "csrftoken=9999JP9mz49NwmqfykyrMupzywy3XZNGgq7Rly23j0u2QuEHdDcOreAnWIjGIhtj; _ga=GA1.2.1853091755.1574187377; _gid=GA1.2.909819738.1574187377; intercom-id-aaaa73km=aaaa1111-18b1-48af-849d-94ad2564a3bc; ga_cid=1853091755.1574187377; sessionid=t2xtsqy6pkf3mkndvd8oljs102ffp6bc; intercom-session-aaaa73km=bXI5eG01b1pJdHlmSk9mYU1jSzZPNGVpWng0KzR6Snk3MngwUjJtNVRzWHhzSHlEenBqTXYyNDRwMWZaekxydC0tUmtTUVo1bjlaNmo3SDVIVFVhcGpCZz09--d927dd0ff0f890889144d645e77525943c851cf5"
        }
        res = requests.get(url, headers=headers)
        html = res.text
        fpath.write_text(html, encoding="utf-8")
    return html


def test_parse_offering_page():
    results = html_parser.parse_offering_page(get_html("https://www.seedinvest.com/offerings"))
    assert len(results) >= 10

def test_parse_project_page():
    result = html_parser.parse_project_page(get_html("https://www.seedinvest.com/nowrx/series.b"))


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
