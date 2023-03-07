#!/usr/bin/env python
# coding: utf-8

import pandas as pd

citation_data = pd.read_csv("data/clean/citation_data.csv")
citation_data["year"] = citation_data["date"].str[:4]
citations_by_year_page = (
    citation_data.drop_duplicates("url")
    .groupby(["year", "page"])["url"]
    .count()
    .reset_index()
    .pivot(index="year", columns="page", values="url")
)

with open("results/tables/citations_by_year_page.tex", "w") as tf:
    tf.write(citations_by_year_page.to_latex())
