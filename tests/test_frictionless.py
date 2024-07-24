import importlib.resources
import json
from pathlib import Path

import pandas as pd
import pytest

from phi4pipeline.frictionless import (
    format_datapackage_readme,
    get_data_stats,
    get_file_sha1_hash,
    load_formatted_datapackage,
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
def readme_templated():
    path = TEST_DATA_DIR / 'readme_expected.md'
    with open(path, encoding='utf-8') as file:
        readme_templated = file.read()
    return readme_templated


def test_load_formatted_datapackage(datapackage_json, contributors):
    format_args = {
        'version': VERSION,
        'doi': f'https://doi.org/{DOI}',
        'phibase_hash': '2f3c683d41d46de6a0a20f56ba29113ab1449936',
        'phibase_bytes': '8973',
        'fasta_hash': '1a65c4809dfa91ea35ae0bd5b3f5c6221e0eab35',
        'fasta_bytes': '5632',
    }
    actual = load_formatted_datapackage(format_args, contributors)
    expected = datapackage_json
    assert actual == expected


def test_format_datapackage_readme(readme_templated, phibase_schema, contributors):
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
        contributors_data=contributors,
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


def test_make_datapackage_json_str(datapackage_json, contributors):
    actual = make_datapackage_json(
        CSV_PATH,
        FASTA_PATH,
        version=VERSION,
        doi=DOI,
        contributors=contributors,
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


def test_make_datapackage_readme(readme_templated, contributors):
    actual = make_datapackage_readme(
        csv_path=TEST_DATA_DIR / 'phi-base_v4-12_cleaned.csv',
        version='4.12',
        semver='4.12.0',
        year=2021,
        doi='10.5281/zenodo.5356871',
        contributors_data=contributors,
    )
    expected = readme_templated
    assert actual == expected
