renv::activate()

library(tidyverse)
library(dplyr)
library(haven)
library(ggplot2)
library(fixest)
library(lubridate)
library(zoo)
library(xtable)

mno_slant_estimate <- read_csv("data/clean/citation_data_sample.csv") %>%
  filter(!section %in% c("belfold", "kulfold", "gazdasag")) %>% # filter for 'soft news'
  filter(date > "2016-06-30" & date < "2021-07-01") %>%
  filter(source == "mno.hu") %>%
  mutate(ym = substr(date, 1, 7)) %>%
  select(ym, page, source) %>%
  mutate(year = as.factor(substr(ym, 1, 4))) %>%
  mutate(ym = as.Date(paste(ym, "-01", sep = ""))) %>%
  mutate(quarter = lubridate::quarter(ym, with_year = FALSE)) %>%
  mutate(date = as.yearqtr(paste(year, quarter, sep = "-"))) %>%
  mutate(nerpage = ifelse(page == "origo.hu", 1, 0)) %>%
  group_by(date, source) %>%
  dplyr::summarise(
    alignment_score = mean(nerpage, na.rm = TRUE),
    se = sd(nerpage, na.rm = TRUE) / sqrt(n()),
    total_cites = n()
  ) %>%
  mutate(alignment_score = ifelse(
    (date == as.yearqtr("2018-03") & (source == "mno.hu")), NA, alignment_score
  )) %>%
  mutate(alignment_score = ifelse(
    (date == as.yearqtr("2018-04") & (source == "mno.hu")), NA, alignment_score
  )) %>%
  mutate(
    alignment_score = 200 * (alignment_score - 0.5),
    se = 200 * se,
    low_ci = alignment_score - 1.96 * se,
    upper_ci = alignment_score + 1.96 * se
  ) %>%
  mutate(low_ci = ifelse(low_ci < -100, -100, low_ci))

ggplot(mno_slant_estimate, aes(x = date, y = alignment_score)) +
  geom_line(size = 0.6) +
  geom_point() +
  geom_ribbon(aes(ymin = low_ci, ymax = upper_ci), alpha = 0.4) +
  scale_x_yearqtr(format = "%Y", expand = c(0.02, 0.02)) +
  scale_y_continuous(limits = c(-105, 100), expand = c(0.01, 0.01)) +
  geom_vline(
    xintercept = as.yearqtr("2019-1"),
    linetype = "dashed",
    color = "black"
  ) +
  annotate("text",
    x = as.yearqtr("2018-4"), y = 40,
    label = "capture of Magyar Nemzet", size = 3, color = "black", angle = 90
  ) +
  theme_bw() +
  xlab("") +
  ylab("Alingment score of Magyar Nemzet")


ggsave("results/figures/dynamic_softnews.png",
  device = "png", dpi = "print", width = 8, height = 5
)
