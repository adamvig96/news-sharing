#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

citation_data = pd.read_csv("data/clean/citation_data.csv")

citation_data["origo_cite"] = citation_data["source_url"].str.contains("origo.hu")
citation_data["24_cite"] = citation_data["source_url"].str.contains("24.hu")
citation_data["hungarian_cite"] = citation_data["source_url"].str.contains(".hu")
citation_data["self_citation"] = (
    (citation_data["page"] == "origo.hu") & (citation_data["origo_cite"])
) | ((citation_data["page"] == "24.hu") & (citation_data["24_cite"]))

# drop self citaitons and keep only hungarian cites
citation_data = citation_data.loc[lambda x: x["hungarian_cite"] == True, :].loc[
    lambda x: x["self_citation"] == False, :
]

# strip urls to source
citation_data["source"] = (
    citation_data["source_url"]
    .str.replace("'", "", regex=False)
    .str.replace("http://", "", regex=False)
    .str.replace("https://", "", regex=False)
    .str.strip()
    .str.split("/")
    .str[0]
    .str.strip()
    .str.replace("www.", "", regex=False)
    .str.replace("hu.", "", regex=False)
    .str.split(".")
    .str[:-1]
    .str.join(".")
)

# drop if there are more than one citation from one source in an article
citation_data = citation_data.drop_duplicates(subset=["url", "source"])

# Unify sites where home url changed
citation_data["source"] = np.where(
    citation_data["source"] == "mno", "magyarnemzet", citation_data["source"]
)

# estimate alignment scores

citation_data["origo_cited"] = citation_data["page"] == "origo.hu"
alignment_scores = (
    citation_data.groupby("source")
    .agg(
        total_cite_count=("url", "count"),
        alignment_score=("origo_cited", "mean"),
        std=("origo_cited", "std"),
    )
    .reset_index()
    .loc[lambda x: x["total_cite_count"] > 30]
    .assign(se=lambda x: x["std"] / x["total_cite_count"].apply(np.sqrt) * 200)
    .assign(alignment_score=lambda x: 200 * (x["alignment_score"] - 0.5))
)

alignment_scores = alignment_scores.loc[lambda x: x["source"] != "police"]
alignment_scores = alignment_scores.reset_index(drop=True)

hun_media_sample = pd.read_csv("data/clean/citation_data_sample.csv")["source"].unique()
hun_media_sample = [i.replace(".hu", "") for i in hun_media_sample]
hun_media_sample.append("magyarnemzet")

alignment_scores["our_sample"] = alignment_scores["source"].isin(hun_media_sample)


_, ax1 = plt.subplots(1, 1, figsize=(6, 5))

sns.ecdfplot(
    alignment_scores,
    y="total_cite_count",
    log_scale=True,
    color="grey",
    stat="count",
    complementary=True,
    ax=ax1,
)
ax1.set_xlabel("Number of domains")
ax1.set_ylabel("Total number of citations")


plt.savefig("results/figures/n_citations_cdf.png", dpi=250)
