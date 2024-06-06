import importlib.resources
import json
from pathlib import Path

import pytest

DATA_DIR = importlib.resources.files('phi4pipeline') / 'metadata'
TEST_DATA_DIR = Path(__file__).parent / 'data'

from phi4pipeline.frictionless import (
    format_datapackage_readme,
    get_file_sha1_hash,
    load_formatted_datapackage,
)


def test_load_formatted_datapackage():
    template_path = DATA_DIR / 'datapackage_template.json'

    expected_path = TEST_DATA_DIR / 'datapackage_expected.json'
    with open(expected_path) as expected_file:
        expected = json.load(expected_file)

    format_args = {
        'version': '4.12',
        'doi': 'https://doi.org/10.5281/zenodo.5356871',
        'phibase_hash': '2f3c683d41d46de6a0a20f56ba29113ab1449936',
        'phibase_bytes': '8998',
        'fasta_hash': '1a65c4809dfa91ea35ae0bd5b3f5c6221e0eab35',
        'fasta_bytes': '5632',
    }

    actual = load_formatted_datapackage(template_path, format_args)
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
        'version': '4.12',
        'semver': '1.0.0',
        'year': '2021',
        'doi': '10.5281/zenodo.5356871',
        'doi_url': 'https://doi.org/10.5281/zenodo.5356871',
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
            TEST_DATA_DIR / 'phi-base_v4-12_test.csv',
            '2f3c683d41d46de6a0a20f56ba29113ab1449936',
            id='csv',
        ),
        pytest.param(
            TEST_DATA_DIR / 'phi-base_v4-12_test.fas',
            '1a65c4809dfa91ea35ae0bd5b3f5c6221e0eab35',
            id='fasta',
        ),
    ],
)
def test_get_file_sha1_hash(path, expected):
    actual = get_file_sha1_hash(path)
    assert actual == expected
