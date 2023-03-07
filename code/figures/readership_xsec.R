renv::activate()

library(tidyverse)
library(dplyr)
library(haven)
library(ggplot2)

source_slant_data <- read_csv("data/validation/hungarian_media_slant.csv")

gemius <- read_csv("data/clean/readership.csv") %>%
  filter(date < " 2022-01-01")

gemius %>%
  filter(page %in% c(
    source_slant_data$source,
    c("origo.hu", "24.hu")
  )) %>%
  mutate(sources = ifelse(page %in% c("origo.hu", "24.hu"), "page", "source")) %>%
  separate(page, c("page", NA)) %>%
  mutate(page = ifelse(page == "hu", "euronews", page)) %>%
  mutate(page = ifelse(page == "mno", "Magyar Nemzet", page)) %>%
  group_by(page) %>%
  summarise(
    mean_readership_share = mean(readership_perc),
    sources = first(sources)
  ) %>%
  ggplot(aes(
    x = reorder(page, mean_readership_share),
    y = mean_readership_share,
    fill = sources
  )) +
  coord_flip() +
  geom_col() +
  scale_fill_grey() +
  scale_y_continuous(labels = scales::percent, limit = c(0, 0.8)) +
  labs(x = "", y = "Share of daily internet users") +
  theme_bw() +
  theme(legend.position = "none")

ggsave(
  "results/figures/readership_xsec.png",
  device = "png", dpi = "print", width = 7, height = 5
)
