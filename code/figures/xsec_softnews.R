renv::activate()

library(tidyverse)
library(dplyr)
library(haven)
library(ggplot2)

source_slant_data <- read_csv("data/validation/hungarian_media_slant.csv")

raw <- read_csv("data/clean/citation_data_sample.csv") %>%
  filter(!section %in% c("belfold", "kulfold", "gazdasag")) %>% # filter for 'soft news'
  filter(date >= "2019-07-01" & date < "2020-07-01") %>%
  filter(source != "origo.hu" & source != "24.hu") %>%
  mutate(origo = ifelse(page == "origo.hu", 1, 0)) %>%
  merge(source_slant_data, all.x = TRUE, by = "source") %>%
  filter(!is.na(pro_govt))

slant_mean_estimates <- raw %>%
  group_by(source) %>%
  dplyr::summarise(
    alignment_score = mean(origo, na.rm = TRUE),
    se = sd(origo, na.rm = TRUE) / sqrt(n()),
    total_cites = n(),
    origo_cites = sum(origo),
    hn_cites = total_cites - origo_cites
  ) %>%
  mutate(
    alignment_score = 200 * (alignment_score - 0.5),
    se = 200 * se,
    low_ci = alignment_score - 1.96 * se,
    upper_ci = alignment_score + 1.96 * se,
    source = as.factor(source)
  ) %>%
  filter((upper_ci - low_ci) < 50) %>%
  mutate(low_ci = ifelse(low_ci < -100, -100, low_ci)) %>%
  mutate(upper_ci = ifelse(upper_ci > 100, 100, upper_ci))

slant_mean_estimates <- slant_mean_estimates %>%
  merge(source_slant_data, all.x = TRUE, by = "source") %>%
  mutate(pro_govt = ifelse(source == "nol.hu", 0, pro_govt)) %>%
  mutate(pro_govt = ifelse(pro_govt == 1, "Pro-government", "Independent")) %>%
  separate(source, c("source", NA)) %>%
  mutate(source = ifelse(source == "hu", "euronews", source)) %>%
  mutate(source = ifelse(source == "mno", "Magyar Nemzet", source))


ggplot(
  slant_mean_estimates,
  aes(
    x = reorder(source, alignment_score), y = alignment_score, shape = pro_govt
  )
) +
  geom_point(aes(size = pro_govt)) +
  coord_flip() +
  scale_y_continuous(limits = c(-100, 100), breaks = seq(-100, 100, by = 50)) +
  geom_errorbar(aes(ymin = low_ci, ymax = upper_ci),
    width = 0.4,
    alpha = 0.5
  ) +
  scale_shape_manual(values = c(1, 17)) +
  scale_size_manual(values = c(1.3, 2)) +
  theme_bw() +
  labs(title = "", x = "", y = "Alignment score") +
  theme(legend.position = "right", legend.title = element_blank())

ggsave(
  "results/figures/xsec_softnews.png",
  device = "png", dpi = "print", width = 8, height = 5
)
