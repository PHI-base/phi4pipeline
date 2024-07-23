# SPDX-FileCopyrightText: 2023-present James Seager <james.seager@rothamsted.ac.uk>
#
# SPDX-License-Identifier: MIT

import pandas as pd
from pandas.testing import assert_series_equal

from phi4pipeline.clean import (
    format_tissue_names,
    get_converted_curation_dates,
)


def test_format_tissue_names():
    tissues = pd.Series(['Adult', 'Foo', 'Blood'])
    expected = pd.Series(['adult', 'Foo', 'blood'])
    actual = format_tissue_names(tissues)
    assert actual.to_dict() == expected.to_dict()


def test_get_converted_curation_dates():
    expected = pd.Series(
        [
            '2005-05-04',
            '2013-10-01',
            '2016-11-01',
            '2017-02-20',
            '2017-06-01',
            '2019-05-01',
        ],
        dtype='datetime64[ns]'
    )
    dates = pd.Series(
        [
            '04/05/2005',
            '2013-10-01',
            'Nov-16',
            '20-Feb-17',
            '17-Jun',
            'May 2019',
        ],
        dtype='object',
    )
    actual = get_converted_curation_dates(dates)
    assert_series_equal(expected, actual)
