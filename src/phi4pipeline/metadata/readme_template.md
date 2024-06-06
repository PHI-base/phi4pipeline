# The Pathogen-Host Interaction Database, version {version}

[doi:{doi}]({doi_url})

-   **Version:** {version} ({semver})
-   **Published:** {year}
-   **Publisher:** PHI-base

**Cite as:** Rothamsted Research ({year}). Pathogen-Host Interaction
Database, version {version}. PHI-base, Rothamsted Research, Harpenden,
UK {doi_url}

## Description

PHI-base is an online biological database (available at
[phi-base.org](http://www.phi-base.org)) that catalogues experimentally
verified pathogenicity, virulence and effector genes from fungal,
oomycete and bacterial pathogens, which infect animal, plant, fungal and
insect hosts. PHI-base aims to aid discovery of genes in pathogens that
are of medical or agronomic importance, and which may be potential
targets for chemical intervention.

Each entry in PHI-base is curated by domain experts and is supported by
strong experimental evidence, as well as references to the literature in
which the original experiments are described. Each gene has a detailed
description of the predicted protein’s function during the host
infection process. To facilitate data interoperability, we have
annotated genes using controlled vocabularies and links to external
sources (UniProt, Gene Ontology, Enzyme Commission, NCBI Taxonomy, EMBL,
PubMed and FRAC).

This PHI-base dataset is a Frictionless Data Package containing an
export of the PHI-base database in CSV format (comma-separated values).
The current version, {version}, contains the following information:

{data_stats_table}

Amino acid sequences for each gene in PHI-base are included as a 
supplementary FASTA file.

## Data contents

| File                           | Name                          | Description                                                      |
|--------------------------------|-------------------------------|------------------------------------------------------------------|
| phi-base\_{version}\_data.csv  | PHI-base {version} dataset    | An export of data from PHI-base in CSV format.                   |
| phi-base\_{version}\_fasta.fas | PHI-base {version} FASTA file | Amino acid sequences for each gene in PHI-base, where available. |

## Contributors

{contributors_table}

## Conditions of use

-   **Rights holder**: Rothamsted Research
-   **Licence**: This dataset is available under the [Creative Commons
    Attribution 4.0
    International](https://creativecommons.org/licenses/by/4.0/)
    licence.
-   **Cite as**: Rothamsted Research ({year}). Pathogen-Host Interaction
    Database, version {version}. PHI-base, Rothamsted Research,
    Harpenden, UK {doi_url}
-   **Conditions of use**: Rothamsted relies on the integrity of users
    to ensure that Rothamsted Research receives suitable acknowledgment
    as being the originators of these data. This enables us to monitor
    the use of each dataset and to demonstrate their value. Please send
    us a link to any publication that uses this Rothamsted data.

## Funding

PHI-base version {version} was funded by the [Biotechnology and
Biological Sciences Research
Council](http://dx.doi.org/10.13039/501100000268) (BBSRC) through the
Bioinformatics and biological resources: {grant_year} grant.

## Technical information

This data package follows several standards that were created by the
[Frictionless Data](https://frictionlessdata.io/) team:

-   the [Data Package](https://specs.frictionlessdata.io/data-package/)
    standard is used for the metadata of the entire dataset,
-   the [Tabular Data
    Resource](https://specs.frictionlessdata.io/tabular-data-resource/)
    standard describes the PHI-base CSV dataset, and
-   the [Table Schema](https://specs.frictionlessdata.io/table-schema/)
    standard describes the columns of the CSV file.

Data in this dataset can be programmatically accessed using the
[Frictionless Framework](https://framework.frictionlessdata.io/), an
open-source framework written in Python.

## Data dictionary

The following table describes the columns in the PHI-base CSV file
included with this data package. For a complete description with
examples and data validation rules, see the file
**phi-base_schema.json**.

{data_dictionary}
