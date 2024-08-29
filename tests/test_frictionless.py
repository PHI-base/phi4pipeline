import importlib.resources
import json
from pathlib import Path

import pandas as pd
import pytest
from freezegun import freeze_time

from phi4pipeline.frictionless import (
    anonymize_contributors,
    convert_readme_to_html,
    format_datapackage_readme,
    format_zenodo_description,
    get_data_stats,
    get_file_sha1_hash,
    load_formatted_datapackage,
    make_author_list,
    make_datapackage_json,
    make_datapackage_readme,
)
from phi4pipeline.load import load_contributors_file

DATA_DIR = importlib.resources.files('phi4pipeline') / 'metadata'
TEST_DATA_DIR = Path(__file__).parent / 'data'
CSV_PATH = TEST_DATA_DIR / 'phi-base_v4-12_test.csv'
FASTA_PATH = TEST_DATA_DIR / 'phi-base_v4-12_test.fas'
VERSION = '4.12'
DOI = '10.5281/zenodo.5356871'
# Used in the freeze_time decorator
CREATED_DATE = "2021-09-02 11:01:15"


@pytest.fixture
def datapackage_json():
    path = TEST_DATA_DIR / 'datapackage_expected.json'
    with open(path) as file:
        datapackage = json.load(file)
    return datapackage


@pytest.fixture
def phibase_schema():
    path = DATA_DIR / 'phi-base_schema.json'
    with open(path, encoding='utf-8') as file:
        schema = json.load(file)
    return schema


@pytest.fixture
def contributors():
    return load_contributors_file(TEST_DATA_DIR / 'contributors.csv')


@pytest.fixture
def anonymized_contributors(contributors):
    return anonymize_contributors(contributors)


@pytest.fixture
def readme_templated():
    path = TEST_DATA_DIR / 'readme_expected.md'
    with open(path, encoding='utf-8') as file:
        readme_templated = file.read()
    return readme_templated


@freeze_time(CREATED_DATE, tz_offset=1)
def test_load_formatted_datapackage(datapackage_json, anonymized_contributors):
    format_args = {
        'version': VERSION,
        'doi': f'https://doi.org/{DOI}',
        'phibase_hash': '2f3c683d41d46de6a0a20f56ba29113ab1449936',
        'phibase_bytes': '8973',
        'fasta_hash': '1a65c4809dfa91ea35ae0bd5b3f5c6221e0eab35',
        'fasta_bytes': '5632',
    }
    actual = load_formatted_datapackage(format_args, anonymized_contributors)
    expected = datapackage_json
    assert actual == expected


def test_format_datapackage_readme(
    readme_templated,
    phibase_schema,
    anonymized_contributors,
):
    readme_path = DATA_DIR / 'readme_template.md'
    with open(readme_path, encoding='utf-8') as text_file:
        readme_str = text_file.read()

    format_args = {
        'version': VERSION,
        'semver': '4.12.0',
        'year': '2021',
        'doi': DOI,
        'doi_url': f'https://doi.org/{DOI}',
    }
    data_stats = {
        'n_pubs': 15,
        'n_interactions': 13,
        'n_pathogen_genes': 16,
        'n_pathogens': 10,
        'n_hosts': 10,
    }

    actual = format_datapackage_readme(
        readme_str,
        format_args=format_args,
        contributors_data=anonymized_contributors,
        data_stats=data_stats,
        data_dict=phibase_schema,
    )
    expected = readme_templated
    assert actual == expected


@pytest.mark.parametrize(
    'path,expected',
    [
        pytest.param(
            CSV_PATH,
            '2f3c683d41d46de6a0a20f56ba29113ab1449936',
            id='csv',
        ),
        pytest.param(
            FASTA_PATH,
            '1a65c4809dfa91ea35ae0bd5b3f5c6221e0eab35',
            id='fasta',
        ),
    ],
)
def test_get_file_sha1_hash(path, expected):
    actual = get_file_sha1_hash(path)
    assert actual == expected


@freeze_time(CREATED_DATE, tz_offset=1)
def test_make_datapackage_json_str(datapackage_json, anonymized_contributors):
    actual = make_datapackage_json(
        CSV_PATH,
        FASTA_PATH,
        version=VERSION,
        doi=DOI,
        contributors=anonymized_contributors,
    )
    expected = datapackage_json
    assert actual == expected


