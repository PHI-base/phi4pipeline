# SPDX-FileCopyrightText: 2023-present James Seager <james.seager@rothamsted.ac.uk>
#
# SPDX-License-Identifier: MIT

import pytest

from phi4pipeline.cli import parse_args


test_parse_args_params = [
    pytest.param(
        [
            'zenodo',
            '--contributors',
            'contrib_path.csv',
            '--doi',
            '10.5281/zenodo.5356871',
            '--fasta',
            'fasta_path.fas',
            '-o',
            'out_dir/',
            '--year',
            '2021',
            'spreadsheet_path.xlsx',
        ],
        {
            'target': 'zenodo',
            'contributors': 'contrib_path.csv',
            'doi': '10.5281/zenodo.5356871',
            'fasta': 'fasta_path.fas',
            'input': 'spreadsheet_path.xlsx',
            'out_dir': 'out_dir/',
            'year': 2021,
        },
        id='zenodo_all_options',
    ),
    pytest.param(
        [
            'excel',
            '-o',
            'out_path.xlsx',
            'spreadsheet_path.xlsx',
        ],
        {
            'target': 'excel',
            'input': 'spreadsheet_path.xlsx',
            'output': 'out_path.xlsx',
        },
        id='excel',
    ),
]


@pytest.mark.parametrize('args,expected', test_parse_args_params)
def test_parse_args(args, expected):
    actual = parse_args(args)
    assert expected == vars(actual)
