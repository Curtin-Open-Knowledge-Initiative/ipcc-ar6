import pandas as pd
import numpy as np
from pathlib import Path

from google.cloud import bigquery

INPUT_DOIS = Path('data') / 'IPCC_AR6_WGII_dois.csv'


def process_dois():
    """
    Load DOIs from spreadsheet and re-organise for upload to BQ

    :return: pd.DataFrame df containing the DOIs by chapter
    """

    df = pd.read_csv(INPUT_DOIS)
    all_dois = list(np.unique(df.dois))

    chapters = list(set(df.Report_part.values))
    chapters.sort()
    bq_df = pd.DataFrame(columns=['doi'].extend(chapters))
    bq_df['doi'] = all_dois

    for chapter in chapters:
        bq_df[chapter] = bq_df['doi'].isin(df[df.Report_part==chapter]['dois'])

    bq_df.to_csv('ipcc.csv')
    bq_df.to_gbq(destination_table='ipcc_ar6.ipcc_ar6_dois',
                 project_id='utrecht-university',
                 if_exists='replace')
    return bq_df


def generate_doi_table():
    query = """
SELECT 
    UPPER(TRIM(i.doi)) as ipcc_doi,
    UPPER(TRIM(d.doi)) as crossref_doi,
    IF(d.doi is null, TRUE, FALSE) as unmatched_doi,
    crossref.published_year,
    crossref.type,
    mag.fields.level_0 as mag_fields,
    mag.fields.level_1 as mag_subfields,
    affiliations.institutions,
    affiliations.countries,
    affiliations.funders,
    unpaywall.*,
    i.* EXCEPT(doi),
    (SELECT ARRAY_AGG(x IGNORE NULLS) FROM UNNEST([
      IF(Chapter01, "Chapter 01", null),
      IF(Chapter02, "Chapter 02", null),
      IF(Chapter03, "Chapter 03", null),
      IF(Chapter04, "Chapter 04", null),
      IF(Chapter05, "Chapter 05", null),
      IF(Chapter06, "Chapter 06", null),
      IF(Chapter07, "Chapter 07", null),
      IF(Chapter08, "Chapter 08", null),
      IF(Chapter09, "Chapter 09", null),
      IF(Chapter10, "Chapter 10", null),
      IF(Chapter11, "Chapter 11", null),
      IF(Chapter12, "Chapter 12", null),
      IF(Chapter13, "Chapter 13", null),
      IF(Chapter14, "Chapter 14", null),
      IF(Chapter15, "Chapter 15", null),
      IF(Chapter16, "Chapter 16", null),
      IF(Chapter17, "Chapter 17", null),
      IF(Chapter18, "Chapter 18", null),
      IF(Cross_Chapter_Paper01, "Cross Chapter Paper 1", null),
      IF(Cross_Chapter_Paper02, "Cross Chapter Paper 2", null),
      IF(Cross_Chapter_Paper03, "Cross Chapter Paper 3", null),
      IF(Cross_Chapter_Paper04, "Cross Chapter Paper 4", null),
      IF(Cross_Chapter_Paper05, "Cross Chapter Paper 5", null),
      IF(Cross_Chapter_Paper06, "Cross Chapter Paper 6", null),
      IF(Cross_Chapter_Paper07, "Cross Chapter Paper 7", null)
     ]) x) as chapters      

FROM 
    `utrecht-university.ipcc_ar6.ipcc_ar6_dois` as i 
    LEFT OUTER JOIN `academic-observatory.observatory.doi20220226` as d on UPPER(TRIM(d.doi))=UPPER(TRIM(i.doi))
"""

    with bigquery.Client() as client:
        job_config = bigquery.QueryJobConfig(destination='utrecht-university.ipcc_arc6.doi_table',
                                             create_disposition='CREATE_IF_NEEDED',
                                             write_disposition='WRITE_TRUNCATE')

        query_job = client.query(query, job_config=job_config)  # Make an API request.
        query_job.result()  # Wait for the job to complete.

    print('...completed')


if __name__ == '__main__':
    df = process_dois()
    generate_doi_table()