def test_get_data_stats():
    phi_df = pd.read_csv(TEST_DATA_DIR / 'phi-base_v4-12_cleaned.csv')
    expected = {
        'n_pubs': 15,
        'n_interactions': 13,
        'n_pathogen_genes': 16,
        'n_pathogens': 10,
        'n_hosts': 10,
    }
    actual = get_data_stats(phi_df)
    assert actual == expected


def test_make_datapackage_readme(readme_templated, anonymized_contributors):
    actual = make_datapackage_readme(
        csv_path=TEST_DATA_DIR / 'phi-base_v4-12_cleaned.csv',
        version='4.12',
        semver='4.12.0',
        year=2021,
        doi='10.5281/zenodo.5356871',
        contributors_data=anonymized_contributors,
    )
    expected = readme_templated
    assert actual == expected


def test_anonymize_contributors(contributors):
    expected = [
        {
            'name': 'Josiah S. Carberry',
            'email': 'josiah.carberry@example.org',
            'orcid': '0000-0002-1825-0097',
            'role_readme': 'Principal Investigator',
            'role_frictionless': 'author',
            'affiliation': 'Brown University',
            'is_author': True,
            'is_private': False,
        },
        {
            'name': 'John Smith',
            'email': None,
            'orcid': None,
            'role_readme': 'Curator',
            'role_frictionless': 'contributor',
            'affiliation': 'Acme Corporation',
            'is_author': False,
            'is_private': False,
        },
        {
            'name': 'Anonymous',
            'email': None,
            'orcid': '0000-0002-1825-0097',
            'role_readme': 'Lead curator',
            'role_frictionless': 'contributor',
            'affiliation': '',
            'is_author': False,
            'is_private': None,
        },
    ]
    actual = anonymize_contributors(contributors)
    assert expected == actual


@pytest.mark.parametrize(
    'contributors_data,expected',
    [
        pytest.param(
            [
                {
                    'name': 'Josiah S. Carberry',
                    'is_author': True,
                },
            ],
            'Carberry, J. S.',
            id='one_author',
        ),
        pytest.param(
            [
                {
                    'name': 'Josiah S. Carberry',
                    'is_author': True,
                },
                {
                    'name': 'Morgan Gooseberry',
                    'is_author': True,
                },
            ],
            'Carberry, J. S. & Gooseberry, M.',
            id='two_authors',
        ),
        pytest.param(
            [
                {
                    'name': 'Josiah S. Carberry',
                    'is_author': True,
                },
                {
                    'name': 'Morgan Gooseberry',
                    'is_author': True,
                },
                {
                    'name': 'Jo Blueberry',
                    'is_author': True,
                },
            ],
            'Carberry, J. S., Gooseberry, M. & Blueberry, J.',
            id='three_authors',
        ),
        pytest.param(
            [
                {
                    'name': 'Ronaldo',
                    'is_author': True,
                },
            ],
            'Ronaldo',
            id='no_initials',
        ),
        pytest.param(
            [
                {
                    'name': 'Josiah S. Carberry',
                    'is_author': True,
                },
                {
                    'name': 'Jo Smith',
                    'is_author': False,
                },
            ],
            'Carberry, J. S.',
            id='with_non_author',
        ),
    ],
)
def test_make_author_list(contributors_data, expected):
    actual = make_author_list(contributors_data)
    assert expected == actual


def test_convert_readme_to_html():
    with open(TEST_DATA_DIR / 'readme_expected.md', encoding='utf-8') as f:
        readme_str = f.read()
    with open(TEST_DATA_DIR / 'readme_expected.html', encoding='utf-8') as f:
        expected = f.read()
    actual = convert_readme_to_html(readme_str)
    assert expected == actual


def test_format_zenodo_description():
    data_stats = {
        'n_pubs': 4387,
        'n_interactions': 18190,
        'n_pathogen_genes': 8411,
        'n_pathogens': 279,
        'n_hosts': 228,
    }
    version = '4.12'
    with open(TEST_DATA_DIR / 'description_expected.html', encoding='utf-8') as f:
        expected = f.read()
    actual = format_zenodo_description(version, data_stats)
    assert expected == actual
