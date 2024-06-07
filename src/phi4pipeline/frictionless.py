import hashlib
import importlib
import json
import os
import re
from os import PathLike
from string import Template

import pandas as pd

DATA_DIR = importlib.resources.files('phi4pipeline') / 'metadata'


def load_formatted_datapackage(format_args: dict[str, str]) -> dict:
    template_path = DATA_DIR / 'datapackage_template.json'
    with open(template_path, encoding='utf-8') as file:
        template_str = file.read()
    template = Template(template_str)
    datapackage = json.loads(template.substitute(**format_args))
    for resource in datapackage['resources']:
        resource['bytes'] = int(resource['bytes'])
    return datapackage


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
            'role': 'Role',
            'affiliation': 'Affiliation',
        }
        df = pd.DataFrame.from_records(contributors_data)
        # Link ORCID IDs to ORCID page
        df.orcid = df.orcid.str.replace(
            pat=orcid_pattern, repl=r'[\1](https://orcid.org/\1)', regex=True
        )
        table_str = df.rename(columns=renames).to_markdown(
            index=False, tablefmt=TABLE_FORMAT
        )
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

    format_args_tables = {
        'contributors_table': make_contributors_table(contributors_data),
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
    return load_formatted_datapackage(format_args)


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

    data_stats = get_data_stats(pd.read_csv(csv_path))
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
