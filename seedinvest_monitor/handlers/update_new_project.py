# -*- coding: utf-8 -*-

from datetime import datetime

import requests

from seedinvest_monitor.crawler import url_builder, html_parser
from seedinvest_monitor.model import Startup

epoch = str(datetime(1970, 1, 1))


def handler(event, context):
    url = url_builder.url_offering()
    html = requests.get(url).text

    for offering_page_result in html_parser.parse_offering_page(html):
        try:
            _ = Startup.get(offering_page_result.startup_id)
        except Startup.DoesNotExist:
            startup = Startup(
                id=offering_page_result.startup_id,
                html_download_at=epoch,
                details_update_at=epoch,
            )
            startup.save()


if __name__ == "__main__":
    handler({}, {})
