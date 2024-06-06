import importlib.resources
import json
from pathlib import Path

import pytest

from phi4pipeline.frictionless import (
    format_datapackage_readme,
    get_file_sha1_hash,
    load_formatted_datapackage,
)

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


def test_load_formatted_datapackage(datapackage_json):
    template_path = DATA_DIR / 'datapackage_template.json'
    format_args = {
        'version': VERSION,
        'doi': f'https://doi.org/{DOI}',
        'phibase_hash': '2f3c683d41d46de6a0a20f56ba29113ab1449936',
        'phibase_bytes': '8998',
        'fasta_hash': '1a65c4809dfa91ea35ae0bd5b3f5c6221e0eab35',
        'fasta_bytes': '5632',
    }
    actual = load_formatted_datapackage(template_path, format_args)
    expected = datapackage_json
    assert actual == expected


def test_format_datapackage_readme():
    readme_path = DATA_DIR / 'readme_template.md'
    with open(readme_path, encoding='utf-8') as text_file:
        readme_str = text_file.read()

    data_dict_path = DATA_DIR / 'phi-base_schema.json'
    with open(data_dict_path, encoding='utf-8') as json_file:
        data_dict = json.load(json_file)

    expected_path = TEST_DATA_DIR / 'readme_expected.md'
    with open(expected_path, encoding='utf-8') as text_file:
        expected = text_file.read()

    format_args = {
        'version': VERSION,
        'semver': '1.0.0',
        'year': '2021',
        'doi': DOI,
        'doi_url': f'https://doi.org/{DOI}',
    }
    contributors_data = [
        {
            'name': 'Josiah Carberry',
            'orcid': '0000-0002-1825-0097',
            'role': 'Principal Investigator',
            'affiliation': 'Brown University',
        },
        {
            'name': 'Jane Smith',
            'orcid': '',
            'role': 'Lead curator',
            'affiliation': 'Acme Corporation',
        },
    ]
    data_stats = {
        'n_pubs': 20,
        'n_interactions': 25,
        'n_pathogen_genes': 4,
        'n_pathogens': 5,
        'n_hosts': 6,
    }

    actual = format_datapackage_readme(
        readme_str,
        format_args=format_args,
        contributors_data=contributors_data,
        data_stats=data_stats,
        data_dict=data_dict,
    )
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
