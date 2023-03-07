# VARIABLES

PYTHON = pipenv run python3 -b
R = R CMD BATCH
FIGURES = xsec dynamic xsec_hardnews xsec_softnews dynamic_hardnews dynamic_softnews readership_xsec readership_ts alignment_score_by_number_of_citations n_citations_cdf
TABLES = number_of_articles hun_citations_sample_by_year_page citations_by_year_page

# REPLICATE ALL

.PHONY: all
all: $(foreach figure, $(FIGURES), results/figures/$(figure).png) $(foreach table, $(TABLES), results/tables/$(table).tex)
	rm -f Rplots.pdf
	rm -f .RData
	rm -f .Rhistory

# FIGURES

results/figures/%.png: code/figures/%.R data/clean/citation_data_sample.csv data/validation/hungarian_media_slant.csv data/clean/readership.csv
	$(R) $< results/logs/$*.Rout

results/figures/%.png: code/figures/%.py data/clean/citation_data.csv data/clean/citation_data_sample.csv
	$(PYTHON) $^

# TABLES

results/tables/%.tex: code/tables/%.py data/clean/citation_data_sample.csv data/clean/citation_data.csv data/raw/citation/newspaper_citations_data_raw.csv
	$(PYTHON) $^


# PREPARE DATA

data/clean/readership.csv: code/data-processing/readership.py data/raw/gemius/*
	$(PYTHON) $^

data/clean/citation_data_sample.csv: code/data-processing/citation_data_sample.py data/validation/hungarian_media_slant.csv data/clean/citation_data.csv
	$(PYTHON) $^

data/clean/citation_data.csv: code/data-processing/citation_data.py data/raw/citation/newspaper_citations_data_raw.csv
	$(PYTHON) $^

data/raw/citation/newspaper_citations_data_raw.csv: data/raw/citation/newspaper_citations_data_raw.zip
	unzip -n data/raw/citation/newspaper_citations_data_raw.zip -d data/raw/citation

# INSTALL
install:
	mkdir -p results/tables
	mkdir -p results/figures
	mkdir -p results/logs
	mkdir -p data/clean
	pipenv sync	
	$(R) code/activate_renv.R results/logs/activate_renv.Rout