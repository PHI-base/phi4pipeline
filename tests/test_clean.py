# SPDX-FileCopyrightText: 2023-present James Seager <james.seager@rothamsted.ac.uk>
#
# SPDX-License-Identifier: MIT

import pandas as pd

from phi4pipeline.clean import (
    format_tissue_names,
)


def test_format_tissue_names():
    tissues = pd.Series(['Adult', 'Foo', 'Blood'])
    expected = pd.Series(['adult', 'Foo', 'blood'])
    actual = format_tissue_names(tissues)
    assert actual.to_dict() == expected.to_dict()
