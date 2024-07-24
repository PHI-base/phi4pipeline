from pathlib import Path

import numpy as np
import pandas as pd

from phi4pipeline.load import (
    load_contributors_file,
)


TEST_DATA_DIR = Path(__file__).parent / 'data'


def test_load_contributors_file():
    actual = load_contributors_file(TEST_DATA_DIR / 'contributors.csv')
    expected = [
        {
            'name': 'Josiah S. Carberry',
            'orcid': '0000-0002-1825-0097',
            'role_readme': 'Principal Investigator',
            'role_frictionless': 'author',
            'affiliation': 'Brown University',
            'is_author': True,
            'is_private': False,
        },
        {
            'name': 'John Smith',
            'orcid': np.nan,
            'role_readme': 'Curator',
            'role_frictionless': 'contributor',
            'affiliation': 'Acme Corporation',
            'is_author': False,
            'is_private': False,
        },
        {
            'name': 'Jane Smith',
            'orcid': '0000-0002-1825-0097',
            'role_readme': 'Lead curator',
            'role_frictionless': 'contributor',
            'affiliation': 'Acme Corporation',
            'is_author': False,
            'is_private': True,
        },
        {
            'name': 'John Doe',
            'orcid': np.nan,
            'role_readme': 'Curator',
            'role_frictionless': 'contributor',
            'affiliation': 'Acme Corporation',
            'is_author': False,
            'is_private': True,
        },
    ]
    assert expected == actual
