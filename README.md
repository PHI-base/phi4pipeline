# PHI-base 4 pipeline

Python package and command-line application for releasing the PHI-base 4 dataset in Excel and CSV formats, and preparing metadata and files for the Zenodo repository.

## Installation

Install the latest release from GitHub:

```
python -m pip install 'phi4pipeline@git+https://github.com/PHI-base/phi4pipeline.git@1.0.0'
```

Or install the latest commit on the `main` branch:

```
python -m pip install 'phi4pipeline@git+https://github.com/PHI-base/phi4pipeline.git@main'
```

## Usage

### Excel release format

To generate a cleaned and validated version of the spreadsheet that contains the PHI-base 4 dataset, use the following command:

```
python -m phi4pipeline excel -o FILE SPREADSHEET
```

Explanation of arguments:

* `-o`, `--output`: the output path for the processed spreadsheet file.

* `SPREADSHEET`: the path to the spreadsheet containing the PHI-base 4 dataset.

### Zenodo release format

To generate release files to be uploaded to Zenodo, use the following command:

```
python -m phi4pipeline zenodo
--contributors PATH
--doi YEAR
--fasta PATH
-o DIR
--year YEAR
SPREADSHEET
```

Explanation of arguments:

* `--contributors`: the path to the CSV file that contains information about the authors and contributors of the dataset. See the 'Contributors file' section below for more information.

* `--doi`: the DOI name for the dataset in prefix/suffix form (for example: 10.5281/zenodo.5356870). The DOI name _must not_ be prefixed with 'doi:' or 'https://doi.org/'. The DOI is usually generated when preparing a release on Zenodo.

* `--fasta`: the path to the FASTA file that accompanies the PHI-base dataset.

* `-o`, `--out_dir`: the output directory for the release files that will be uploaded to Zenodo.

* `--year`: the year of publication of the dataset. This is the first date of publication anywhere online (for example, year of publication on the PHI-base website), not necessarily the year of publication on Zenodo.

* `SPREADSHEET`: the path to the spreadsheet containing the PHI-base 4 dataset.

## Contributors file

The Contributors file is a CSV file that contains information about the people (authors and contributors) related to the dataset. It contains the following columns, in the following order:

* **name**: the full name of the person.

* **orcid**: the Open Researcher and Contributor ID (ORCID) for the person, without any URL prefix. For example: 0000-0002-1825-0097

* **email**: the email address for the person.

* **role_readme**: the role of the person, as shown in the README file included with the dataset.

* **role_frictionless**: the role of the author or contributor, as shown in the Frictionless Data Package metadata file (datapackage.json) included with the dataset. The recommended role values can be found in the [Data Package specification](https://specs.frictionlessdata.io/data-package/#contributors).

* **affiliation**: the organization that the author or contributor is affiliated with.

* **is_author**: TRUE if the person is an author; FALSE if the person is a contributor. Controls which table the person's details appear in the README file.

* **is_private**: TRUE if the person's personal details should be hidden from the README and datapackage.json files; otherwise FALSE. Defaults to FALSE. This is included to comply with data protection requirements.

## License

`phi4pipeline` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
