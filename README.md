# Analysis of references in the IPCC AR6 WG2 Report of 2022

## Description
This repository contains data on 17,564 DOIs cited in the [IPCC Working Group 2 contribution to the Sixth Assessment Report](https://www.ipcc.ch/report/ar6/wg2/), and the code to link them to the dataset built at the Curtin Open Knowledge Initiative (COKI).

References were extracted from the report's PDFs (downloaded 2022-03-01) via [Scholarcy](https://www.scholarcy.com/) and exported as RIS and BibTeX files. DOI strings were identified from RIS files by pattern matching and saved as CSV file. The list of DOIs for each chapter and cross chapter paper was processed using a custom Python script to generate a pandas DataFrame which was saved as CSV file and uploaded to Google Big Query.

We used the main object table of the Academic Observatory, which combines information from Crossref, Unpaywall, Microsoft Academic, Open Citations, the Research Organization Registry and Geonames to enrich the DOIs with bibliographic information, affiliations, and open access status. A custom query was used to join and format the data and the resulting table was visualised in a Google DataStudio dashboard.

A brief descriptive analysis was provided as a blogpost on the COKI website. 


**The repository contains the following content:**

Data:  
- [data/scholarcy/RIS/](data/scholarcy/RIS/) - extracted references as RIS files  
- [data/scholarcy/BibTeX/](data/scholarcy/BibTex/)  - extracted references as BibTeX files  
- [IPCC_AR6_WGII_dois.csv](data/IPCC_AR6_WGII_dois.csv) - list of DOIs

Processing:  
- [preprocessing.txt](preprocessing.txt) - preprocessing steps for identifying and cleaning DOIs  
- [process.py](process.py) - Python script for transforming data and linking to COKI data through Google Big Query

Outcomes: [to add]  
- dataset (Zenodo)?
- blogpost as pdf?  
- [https://console.cloud.google.com/bigquery?project=utrecht-university&ws=!1m23!1m3!8m2!1s145441926252!2sd59dfac7972a45f8a2f5ee4ac866c34d!1m4!4m3!1sacademic-observatory!2sobservatory!3sdoi20220226!1m4!4m3!1sutrecht-university!2sipcc_ar6!3sdoi_table!1m3!3m2!1sutrecht-university!2sipcc_ar6!1m4!4m3!1sutrecht-university!2sipcc_ar6!3sipcc_ar6_dois&d=ipcc_ar6&p=utrecht-university&page=table&t=doi_table&pli=1&authuser=1](Dataset on BigQuery) - Requires a google account for access and bigquery account for querying  
- [https://datastudio.google.com/s/iVmaM6huxgk](Data Studio Dashboard) - Interactive analysis of the generated data


**Note on licenses:**
Data are made available under [CC0](https://creativecommons.org/publicdomain/zero/1.0/)



