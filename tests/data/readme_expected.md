# The Pathogen-Host Interaction Database, version 4.12

[doi:10.5281/zenodo.5356871](https://doi.org/10.5281/zenodo.5356871)

-   **Version:** 4.12 (1.0.0)
-   **Published:** 2021
-   **Publisher:** PHI-base

**Cite as:** Rothamsted Research (2021). Pathogen-Host Interaction
Database, version 4.12. PHI-base, Rothamsted Research, Harpenden,
UK https://doi.org/10.5281/zenodo.5356871

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
The current version, 4.12, contains the following information:

| Data Type                  |   Count |
|----------------------------|---------|
| Publications               |      20 |
| Pathogen-host interactions |      25 |
| Pathogen genes             |       4 |
| Pathogen species           |       5 |
| Host species               |       6 |

Amino acid sequences for each gene in PHI-base are included as a 
supplementary FASTA file.

## Data contents

| File                           | Name                          | Description                                                      |
|--------------------------------|-------------------------------|------------------------------------------------------------------|
| phi-base\_4.12\_data.csv  | PHI-base 4.12 dataset    | An export of data from PHI-base in CSV format.                   |
| phi-base\_4.12\_fasta.fas | PHI-base 4.12 FASTA file | Amino acid sequences for each gene in PHI-base, where available. |

## Contributors

| Name            | ORCID ID                                                     | Role                   | Affiliation      |
|-----------------|--------------------------------------------------------------|------------------------|------------------|
| Josiah Carberry | [0000-0002-1825-0097](https://orcid.org/0000-0002-1825-0097) | Principal Investigator | Brown University |
| Jane Smith      |                                                              | Lead curator           | Acme Corporation |

## Conditions of use

-   **Rights holder**: Rothamsted Research
-   **Licence**: This dataset is available under the [Creative Commons
    Attribution 4.0
    International](https://creativecommons.org/licenses/by/4.0/)
    licence.
-   **Cite as**: Rothamsted Research (2021). Pathogen-Host Interaction
    Database, version 4.12. PHI-base, Rothamsted Research,
    Harpenden, UK https://doi.org/10.5281/zenodo.5356871
-   **Conditions of use**: Rothamsted relies on the integrity of users
    to ensure that Rothamsted Research receives suitable acknowledgment
    as being the originators of these data. This enables us to monitor
    the use of each dataset and to demonstrate their value. Please send
    us a link to any publication that uses this Rothamsted data.

## Funding

PHI-base version 4.12 was funded by the [Biotechnology and
Biological Sciences Research
Council](http://dx.doi.org/10.13039/501100000268) (BBSRC) through the
BBR award "A FAIR community resource for pathogens, hosts and their 
interactions to enhance global food security and human health"
\[BB/S020020/1\].

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

| Column                    | Name                               | Type    | Description                                                                                                                                                                                                                                                  |
|---------------------------|------------------------------------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| record_id                 | Record ID                          | string  | The unique identifier for a record (row) in the PHI-base database.                                                                                                                                                                                           |
| phi_id                    | PHI ID                             | string  | An identifier corresponding to one gene of one pathogen from one publication.                                                                                                                                                                                |
| protein_id_source         | Protein ID source                  | string  | The source database for the protein identifier.                                                                                                                                                                                                              |
| protein_id                | Protein ID                         | string  | The unique identifier for the protein expressed by the pathogen gene. The identifier references a protein database (such as UniProtKB).                                                                                                                      |
| gene_id_source            | Gene ID source                     | string  | The source database for the pathogen gene identifier.                                                                                                                                                                                                        |
| gene_id                   | Gene ID                            | string  | The unique identifier for the pathogen gene, which references a genetic database (such as GenBank).                                                                                                                                                          |
| sequence_strain           | Sequence strain                    | string  | The strain, isolate, subspecies, etc. of the pathogen for the gene sequence or protein sequence.                                                                                                                                                             |
| gene                      | Gene                               | string  | The gene name for the pathogen gene.                                                                                                                                                                                                                         |
| chromosome_location       | Chromosome location                | string  | The chromosome where the pathogen gene is located.                                                                                                                                                                                                           |
| gene_protein_modification | Gene protein modification          | string  | Specific modifications to the targeted pathogen protein or promoter, such as amino acid modification, promoter sequence modification, or domain swaps.                                                                                                       |
| modified_gene_protein_id  | Modified gene protein ID           | string  | The unique identifier for the modified pathogen gene.                                                                                                                                                                                                        |
| interacting_partners      | Interacting partners               | string  | Proteins or DNA elements within the pathogen that interact with the pathogen gene. Multiple values are delimited with a semicolon.                                                                                                                           |
| interacting_partners_id   | Interacting partners ID            | string  | The unique identifiers for the proteins or DNA elements within the pathogen that interact with the pathogen gene. Each identifier is prefixed with with the name of its source database. Multiple values are delimited with a semicolon.                     |
| multiple_mutation         | Multiple mutation                  | string  | One or more PHI IDs for pathogen genes that are disrupted as part of a mutation. Multiple values are delimited with a semicolon.                                                                                                                             |
| pathogen_id               | Pathogen ID                        | integer | The NCBI Taxonomy identifier for the pathogen.                                                                                                                                                                                                               |
| pathogen_species          | Pathogen species                   | string  | The scientific name of the pathogen.                                                                                                                                                                                                                         |
| pathogen_strain_id        | Pathogen strain ID                 | integer | The NCBI Taxonomy identifier at the strain level for the strain of the pathogen.                                                                                                                                                                             |
| pathogen_strain           | Pathogen strain                    | string  | The names of the strain, isolate, subspecies, pathovars, serotypes etc. of the pathogen. Multiple values are delimited with a semicolon.                                                                                                                     |
| disease                   | Disease                            | string  | The names of any diseases known to be caused by the pathogen. Multiple values are delimited with a semicolon.                                                                                                                                                |
| host_description          | Host description                   | string  | High-level taxonomic classification for the host species, such as an order or clade.                                                                                                                                                                         |
| host_id                   | Host ID                            | integer | The NCBI Taxonomy identifier for the host organism.                                                                                                                                                                                                          |
| host_species              | Host species                       | string  | The scientific name of the host organism. The common name of the species (if any) is included in parentheses after the scientific name.                                                                                                                      |
| host_strain               | Host strain                        | string  | The name of the strain, cell line, genotype, cultivar, ecotype etc. of the host species. Multiple values are delimited with a semicolon.                                                                                                                     |
| host_genotype             | Host genotype                      | string  | Any host genes of interest which are not necessarily tested, but referred to in the publication with regard to the pathogen gene of interest. Multiple values are delimited with a semicolon.                                                                |
| host_genotype_id          | Host genotype ID                   | string  | The unique identifiers for the host genes referred to in the publication. Each identifier is prefixed with with the name of its source database. Multiple values are delimited with a semicolon.                                                             |
| tissue                    | Tissue                             | string  | The host tissue where the experiment was initiated. The resulting diseased tissue may be provided in parentheses. Most tissue names follow the naming conventions of the BRENDA Tissue Ontology (BTO). Multiple values are delimited with a semicolon.       |
| gene_function             | Gene function                      | string  | The biological function of the disrupted pathogen gene.                                                                                                                                                                                                      |
| go_annotation             | Gene Ontology annotation           | string  | List of all appropriate Gene Ontology (GO) terms or Enzyme Commission (EC) numbers for the pathogen gene of interest. GO terms may be followed by a GO evidence code (e.g. IMP). Multiple values are delimited with a semicolon.                             |
| database                  | Database                           | string  | The name of the source database for records in the 'GO annotation' column.                                                                                                                                                                                   |
| pathway                   | Pathway                            | string  | The name of the pathway that the disrupted pathogen gene is involved in.                                                                                                                                                                                     |
| mutant_phenotype          | Mutant phenotype                   | string  | Broadly describes a phenotype that results from a pathogen-host interaction, or the response of a pathogen to some chemical.                                                                                                                                 |
| mating_defect             | Mating defect                      | string  | Whether the experimental pathogen has a mating defect prior to penetrating the host (yes or no). Additional information may be included in parentheses.                                                                                                      |
| pre_penetration_defect    | Pre-penetration defect             | string  | Whether the experimental pathogen has a pre-penetration defect (yes or no). Additional information may be included in parentheses.                                                                                                                           |
| penetration_defect        | Penetration defect                 | string  | Whether the experimental pathogen has a penetration defect (yes or no). Additional information may be included in parentheses.                                                                                                                               |
| post_penetration_defect   | Post-penetration defect            | string  | Whether the experimental pathogen has a post-penetration defect (yes or no). Additional information may be included in parentheses.                                                                                                                          |
| disease_manifestation     | Disease manifestation              | string  | Description of how disease develops during the pathogen-host interaction (at a macroscopic scale).                                                                                                                                                           |
| vegetative_spores         | Vegetative spores                  | string  | Description of the experimental pathogen's vegetative spores.                                                                                                                                                                                                |
| sexual_spores             | Sexual spores                      | string  | Description of the experimental pathogen's sexual spores.                                                                                                                                                                                                    |
| in_vitro_growth           | In vitro growth                    | string  | Description of how the experimental pathogen grows in vitro.                                                                                                                                                                                                 |
| spore_germination         | Spore germination                  | string  | Description of the experimental pathogen's spore germination process.                                                                                                                                                                                        |
| essential_gene            | Essential gene                     | string  | Whether a knockout of the pathogen gene is lethal to the pathogen; that is, whether the gene is essential for the in vitro or in vivo growth of the pathogen (yes or no).                                                                                    |
| gene_inducer              | Gene inducer                       | string  | Chemical substance that can alter metabolic reactions within a cell, tissue, or intact host organism. Multiple values are delimited with a semicolon.                                                                                                        |
| gene_inducer_id           | Gene inducer ID                    | string  | Accession numbers for the inducer chemicals, sourced from ChEBI or the CAS Registry. Accession numbers for each chemical are separated by a semicolon. Where there are multiple accessions for one chemical, the accession numbers are separated by a comma. |
| host_target               | Host target                        | string  | The first-host-target proteins which interact with the corresponding pathogen protein. May include the host cellular location where the experiment was observed. Multiple values are delimited with a semicolon.                                             |
| host_target_id            | Host target ID                     | string  | Accession numbers for the host target genes of interest. Each accession number is prefixed with with the name of its source database. Multiple values are delimited with a semicolon.                                                                        |
| interaction_phenotype     | Interaction phenotype              | string  | Description of the interaction phenotype between the pathogen and the host organism.                                                                                                                                                                         |
| host_response             | Host response                      | string  | The response observed in the host organism when it interacts with the altered pathogen gene (or protein) of interest.                                                                                                                                        |
| exp_technique_stable      | Experimental technique (stable)    | string  | Description of the experimental procedure.                                                                                                                                                                                                                   |
| exp_technique_transient   | Experimental technique (transient) | string  | Describes the experimental evidence for a transient assay. Used when the experimental technique is 'functional test in host: transient expression' or 'other evidence'.                                                                                      |
| pmid                      | PubMed ID                          | integer | The PubMed identifier (PMID) for the referenced publication, without the 'PMID:' prefix.                                                                                                                                                                     |
| reference_source          | Reference source                   | string  | The name of the library or information resource that contains the referenced publication.                                                                                                                                                                    |
| doi                       | DOI                                | string  | The Digital Object Identifier for the referenced publication.                                                                                                                                                                                                |
| reference_detail          | Reference detail                   | string  | The full citation of the referened publication. May be used as a substitute for a missing PubMed ID or DOI.                                                                                                                                                  |
| comments                  | Comments                           | string  | Additional information, e.g. information found only in the abstract of the referenced publication, or information that is not compatible with any other column in the PHI-base database.                                                                     |
| author_reference          | Author reference                   | string  | An abbreviated citation for the referenced publication.                                                                                                                                                                                                      |
| year                      | Year                               | year    | The year of publication of the referenced publication.                                                                                                                                                                                                       |
| curation_date             | Curation date                      | date    | The date when the referenced publication was curated.                                                                                                                                                                                                        |
