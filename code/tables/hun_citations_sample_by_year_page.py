#!/usr/bin/env python
# coding: utf-8

import pandas as pd

hun_citation_data = pd.read_csv("data/clean/citation_data_sample.csv")
hun_citation_data["year"] = hun_citation_data["date"].str[:4]
hun_citations_sample_by_year_page = (
    hun_citation_data.groupby(["year", "page"])["url"]
    .count()
    .reset_index()
    .pivot(index="year", columns="page", values="url")
)

with open("results/tables/hun_citations_sample_by_year_page.tex", "w") as tf:
    tf.write(hun_citations_sample_by_year_page.to_latex())
