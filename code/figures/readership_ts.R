renv::activate()

library(tidyverse)
library(dplyr)
library(haven)
library(ggplot2)

read_csv("data/clean/readership.csv") %>%
  filter(date < " 2022-01-01") %>%
  filter(page %in% c("origo.hu", "24.hu")) %>%
  separate(page, c("page", NA)) %>%
  ggplot(aes(x = date, y = readership_perc, linetype = page)) +
  geom_line() +
  labs(x = "Date", y = "Share of daily internet users") +
  scale_y_continuous(labels = scales::percent, limit = c(0, 0.8)) +
  theme_bw()

ggsave(
  "results/figures/readership_ts.png",
  device = "png", dpi = "print", width = 7, height = 5
)
