# -*- coding: utf-8 -*-

import typing

import attr
import bs4
from attrs_mate import AttrsClass

DOMAIN = "https://www.seedinvest.com"


@attr.s
class OfferingPageResult(AttrsClass):
    startup_name = attr.ib()  # type: str
    series = attr.ib()  # type: str
    href = attr.ib()  # type: str

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


def extract_number_from_string(text):
    """Take number like string out of text.
    """
    numberstr_list = list()
    chunks = list()

    for char in text:
        if char.isdigit() or char == "." or char == ",":
            if char != ",":
                chunks.append(char)
        else:
            if len(chunks):
                numberstr_list.append("".join(chunks))
                chunks = list()

    if len(chunks):
        numberstr_list.append("".join(chunks))

    new_numberstr_list = list()

    for s in numberstr_list:
        try:
            float(s)
            new_numberstr_list.append(s)
        except:
            pass

    return new_numberstr_list


class ProjectPageParser(object):
    _getters = list()

    def parse(self, html):
        soup = bs4.BeautifulSoup(html, "html.parser")

        data = dict()
        for getter_method_name in self._getters:
            key = getter_method_name.replace("get_", "")
            try:
                value = getattr(self, getter_method_name)(soup)
            except:
                value = None
            data[key] = value

        return data

    def get_keywords(self, soup):
        div = soup.find("div", class_="column xs-16 large-6 xl-5 float-right")
        p = div.find("p", class_="plain-subtitle xs")
        return p.text

    def get_amount_raised(self, soup):
        amount_raised = None
        for ul in soup.find_all("ul", class_="no-bullet-list inline-list count-list"):
            for li in ul.find_all("li"):
                if "Amount raised" in li.text:
                    amount_raised = extract_number_from_string(li.text)[0]
        return amount_raised

    def get_total_investor(self, soup):
        total_investor = None
        for ul in soup.find_all("ul", class_="no-bullet-list inline-list count-list"):
            for li in ul.find_all("li"):
                if "Total investors" in li.text:
                    total_investor = extract_number_from_string(li.text)[0]
        return total_investor

    # def get_share_price(self, soup):
    #     share_price = None
    #     for ul in soup.find_all("ul", class_="no-bullet-list inline-list count-list"):
    #         for li in ul.find_all("li"):
    #             if "Share Price" in li.text:
    #                 share_price = extract_number_from_string(li.text)[0]
    #     return share_price

    # def get_minimum_investment(self, soup):
    #     minimum_investment = None
    #     for ul in soup.find_all("ul", class_="no-bullet-list inline-list count-list"):
    #         for li in ul.find_all("li"):
    #             if "Minimum" in li.text:
    #                 minimum_investment = extract_number_from_string(li.text)[0]
    #     return minimum_investment

    def get_valuation_cap(self, soup):
        valuation_cap = None
        for ul in soup.find_all("ul", class_="no-bullet-list inline-list count-list"):
            for li in ul.find_all("li"):
                if "Valuation cap" in li.text:
                    valuation_cap = extract_number_from_string(li.text)[0]
        return valuation_cap

    #---
    def get_company_description(self, soup):
        section = soup.find("section", id="about")
        return section.text

    def get_product(self, soup):
        section = soup.find("section", id="product")
        return section.text

    def get_founder_and_officers(self, soup):
        founder_and_officers = list()
        section = soup.find("section", id="founders")
        for div in section.find_all("div", class_="row"):
            text = div.text
            if text not in founder_and_officers:
                founder_and_officers.append(div.text)
        return founder_and_officers

    def get_investor_perks(self, soup):
        section = soup.find("section", id="investor_perks")
        return section.text

    def get_round_type(self, soup):
        round_type = None
        section = soup.find("section", id="termsheet")
        for li in section.find_all("li", class_="inline-term split-1-to-1"):
            if "Round type:" in li.text:
                round_type = li.text.split(":")[-1].strip()
        return round_type

    def get_round_size(self, soup):
        round_size = None
        section = soup.find("section", id="termsheet")
        for li in section.find_all("li", class_="inline-term split-1-to-1"):
            if "Round size:" in li.text:
                round_size = extract_number_from_string(li.text)[0]
        return round_size

    def get_raised_to_date(self, soup):
        raised_to_date = None
        section = soup.find("section", id="termsheet")
        for li in section.find_all("li", class_="inline-term split-1-to-1"):
            if "Raised to date:" in li.text:
                raised_to_date = extract_number_from_string(li.text)[0]
        return raised_to_date

    def get_minimum_investment(self, soup):
        minimum_investment = None
        section = soup.find("section", id="termsheet")
        for li in section.find_all("li", class_="inline-term split-1-to-1"):
            if "Minimum investment:" in li.text:
                minimum_investment = extract_number_from_string(li.text)[0]
        return minimum_investment

    def get_target_minimum(self, soup):
        target_minimum = None
        section = soup.find("section", id="termsheet")
        for li in section.find_all("li", class_="inline-term split-1-to-1"):
            if "Target Minimum:" in li.text:
                target_minimum = extract_number_from_string(li.text)[0]
        return target_minimum

    def get_round_security_type(self, soup):
        round_security_type = None
        section = soup.find("section", id="termsheet")
        for li in section.find_all("li", class_="inline-term split-1-to-1"):
            if "Security Type:" in li.text:
                round_security_type = li.text.split(":")[-1].strip()
        return round_security_type

    def get_share_price(self, soup):
        share_price = None
        section = soup.find("section", id="termsheet")
        for li in section.find_all("li", class_="inline-term split-1-to-1"):
            if "Share price:" in li.text:
                share_price = extract_number_from_string(li.text)[0]
        return share_price

    def get_pre_money_valuation(self, soup):
        pre_money_valuation = None
        section = soup.find("section", id="termsheet")
        for li in section.find_all("li", class_="inline-term split-1-to-1"):
            if "Pre-money valuation:" in li.text:
                pre_money_valuation = extract_number_from_string(li.text)[0]
        return pre_money_valuation

    def get_option_pool(self, soup):
        option_pool = None
        section = soup.find("section", id="termsheet")
        for li in section.find_all("li", class_="inline-term split-1-to-1"):
            if "Option pool:" in li.text:
                option_pool = extract_number_from_string(li.text)[0]
        return option_pool

    def get_faqs(self, soup):
        section = soup.find("section", id="faqs")
        return section.text

    @classmethod
    def _init_getters(cls):
        _getters = list()
        for k, v in cls.__dict__.items():
            if k.startswith("get_") and callable(v):
                _getters.append(k)
        cls._getters = _getters


ProjectPageParser._init_getters()

project_page_parser = ProjectPageParser()


def parse_project_page(html):
    return project_page_parser.parse(html)
