#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

# read raw data
data = pd.read_csv("data/raw/citation/newspaper_citations_data_raw.csv")
data = data.loc[lambda x: (x["date"] >= "2016-01-01") & (x["date"] < "2022-01-01")]

# drop where url existed, but the actual page is now removed from the site
data = data.loc[lambda x: (x["date"].notnull()) & (x["section"].notnull())]

# drop accidentaly left duplicates (by url)
data = data.drop_duplicates("url")

# drop if article does not contain source url
data = data.loc[
    lambda x: (x.source_urls != "[]")
    & (x.source_urls != "")
    & (x.source_urls.notnull())
]

# explode by source url list, to get article - source url level observations
data = data.assign(
    source_urls=lambda x: x.source_urls.str.replace("[", "", regex=False)
    .str.replace("]", "", regex=False)
    .str.split(",")
)

data = data.explode("source_urls")

data = data.rename({"source_urls": "source_url"}, axis=1)

data.to_csv("data/clean/citation_data.csv", index=False)
