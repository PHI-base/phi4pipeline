# SPDX-FileCopyrightText: 2023-present James Seager <james.seager@rothamsted.ac.uk>
#
# SPDX-License-Identifier: MIT

import json
import shutil
from pathlib import Path

import pandas as pd

from phi4pipeline.clean import clean_phibase
from phi4pipeline.frictionless import (
    make_datapackage_json,
    make_datapackage_readme,
)
from phi4pipeline.load import (
    get_column_header_mapping,
    get_version_from_filename,
    load_contributors_file,
    load_excel,
)
from phi4pipeline.validate import validate_phibase


def restore_header_rows(column_header_mapping, phi_df):
    """Restore the original column headers of the PHI-base DataFrame.

    :param column_header_mapping: a mapping between the original first and
    second header rows of the PHI-base DataFrame
    :type column_header_mapping: dict
    :param phi_df: the PHI-base DataFrame
    :type phi_df: pandas.DataFrame
    :return: the PHI-base DataFrame with headers restored
    :rtype: pandas.DataFrame
    """
    columns = [column_header_mapping[col] for col in phi_df.columns]
    phi_df.columns = pd.MultiIndex.from_tuples(columns)
    return phi_df


def load_phibase_spreadsheet(spreadsheet_path, keep_headers=True):
    phi_df = load_excel(spreadsheet_path)
    column_mapping = get_column_header_mapping(phi_df)
    phi_df = clean_phibase(phi_df)
    validate_phibase(phi_df)
    if keep_headers:
        phi_df = restore_header_rows(column_mapping, phi_df)
    return phi_df


def prepare_spreadsheet_for_zenodo(spreadsheet_path):
    """Prepare the PHI-base DataFrame for export as a CSV file.

    :param phi_df: the PHI-base DataFrame
    :type phi_df: pandas.DataFrame
    :return: the PHI-base DataFrame
    :rtype: pandas.DataFrame
    """
    phi_df = load_phibase_spreadsheet(spreadsheet_path, keep_headers=False)
    # These columns contain personal information that should not be shared.
    exclude_columns = ['author_email', 'species_expert', 'entered_by']
    return phi_df.drop(exclude_columns, axis=1, errors='ignore')


def make_files_for_zenodo(
    spreadsheet_path,
    out_dir,
    *,
    doi,
    year,
    fasta_path=None,
    contributors_path=None,
):
    out_dir = Path(out_dir)
    phibase_version = get_version_from_filename(spreadsheet_path)
    csv_filename = f'phi-base_{phibase_version}_data.csv'
    csv_path = out_dir / csv_filename
    fasta_filename = f'phi-base_{phibase_version}_fasta.fas'
    fasta_out_path = out_dir / fasta_filename
    contributors = load_contributors_file(contributors_path)

    phi_df = prepare_spreadsheet_for_zenodo(spreadsheet_path)
    # Write files now so we can calculate file hash and size.
    phi_df.to_csv(csv_path, index=False, lineterminator='\r\n')
    shutil.copyfile(fasta_path, fasta_out_path)

    datapackage_json = make_datapackage_json(
        csv_path,
        fasta_out_path,
        version=phibase_version,
        doi=doi,
        contributors=contributors,
    )
    with open(out_dir / 'datapackage.json', encoding='utf-8') as f:
        json.dump(datapackage_json, f, indent=4)

    readme_text = make_datapackage_readme(
        csv_path,
        version=phibase_version,
        semver=f'{phibase_version}.0',
        year=year,
        doi=doi,
        contributors_data=contributors,
    )
    with open(out_dir / 'README.md', encoding='utf-8') as f:
        f.write(readme_text)


def prepare_spreadsheet_for_excel(spreadsheet_path):
    """Prepare the PHI-base DataFrame for export to an Excel file.

    Convert pandas timestamps to date strings (without times), and remove
    the MultiIndex column headings by moving the second header row to the
    first row of the table. Changing the headers is the only way to avoid
    writing an index column.

    :param phi_df: the PHI-base DataFrame
    :type phi_df: pandas.DataFrame
    :return: the PHI-base DataFrame
    :rtype: pandas.DataFrame
    """
    phi_df = load_phibase_spreadsheet(spreadsheet_path)

    # Preserve existing behavior of truncating interacting partner IDs
    interacting_ids = ('Interacting protein - locus ID', 'InteractingpartnersId')
    if phi_df[interacting_ids].notna().any():
        phi_df[interacting_ids] = phi_df[interacting_ids].str.slice(stop=92)

    # pandas.Series.dt.date is needed to remove timestamps from dates
    date_column = ('Curation date', 'Curationdate')
    phi_df[date_column] = phi_df[date_column].dt.date

    first_header = phi_df.columns.get_level_values(0)
    second_header = phi_df.columns.get_level_values(1)
    first_row = pd.DataFrame(
        data=[list(second_header)],
        index=[0],
        columns=[first_header, second_header],
    )
    # Shift the index so we can insert the first row at index 0
    phi_df.index = phi_df.index + 1
    phi_df = pd.concat([first_row, phi_df])
    # Remove the second header row since it's now the first row of the table
    phi_df.columns = first_header

    return phi_df
