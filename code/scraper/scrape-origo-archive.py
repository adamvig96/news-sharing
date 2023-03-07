import os
import re

import aswan
import numpy as np
import pandas as pd
import ray
import requests
from bs4 import BeautifulSoup

df_archivum = (
    pd.DataFrame(pd.date_range(start="1998-12-1", end="2021-8-16", freq="d"))
    .rename(columns={0: "date"})
    .assign(
        date=lambda x: x["date"].astype(str).str.replace("-", ""),
        year=lambda x: x["date"].str[:4],
        source="https://www.origo.hu/hir-archivum/",
    )
    .assign(source_url=lambda x: x["source"] + x["year"] + "/" + x["date"] + ".html")
)

link_list = df_archivum["source_url"].tolist()

config = aswan.AswanConfig.default_from_dir("origo-archive-urls")

url_table = config.get_prod_table("url")

project = aswan.Project(config)  # this creates the env directories by default


@project.register_handler
class UrlHandler(aswan.UrlHandler):
    def parse_soup(self, soup):

        articles = [article.get("href") for article in soup.select(".archive-cikk a")]

        return {"article": articles}


project.register_t2_table(url_table)


@project.register_t2_integrator
class UrlIntegrator(aswan.FlexibleDfParser):
    handlers = [UrlHandler]

    def get_t2_table(self):
        return url_table


def add_init_urls():
    archive_pages = link_list

    project.add_urls_to_handler(UrlHandler, archive_pages)


add_init_urls()

project.config.prod.batch_size = 500
project.config.prod.min_queue_size = 1000

project.start_monitor_process()

project.run()

ray.shutdown()


# organise to dataframe
clean = []

for pcev in project.handler_events(UrlHandler):
    paperd = pcev.content
    paperd["url"] = pcev.__dict__["url"]

    clean.append(paperd)

cleand = (
    pd.DataFrame(clean)
    .explode("article")
    .loc[lambda x: x["article"].notnull()]
    .assign(
        date=lambda x: x["article"]
        .apply(lambda x: re.findall("\d\d\d\d\d\d\d\d", x))
        .str[0]
    )
)

cleand["date"] = np.where(cleand["date"].isnull(), "20001120", cleand["date"])

cleand["section"] = (
    cleand["article"].str.split("https://www.origo.hu/").str[1].str.split("/").str[0]
)

cleand = cleand.assign(
    date=lambda x: x["date"].str[:4]
    + "-"
    + x["date"].str[4:6]
    + "-"
    + x["date"].str[6:]
)

cleand.drop_duplicates("article").rename(columns={"article": "url"}).to_csv(
    "origo_links.csv", index=False
)
