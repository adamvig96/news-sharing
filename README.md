# README

Overview
--------

This replication package constructs the results for the paper titled *News-sharing as a measure of media alignment* by Gabor Simonovits and Adam Vig, published in the Journal of Quantitative Description: Digital Media. A Makefile runs all of the code to clean and organize the data and generates the tables and figures in the paper. The replicator should expect the code to run for about 2-3 minutes.

Data Availability and Provenance Statements
----------------------------

### Statement about Rights

- [x] I certify that the author(s) of the manuscript have legitimate access to and permission to use the data used in this manuscript. 


### License for Data

The code is licensed under a Creative Commons/CC-BY-NC/CC0 license. See [LICENSE](LICENSE) for details.


### Summary of Availability

- [x] All data **are** publicly available.
- [ ] Some data **cannot be made** publicly available.
- [ ] **No data can be made** publicly available.

### Details on each Data Source

The data were collected by the authors, and are available under a Creative Commons Non-commercial license. 

- **Database of citations on 24.hu and origo.hu**
`data/raw/newspaper_citations_data_raw.csv` were collected using scraping code writen in Python by the authors. Scraper code is available at the `code/scraper` folder. 


- **Validation data on the slant of Hungarian news portals**
`data/validation/hungarian_media_slant.csv` is from Bátorfy (2020).

- **Readership data for Hungarian domains**
There is a .csv or .xlsx file in the `data/raw/gemius/` folder named as gemius_YEAR_MONTH for each consecutive month which contains the number of real user for Hungarian domains estimated by Gemius (2022). 



Computational requirements
---------------------------

### Software Requirements

The following versions of Python, R and GNU Make were used by the authors:

- Python 3.10.0
- R 4.1.2
- GNU Make 3.81

Package requirements are stored in the `Pipfile.lock` and `renv.lock` files. [`pipenv`](https://pipenv.pypa.io/en/latest/) is used for Python, [`renv` ](https://rstudio.github.io/renv/index.html) for R dependency management. [CNU Make](https://www.gnu.org/software/make/) for execution.

> Note: requirements for scraping the citations database is listed in `requirements.txt` in the `code/scraper` folder.


### Memory and Runtime Requirements

#### Summary
 
A few minutes needed to reproduce the analyses on a standard 2023 desktop machine. The authors would not recommend running the scraper code on a destop machine.

#### Details

The analysis code were last run on a **8-core M1 Macbook Pro with 16 GB RAM and MacOS version 13.2**. 

The scraper code were last run on a **8-core AWS EC2 server with 32 GB of RAM**.



Instructions to Replicators
---------------------------

- **Scraper**

There is no master script for the scraper code. The scripts `scrape-24hu-sitemaps.py` and `scrape-origo-archive.py` collect the urls for every published article at `24.hu` or `origo.hu` respectively. `24hu_parser.py` and `origo_parser.py` contain parser functions for the sites. The functions parse the html script of one article published on 24.hu or origo.hu respectively. **The scraper codes were last executed on 2022.08.02.**

> Note: The parser functions might need modification to work properly, as the sites might change their HTML content since our last execution.


- **Analysis**

1. run `make install` in terminal to set up the environment and required folders for the analysis.
2. run `make` in terminal to clean and organize data and replicate the 7 figures and 3 tables used in the paper.


Description of `code`
----------------------------

- Scripts in `code/scraper` can be used to replicate the raw data used by the analysis.
- `code/activate_renv.R` is run by `make install` and activates the virtual environment for R.
- Scripts in `code/data-processing/`
    - clean and reformat the scraped citation database `data/raw/newspaper_citations_data_raw.csv`.
    - clean and concatenate the montly datafiles of real usership in `data/raw/gemius/`.
- Scripts in `code/figures` generate all figures in the main body and the appendix of the article.
- Scripts in `code/tables` generate all tables in the appendix of the article.

List of tables and figures with scripts
---------------------------------------

The provided code reproduces:

- [x] All numbers provided in text in the paper
- [x] All tables and figures in the paper

| Exhibit     | Script                              |
|-------------|-------------------------------------|
| Figure 1    | alignment_score_by_ncitations.py    |
| Figure 2    | xsec.R                              |
| Figure 3    | dynamic.R                           |
| Figure A1   | n_citations_cdf.py                  |
| Figure A2/a | readership_ts.R                     |
| Figure A2/b | readership_xsec.R                   |
| Figure A3/a | xsec_hardnews.R                     |
| Figure A3/b | xsec_softnews.R                     |
| Figure A4/a | dynamic_hardnews.R                  |
| Figure A4/b | dynamic_softnews.R                  |
| Table A1    | number_of_articles.R                |
| Table A2    | citations_by_year_page.R            |
| Table A3    | hun_citations_sample_by_year_page.R |

The output files are named after their corresponding script and are in `results/figures` or `results/tables`.


## References

- Bátorfy, Attila. 2020. “The past ten years of the Hungarian media.” https://atlo.team/media2020/
- gemiusAudience. 2022. “Number of real users for Hungarian online brands.” https://e-public.gemius.com/hu/
---
