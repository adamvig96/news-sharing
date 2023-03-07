#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import os


folder_path = "data/raw/gemius/"
files_csv = [folder_path + file for file in os.listdir(folder_path) if ".csv" in file]
files_xlsx = [folder_path + file for file in os.listdir(folder_path) if ".xlsx" in file]


# clean .csv files
csv_file_list = []
for file in files_csv:
    df = pd.read_csv(file, sep="delimiter", engine="python").iloc[7:, :]
    df = df.loc[: df.loc[lambda x: x["# Táblázat"] == "# Diagramm"].index[0] - 1, :]
    df = df.rename({"# Táblázat": 0}, axis=1)
    df = pd.DataFrame(df[0].str.replace('"', "").str.split(",").tolist())
    df.columns = df.iloc[0, :]
    df = df.iloc[1:, :]
    df["page"] = df["Node"].str.split("|").str[1].str.strip().fillna("Internet")
    df["real_users"] = df["Real users"].astype(int)
    df["date"] = (
        pd.read_csv(file, sep="delimiter", engine="python")
        .loc[lambda x: x["# Táblázat"].str.contains('"Periódus"')]
        .values[0][0]
        .split(",")[1]
        .replace('"', "")
        .split(" - ")[0]
    )

    df = df.filter(["page", "date", "real_users"])

    csv_file_list.append(df)

df_csv = pd.concat(csv_file_list)


# ## clean .xslx files

xlsx_file_list = []
for file in files_xlsx:
    df = (
        pd.read_excel(file, sheet_name=0)
        .rename({"Media channel": "page"}, axis=1)
        .assign(real_users=lambda x: x["Real users"].astype(int))
        .filter(["page", "real_users"])
        .assign(
            date=pd.read_excel(file, sheet_name=1)
            .loc[lambda x: x["Report"] == "Time period", "Websites"]
            .values[0]
        )
    )
    xlsx_file_list.append(df)


month_map = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12",
}


df_xlsx = (
    pd.concat(xlsx_file_list)
    .assign(
        month=lambda x: x["date"].str.split(" ").str[0].str.strip().map(month_map),
        year=lambda x: x["date"].str.split(" ").str[1].str.strip(),
    )
    .assign(date=lambda x: x["year"] + "-" + x["month"] + "-01")
    .filter(["page", "date", "real_users"])
)


# concat

df_clean = pd.concat([df_csv, df_xlsx]).reset_index(drop=True)

df_clean = df_clean.assign(date=lambda x: pd.to_datetime(x["date"], format="%Y-%m-%d"))

df_clean["page"] = np.where(
    df_clean["page"] == "mno.hu", "magyarnemzet.hu", df_clean["page"]
)
df_clean["page"] = np.where(
    df_clean["page"] == "All media channels", "Internet", df_clean["page"]
)
df_clean["date"] = pd.to_datetime(df_clean["date"])
df_clean.loc[
    lambda x: (x["page"] == "magyarnemzet.hu")
    & ((x["date"] > "2019-02-01") & (x["date"] < "2020-03-01")),
    "real_users",
] = None


internet_users = df_clean.loc[
    lambda x: x["page"] == "Internet", ["date", "real_users"]
].rename(columns={"real_users": "internet_penetration"})


df_clean = (
    df_clean.loc[lambda x: x["page"] != "Internet"]
    .merge(internet_users, on="date", how="left")
    .assign(readership_perc=lambda x: x["real_users"] / x["internet_penetration"])
)


df_clean.to_csv("data/clean/readership.csv", index=False)
