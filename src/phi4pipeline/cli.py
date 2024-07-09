# SPDX-FileCopyrightText: 2023-present James Seager <james.seager@rothamsted.ac.uk>
#
# SPDX-License-Identifier: MIT

"""Command line interface for the phi4pipeline package."""

import argparse

from phi4pipeline.clean import clean_phibase
from phi4pipeline.load import get_column_header_mapping, load_excel
from phi4pipeline.release import prepare_for_excel, prepare_for_zenodo
from phi4pipeline.validate import validate_phibase


def parse_args(args):
    parser = argparse.ArgumentParser(
        prog='phi4pipeline',
        description='Apply cleaning to the PHI-base 4 spreadsheet.',
    )
    parser.add_argument(
        'input',
        metavar='SPREADSHEET',
        type=str,
        help='the path to the PHI-base 4 spreadsheet',
    )
    parser.add_argument(
        '-s',
        '--sheet',
        metavar='SHEET',
        required=True,
        type=str,
        help='the name of the sheet in the spreadsheet to clean',
    )
    parser.add_argument(
        '-o',
        '--output',
        metavar='FILE',
        required=True,
        type=str,
        help='the output path for the cleaned PHI-base 4 spreadsheet',
    )
    parser.add_argument(
        '-t',
        '--target',
        metavar='TARGET',
        type=str,
        default='excel',
        choices=['excel', 'zenodo'],
        help='the release target for the processed spreadsheet (excel or zenodo)',
    )
    return parser.parse_args(args)


def run(args):
    args = parse_args(args)
    phi_df = load_excel(args.input)
    column_mapping = get_column_header_mapping(phi_df)
    phi_df = clean_phibase(phi_df)
    validate_phibase(phi_df)

    if args.target == 'excel':
        phi_df = prepare_for_excel(phi_df, column_mapping)
        phi_df.to_excel(args.output, index=False)
    elif args.target == 'zenodo':
        phi_df = prepare_for_zenodo(phi_df)
        phi_df.to_csv(args.output, index=False, line_terminator='\r\n')
    else:
        # This should never be reached due to the choices parameter of argparse
        raise ValueError(f'unsupported target type: {args.target}')
