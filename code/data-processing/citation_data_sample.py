#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

# read sources
hun_sources = pd.read_csv("data/validation/hungarian_media_slant.csv")["source"]

sources = hun_sources.unique().tolist()
sources = sorted(sources, reverse=True)

# read raw data
data = pd.read_csv("data/clean/citation_data.csv")

data = data.dropna(subset=["source_url"])

for i in [
    ("'", ""),
    ('"', ""),
    ("\\", ""),
    ("www.investor.hu", "www.origo.hu"),
    ("magyarnemzet.hu", "mno.hu"),
    ("fn.hu", "24.hu"),
    ("napigazdasag.hu", "magyaridok.hu"),
    ("/valasz.hu", "/hetivalasz.hu"),
]:
    data["source_url"] = (
        data["source_url"].str.strip().str.replace(i[0], i[1], regex=False)
    )

# search in only the first part of the URL, as sites may refer to other sites later in the URL
data["source_url_short"] = data["source_url"].str[:33]

# create source variable
data["source"] = None
for source in sources:
    data.loc[lambda x: x["source_url_short"].str.contains(source), "source"] = source

# drop helper columns
data = data.drop("source_url_short", axis=1)

# drop if source not found
data = data.loc[lambda x: x["source"].notnull()]

# unify hard-news sections
data["section"] = np.where(data["section"] == "itthon", "belfold", data["section"])
data["section"] = np.where(data["section"] == "nagyvilag", "kulfold", data["section"])
data["section"] = np.where(data["section"] == "kozelet", "belfold", data["section"])
data["section"] = np.where(
    data["section"] == "uzleti-tippek", "gazdasag", data["section"]
)
data["section"] = np.where(data["section"] == "penzugy", "gazdasag", data["section"])

# drop if there are more than one citation from one source in an article
data = data.drop_duplicates(["url", "source"])

data.to_csv("data/clean/citation_data_sample.csv", index=False)
