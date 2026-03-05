# The Pathogen-Host Interaction Database, version {version}

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
description of the predicted protein's function during the host
infection process. To facilitate data interoperability, we have
annotated genes using controlled vocabularies and links to external
sources (UniProt, Gene Ontology, Enzyme Commission, NCBI Taxonomy, EMBL,
PubMed and FRAC).

This PHI-base dataset is a Frictionless Data Package containing an
export of the PHI-base database in CSV format (comma-separated values).

Amino acid sequences for each gene in PHI-base are included as a 
supplementary FASTA file.

## How to cite

To cite this version of the dataset (version {version}), use the 
following citation:

> {author_list} ({year}). The Pathogen-Host Interactions Database,
> version {version}. PHI-base, Rothamsted Research, Harpenden, UK
> <{doi_url}>

## Conditions of use

-   **Rights holder**: Rothamsted Research

-   **Licence**: Creative Commons Attribution 4.0 International
    (<https://creativecommons.org/licenses/by/4.0/>)

-   **Citation**: {author_list} ({year}). The Pathogen-Host 
    Interactions Database, version {version}. PHI-base, Rothamsted 
    Research, Harpenden, UK <{doi_url}>

Rothamsted Research relies on the integrity of our users to ensure that
we receive suitable acknowledgment as being the originator of this
dataset. This enables us to monitor the use of this dataset and to
demonstrate its value. Please send us a link to any publication that
uses this dataset.

## Data contents

| File                           | Name                          | Description                                                      |
|--------------------------------|-------------------------------|------------------------------------------------------------------|
| phi-base\_{version}\_data.csv  | PHI-base {version} dataset    | An export of data from PHI-base in CSV format.                   |
| phi-base\_{version}\_fasta.fas | PHI-base {version} FASTA file | Amino acid sequences for each gene in PHI-base, where available. |

## Authors

{authors_table}

## Contributors

{contributors_table}

The data content for PHI-base {version} was curated by curators at
[Molecular Connections Pvt Ltd.](https://molecularconnections.com/)
in Bangalore, India.

(Note: for data protection reasons, the names and affiliations of
some contributors may not be included within this dataset.
Information about these contributors can instead be seen on the [Zenodo record page]({doi_url})
for this dataset.)

## Funding

PHI-base version {version} was funded by Rothamsted Research. Rothamsted
Research receives strategic funding from the Biotechnology and
Biological Sciences Research Council (BBSRC) of the United Kingdom. We
acknowledge support from the [Growing
Health](https://repository.rothamsted.ac.uk/project/98ww1/growing-health-isp)
(BB/X010953/1) Institute Strategic Programme and the [Delivering
Sustainable
Wheat](https://repository.rothamsted.ac.uk/project/98ww2/delivering-sustainable-wheat)
(BB/X011003/1) Institute Strategic Programme.

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
[Frictionless Framework](https://framework.frictionlessdata.io/).

## Data dictionary

The following table describes the columns in the PHI-base CSV file
included with this data package. For a complete description with
examples and data validation rules, see the file
**phi-base_schema.json**.

{data_dictionary}
