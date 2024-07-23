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
            'role': 'Principal Investigator',
            'affiliation': 'Brown University',
        },
        {
            'name': 'Jane Smith',
            'orcid': np.nan,
            'role': 'Lead curator',
            'affiliation': 'Acme Corporation',
        },
    ]
    assert expected == actual
