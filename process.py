import pandas as pd
import numpy as np
from pathlib import Path
import json

from google.cloud import bigquery

WG1_INPUT_DOI_FOLDER = Path('data') / '10.5281_zenodo.5475442' / 'vers_1' / 'json_files'
WG1_FILES = ['ipcc_6_refs_assessmentreport_wg1.json'] #, 'ipcc_6_refs_specialreports.json']
WG2_INPUT_DOIS = Path('data') / 'IPCC_AR6_WGII_dois.csv'


def process_dois():
    """
    Load DOIs from spreadsheet and re-organise for upload to BQ

    :return: pd.DataFrame df containing the DOIs by chapter
    """

    wg1 = pd.DataFrame()
    for f in WG1_FILES:
        with open(WG1_INPUT_DOI_FOLDER / f) as fp:
            data = json.load(fp)
            df = pd.DataFrame(data['data'])
            df['Report_part'] = df.report_section.str[13:]
            df['dois'] = df['id_doi']
            df['working_group'] = ['WG1'] * len(df)
            df['release_year'] = [2021] * len(df)
            df['annual_report'] = ['AR6'] * len(df)
            df['report_title'] = ['Climate Change 2021: The Physical Science Basis'] * len(df)
            wg1 = wg1.append(df[['Report_part', 'dois', 'working_group', 'release_year', 'annual_report', 'report_title']])

    wg2 = pd.read_csv(WG2_INPUT_DOIS)
    wg2['working_group'] = ['WG2'] * len(wg2)
    wg2['release_year'] = [2022] * len(wg2)
    wg2['annual_report'] = ['AR6'] * len(wg2)
    wg2['report_title'] = ['Climate Change 2022: Impacts, Adaptation and Vulnerability'] * len(wg2)

    bq_df = wg1.append(wg2, ignore_index=True)

    # all_dois = list(np.unique(df.dois))
    #
    # chapters = list(set(df.Report_part.values))
    # chapters.sort()
    # chapters = [c.replace('-', '_') for c in chapters]
    # bq_df = pd.DataFrame(columns=['doi'].extend(chapters))
    # bq_df['doi'] = all_dois
    #
    # for chapter in chapters:
    #     bq_df[chapter] = bq_df['doi'].isin(df[df.Report_part==chapter]['dois'])

    #bq_df.to_csv('ipcc.csv')
    bq_df.to_gbq(destination_table='ipcc_ar6.ipcc_ar6_combined_dois',
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
    i.*      

FROM 
    `utrecht-university.ipcc_ar6.ipcc_ar6_combined_dois` as i 
    LEFT OUTER JOIN `academic-observatory.observatory.doi20220226` as d on UPPER(TRIM(d.doi))=UPPER(TRIM(i.doi))
"""

    with bigquery.Client() as client:
        job_config = bigquery.QueryJobConfig(destination='utrecht-university.ipcc_ar6.combined_doi_table',
                                             create_disposition='CREATE_IF_NEEDED',
                                             write_disposition='WRITE_TRUNCATE')

        query_job = client.query(query, job_config=job_config)  # Make an API request.
        query_job.result()  # Wait for the job to complete.

    print('...completed')


if __name__ == '__main__':
    df = process_dois()
    generate_doi_table()
