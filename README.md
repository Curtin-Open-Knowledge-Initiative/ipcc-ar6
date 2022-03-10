# Analysis of references in the IPCC AR6 WG2 Report of 2022

## Description
This repository contains data on 17,419 DOIs cited in the [IPCC Working Group 2 contribution to the Sixth Assessment Report](https://www.ipcc.ch/report/ar6/wg2/), and the code to link them to the dataset built at the Curtin Open Knowledge Initiative (COKI).

References were extracted from the report's PDFs (downloaded 2022-03-01) via [Scholarcy](https://www.scholarcy.com/) and exported as RIS and BibTeX files. DOI strings were identified from RIS files by pattern matching and saved as CSV file. 

As not all reference information was processed correctly, DOIs were extracted from all fields, rather than just the DO field in the RIS files. The list of cleaned DOIs can still contain incomplete or otherwise invalid DOIs. Coverage of DOIs across chapters varies greatly, with some chapters having DOIs for almost all references, and other chapters lacking DOIs almost all together.

The list of DOIs for each chapter and cross chapter paper was processed using a custom Python script to generate a pandas DataFrame which was saved as CSV file and uploaded to Google Big Query.

We used the main object table of the Academic Observatory, which combines information from Crossref, Unpaywall, Microsoft Academic, Open Citations, the Research Organization Registry and Geonames to enrich the DOIs with bibliographic information, affiliations, and open access status. A custom query was used to join and format the data and the resulting table was visualised in a Google DataStudio dashboard.

This version of the repository also includes the set of DOIs from references in the [IPCC Working Group 1 contribution to the Sixth Assessment Report](https://www.ipcc.ch/report/ar6/wg1/) as extracted by Alexis-Michel Mugabushaka and shared on Zenodo: https://doi.org/10.5281/zenodo.5475442 (CC-BY)

A brief descriptive analysis was provided as a [blogpost on the COKI website](https://openknowledge.community/tracking-climate-change-openaccess/). 


**The repository contains the following content:**

Data:  
- [data/scholarcy/RIS/](data/scholarcy/RIS/) - extracted references as RIS files  
- [data/scholarcy/BibTeX/](data/scholarcy/BibTex/)  - extracted references as BibTeX files  
- [IPCC_AR6_WGII_dois.csv](data/IPCC_AR6_WGII_dois.csv) - list of DOIs  
- [data/10.5281_zenodo.5475442/](data/10.5281_zenodo.5475442) - references from IPCC AR6 WG1 report

Processing:  
- [preprocessing.R](preprocessing.R) - R script for preprocessing: identifying and cleaning DOIs  
- [process.py](process.py) - Python script for transforming data and linking to COKI data through Google Big Query

Outcomes:  
- [Dataset on BigQuery](https://console.cloud.google.com/bigquery?project=utrecht-university&ws=!1m23!1m3!8m2!1s145441926252!2sd59dfac7972a45f8a2f5ee4ac866c34d!1m4!4m3!1sacademic-observatory!2sobservatory!3sdoi20220226!1m4!4m3!1sutrecht-university!2sipcc_ar6!3sdoi_table!1m3!3m2!1sutrecht-university!2sipcc_ar6!1m4!4m3!1sutrecht-university!2sipcc_ar6!3sipcc_ar6_dois&d=ipcc_ar6&p=utrecht-university&page=table&t=doi_table&pli=1&authuser=1) - requires a google account for access and bigquery account for querying  
- [Data Studio Dashboard](https://datastudio.google.com/s/vZN2zLr9wS4) - interactive analysis of the generated data for WG1 and WG2  
- [Zotero library](https://www.zotero.org/groups/4614109) of references as extracted via Scholarcy  
- [PDF version of blogpost](IPCC%20AR6.pdf)


**Note on licenses:**   
Data are made available under [CC0](https://creativecommons.org/publicdomain/zero/1.0/), with the exception of WG1 reference data which have been shared under a CC-BY license.

**Archived version of this repositoy on Zenodo:**  
[doi: 10.5281/zenodo.6344388](https:/doi.org/10.5281/zenodo.6344388)



