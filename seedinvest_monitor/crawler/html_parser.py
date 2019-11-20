# -*- coding: utf-8 -*-

import typing
import bs4
import attr
from attrs_mate import AttrsClass


DOMAIN = "https://www.seedinvest.com"

@attr.s
class OfferingPageResult(AttrsClass):
    startup_name = attr.ib() # type: str
    series = attr.ib() # type: str
    href = attr.ib() # type: str

    @property
    def startup_id(self):
        return self.startup_name

    @property
    def url(self):
        return f"{DOMAIN}{self.href}"


def parse_offering_page(html) -> typing.List[OfferingPageResult]:
    results = list()
    soup = bs4.BeautifulSoup(html, "html.parser")
    for div_thumbnail_content in soup.find_all("div", class_="thumbnail-content"):
        a_thumbnail_hero_image = div_thumbnail_content.find("a", class_="thumbnail-hero-image-wrapper")
        if a_thumbnail_hero_image is not None:
            try:
                href = a_thumbnail_hero_image["href"]

                chunks = href.split("/")
                if len(chunks) != 3:
                    continue

                _, startup_name, series = chunks
                result = OfferingPageResult(
                    startup_name=startup_name,
                    series=series,
                    href=href,
                )
                results.append(result)
                # print(result.url)
            except Exception as e:
                pass

    return results


def parse_project_page(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
