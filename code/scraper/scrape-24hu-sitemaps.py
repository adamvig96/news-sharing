#!/usr/bin/env python
# coding: utf-8

import re

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


def parse_sitemaps(soup):
    return (
        pd.DataFrame(str(soup).split("<loc>"))
        .assign(sitemaps=lambda x: x[0].str.split("</loc>").str[0].str.strip())
        .iloc[1:, 1]
    )


sitemap_collection_url = "https://24.hu/app/uploads/sitemap/24.hu_sitemap.xml"

soup = BeautifulSoup(requests.get(sitemap_collection_url).content)

sitemap_urls = parse_sitemaps(soup)

url_lists_24hu = []
for url in sitemap_urls[1:]:  # without the first 'fresh' sitemap
    soup = BeautifulSoup(requests.get(url).content, features="lxml")
    url_lists_24hu.append(parse_sitemaps(soup))

url_list_24hu_all = (
    pd.concat(url_lists_24hu)
    .to_frame()
    .rename({"sitemaps": "url"}, axis=1)
    .drop_duplicates("url")
    .assign(
        regex_date=lambda x: x["url"].apply(
            lambda url: re.search("([0-9]{4}\/[0-9]{2}\/[0-9]{2})", url)
        )
    )
    .loc[lambda x: x["regex_date"].notnull()]
    .assign(date=lambda x: x["regex_date"].apply(lambda x: x[0].replace("/", "-")))
    .sort_values(by=["date"])
    .drop("regex_date", axis=1)
)

url_list_24hu_all.to_csv("24hu_links.csv", index=False)
