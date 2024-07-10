# SPDX-FileCopyrightText: 2023-present James Seager <james.seager@rothamsted.ac.uk>
#
# SPDX-License-Identifier: MIT

"""Command line interface for the phi4pipeline package."""

import argparse

from phi4pipeline.release import (
    prepare_spreadsheet_for_excel,
    prepare_spreadsheet_for_zenodo,
)


def parse_args(args):
    input_args = {
        'metavar': 'SPREADSHEET',
        'type': str,
        'help': 'the path to the PHI-base 4 spreadsheet',
    }

    parser = argparse.ArgumentParser(
        prog='phi4pipeline',
        description='Apply cleaning to the PHI-base 4 spreadsheet.',
    )
    subparsers = parser.add_subparsers(
        dest='target',
        required=True,
    )

    parser_excel = subparsers.add_parser('excel')
    parser_excel.add_argument('input', **input_args)
    parser_excel.add_argument(
        '-o',
        '--output',
        metavar='FILE',
        required=True,
        type=str,
        help='the output directory for the datapackage files',
    )

    parser_zenodo = subparsers.add_parser('zenodo')
    parser_zenodo.add_argument('input', **input_args)
    parser_zenodo.add_argument(
        '--contributors',
        metavar='PATH',
        type=str,
        help='path to contributors file',
    )
    parser_zenodo.add_argument(
        '--doi',
        metavar='YEAR',
        type=str,
        required=True,
        help='DOI for the dataset',
    )
    parser_zenodo.add_argument(
        '--fasta',
        metavar='PATH',
        type=str,
        help='path to FASTA file for the dataset',
    )
    parser_zenodo.add_argument(
        '-o',
        '--out_dir',
        metavar='DIR',
        required=True,
        type=str,
        help='the output path for the cleaned PHI-base 4 spreadsheet',
    )
    parser_zenodo.add_argument(
        '--year',
        metavar='YEAR',
        type=int,
        help='year of dataset publication',
    )
    return parser.parse_args(args)


def run(args):
    args = parse_args(args)
    if args.target == 'excel':
        phi_df = prepare_spreadsheet_for_excel(args.input)
        phi_df.to_excel(args.output, index=False)
    elif args.target == 'zenodo':
        phi_df = prepare_spreadsheet_for_zenodo(args.input)
        phi_df.to_csv(args.output, index=False, line_terminator='\r\n')
    else:
        # argparse should prevent this from being reached
        raise ValueError(f'unsupported target type: {args.target}')
