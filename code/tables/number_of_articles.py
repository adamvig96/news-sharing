#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np


raw = pd.read_csv("data/raw/citation/newspaper_citations_data_raw.csv")
raw["contains_citation"] = raw["source_urls"] != "[]"
citation_statistics = (
    raw.groupby("page")
    .agg(n_articles=("url", "count"), citation=("contains_citation", "sum"))
    .rename(
        columns={
            "n_articles": "Number of articles",
            "citation": "Article contains citation",
        }
    )
)


citation_data = pd.read_csv("data/clean/citation_data.csv")
citation_data["origo_cite"] = citation_data["source_url"].str.contains("origo.hu")
citation_data["24_cite"] = citation_data["source_url"].str.contains("24.hu")
citation_data["hungarian_cite"] = citation_data["source_url"].str.contains(".hu")
citation_data["self_citation"] = (
    (citation_data["page"] == "origo.hu") & (citation_data["origo_cite"])
) | ((citation_data["page"] == "24.hu") & (citation_data["24_cite"]))

self_citations = (
    citation_data.groupby("url")
    .agg(
        page=("page", "first"),
        self_citation=("self_citation", "sum"),
        number_of_citation=("url", "count"),
    )
    .loc[
        lambda x: (x["self_citation"] != 0)
        & (x["self_citation"] == x["number_of_citation"]),
        "page",
    ]
    .value_counts()
)
foreign_citations = (
    citation_data.groupby(["page", "url"])
    .agg(hu_cited=("hungarian_cite", "sum"))
    .assign(foreign_cited=lambda x: np.where(x["hu_cited"] == 0, True, False))
    .reset_index()
    .loc[lambda x: x["foreign_cited"], "page"]
    .value_counts()
)


hun_citation_data = pd.read_csv("data/clean/citation_data_sample.csv")
hungarian_media_sample = hun_citation_data["page"].value_counts()

citation_statistics["'Self citation'"] = self_citations
citation_statistics["Foreign outlets"] = foreign_citations
citation_statistics["Hungarian media sample"] = hungarian_media_sample
citation_statistics = pd.concat(
    [citation_statistics, citation_statistics.sum(axis=0).rename("Total").to_frame().T]
).T


with open("results/tables/number_of_articles.tex", "w") as tf:
    tf.write(citation_statistics.to_latex())
