import importlib.resources
import json
from pathlib import Path

DATA_DIR = importlib.resources.files('phi4pipeline') / 'metadata'
TEST_DATA_DIR = Path(__file__).parent / 'data'

from phi4pipeline.frictionless import (
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
