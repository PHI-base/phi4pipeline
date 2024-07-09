# SPDX-FileCopyrightText: 2023-present James Seager <james.seager@rothamsted.ac.uk>
#
# SPDX-License-Identifier: MIT

import pytest

from phi4pipeline.cli import parse_args


@pytest.mark.parametrize(
    'args,expected',
    [
        (
            ['sheet_path', '-s', 'sheet1', '-o', 'out_path'],
            {
                'input': 'sheet_path',
                'output': 'out_path',
                'sheet': 'sheet1',
                'target': 'excel',
            },
        ),
        (
            ['sheet_path', '-s', 'sheet1', '-o', 'out_path', '-t', 'zenodo'],
            {
                'input': 'sheet_path',
                'output': 'out_path',
                'sheet': 'sheet1',
                'target': 'zenodo',
            },
        ),
    ],
)
def test_parse_args(args, expected):
    actual = parse_args(args)
    assert expected == vars(actual)
