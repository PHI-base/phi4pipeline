import hashlib
import importlib.resources
import json
import os
import re
from os import PathLike
from string import Template
import textwrap

import markdown
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
    datapackage['contributors'] = [
        {
            k: v for k, v in
            {
                'title': contributor['name'],
                'path': (
                    f'https://orcid.org/{contributor["orcid"]}'
                    if contributor['orcid'] else None
                ),
                'role': contributor['role_frictionless'],
                'organization': contributor['affiliation'] or None
            }.items()
            if v is not None
        }
        for contributor in contributors
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


def make_author_list(contributors_data):

    def iter_formatted_names(authors):
        for author in authors:
            name_parts = author['name'].split()
            if len(name_parts) == 1:
                yield name_parts[0]
                continue
            last_name = name_parts[-1]
            initials = ' '.join(f'{x[0].upper()}.' for x in name_parts[:-1])
            author_name = ', '.join((last_name, initials))
            yield author_name

    authors = (a for a in contributors_data if a['is_author'])
    formatted_names = list(iter_formatted_names(authors))
    author_list = (
        formatted_names[0]
        if len(formatted_names) == 1
        else ' & '.join(
            (', '.join(formatted_names[:-1]), formatted_names[-1])
        )
    )
    return author_list


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
        if not contributors_data:
            return ''
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
        'author_list': make_author_list(contributors_data),
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


def convert_readme_to_html(readme_str):
    html = markdown.markdown(readme_str, extensions=['tables'])
    # We aren't using <strong> for emphasis for accessibility purposes,
    # so <b> should be preferred for visual emphasis.
    html = re.sub(r'<(/?)strong>', r'<\1b>', html)
    # Python-Markdown doesn't support CSS, so we must add our own
    head = textwrap.dedent(r"""
        <head>
        <meta charset="utf-8">
        <style>
        body {font-family: sans-serif}
        p, ol, ul {width: 40em}
        table {border-collapse: collapse}
        td, th {border: 1px solid black; padding: 0.2em 0.3em}
        th {font-weight: bold}
        </style>
        </head>
    """).strip()
    # Python-Markdown only exports an HTML fragment, which we need to wrap.
    html = '\n'.join((
        '<html>',
        head,
        '<body>',
        html,
        '</body>',
        '</html>',
        '',  # trailing newline
    ))
    return html
