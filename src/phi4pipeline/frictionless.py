import hashlib
import importlib.resources
import json
import os
import re
from os import PathLike
from string import Template

import pandas as pd

DATA_DIR = importlib.resources.files('phi4pipeline') / 'metadata'


def load_formatted_datapackage(format_args: dict[str, str], contributors: dict) -> dict:
    template_path = DATA_DIR / 'datapackage_template.json'
    with open(template_path, encoding='utf-8') as file:
        template_str = file.read()
    template = Template(template_str)
    datapackage = json.loads(template.substitute(**format_args))
    for resource in datapackage['resources']:
        resource['bytes'] = int(resource['bytes'])
    # Extra caution: explicitly check for NaN since NaN is truthy
    contributors_with_orcid = (
        c for c in contributors if c['orcid'] and pd.notna(c['orcid'])
    )
    datapackage['contributors'] = [
        {
            'title': 'Anonymous contributor',
            'path': f'https://orcid.org/{contrib["orcid"]}',
            'role': 'contributor',
        }
        for contrib in contributors_with_orcid
    ]
    return datapackage


def anonymize_contributors(contributors_data):

    def anonymize(contributor):
        contributor = contributor.copy()
        # Be extra careful to default to anonymization here
        if contributor['is_private'] is not False:
            contributor['name'] = 'Anonymous'
            contributor['affiliation'] = ''
        return contributor

    anonymized_contributors = map(anonymize, contributors_data)

    # No point including private contributors with no ORCID ID, since
    # we can't provide any useful information about them.
    filtered_contributors = [
        d for d in anonymized_contributors
        if not (d['is_private'] and not d['orcid'])
    ]
    return filtered_contributors


def format_datapackage_readme(
    readme_str: str,
    *,
    format_args: dict[str, str],
    contributors_data: list[dict[str, str]],
    data_stats: dict[str, int],
    data_dict: dict,
) -> str:

    TABLE_FORMAT = 'github'

    def make_contributors_table(contributors_data):
        orcid_pattern = re.compile(r'^(\d{4}-\d{4}-\d{4}-(?:\d{4}|\d{3}X))$')
        renames = {
            'name': 'Name',
            'orcid': 'ORCID ID',
            'affiliation': 'Affiliation',
            'role_readme': 'Role',
        }
        include_columns = list(renames.keys())
        df = pd.DataFrame.from_records(contributors_data)
        df.name = df.name.replace('', 'Anonymous')
        df.orcid = df.orcid.fillna('').str.replace(
            pat=orcid_pattern, repl=r'[\1](https://orcid.org/\1)', regex=True
        )
        display_df = df[include_columns].rename(columns=renames)
        table_str = display_df.to_markdown(index=False, tablefmt=TABLE_FORMAT)
        return table_str

    def make_data_stats_table(data_stats):
        renames = {
            'n_pubs': ' Publications',
            'n_interactions': ' Pathogen-host interactions',
            'n_pathogen_genes': 'Pathogen genes',
            'n_pathogens': 'Pathogen species',
            'n_hosts': 'Host species',
        }
        table_str = (
            pd.DataFrame.from_records([data_stats], index=['Count'])
            .rename(columns=renames)
            .transpose()
            .rename_axis('Data Type')
            .to_markdown(tablefmt=TABLE_FORMAT)
        )
        return table_str

    def make_data_dict_table(data_dict):
        renames = {
            'name': 'Column',
            'title': 'Name',
            'type': 'Type',
            'description': 'Description',
        }
        columns = list(renames.keys())
        table_str = (
            pd.DataFrame.from_records(data_dict['fields'])[columns]
            .rename(columns=renames)
            .to_markdown(index=False, tablefmt=TABLE_FORMAT)
        )
        return table_str

    authors = [d for d in contributors_data if d['is_author']]
    contributors = [d for d in contributors_data if not d['is_author']]

    format_args_tables = {
        'authors_table': make_contributors_table(authors),
        'contributors_table': make_contributors_table(contributors),
        'data_dictionary': make_data_dict_table(data_dict),
        'data_stats_table': make_data_stats_table(data_stats),
    }
    formatted_readme_str = readme_str.format(**format_args, **format_args_tables)
    return formatted_readme_str


def get_file_sha1_hash(path: PathLike) -> str:
    with open(path, 'rb') as file:
        file_hash = hashlib.sha1(file.read()).hexdigest()
    return file_hash


def make_datapackage_json(
    csv_path: PathLike,
    fasta_path: PathLike,
    *,
    version: str,
    doi: str,
    contributors: dict,
) -> dict:
    phibase_hash, fasta_hash = (
        get_file_sha1_hash(path) for path in (csv_path, fasta_path)
    )
    phibase_bytes, fasta_bytes = (
        os.path.getsize(path) for path in (csv_path, fasta_path)
    )
    format_args = {
        'version': version,
        'doi': f'https://doi.org/{doi}',
        'phibase_hash': phibase_hash,
        'phibase_bytes': phibase_bytes,
        'fasta_hash': fasta_hash,
        'fasta_bytes': fasta_bytes,
    }
    return load_formatted_datapackage(format_args, contributors)


def get_data_stats(phi_df: pd.DataFrame) -> dict[str, int]:
    return {
        'n_pubs': phi_df.pmid.nunique(),
        'n_interactions': (
            phi_df[['pathogen_species', 'host_species']]
            .drop_duplicates()
            .value_counts()
            .sum()
        ),
        'n_pathogen_genes': phi_df.gene.nunique(),
        'n_pathogens': phi_df.pathogen_species.nunique(),
        'n_hosts': phi_df.host_species.nunique(),
    }


def make_datapackage_readme(
    csv_path: PathLike,
    version: str,
    semver: str,
    year: int | str,
    doi: str,
    contributors_data: list[dict[str, str]],
) -> str:
    with open(DATA_DIR / 'readme_template.md', encoding='utf-8') as file:
        readme_str = file.read()
    with open(DATA_DIR / 'phi-base_schema.json', encoding='utf-8') as file:
        data_dict = json.load(file)

    data_stats = get_data_stats(pd.read_csv(csv_path, low_memory=False))
    format_args = {
        'version': version,
        'semver': semver,
        'year': f'{year}',
        'doi': doi,
        'doi_url': f'https://doi.org/{doi}',
    }
    return format_datapackage_readme(
        readme_str,
        format_args=format_args,
        contributors_data=contributors_data,
        data_stats=data_stats,
        data_dict=data_dict,
    )
