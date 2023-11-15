# SPDX-FileCopyrightText: 2023-present James Seager <james.seager@rothamsted.ac.uk>
#
# SPDX-License-Identifier: MIT

import re


def validate_phibase(phi_df):
    """Validate values in all columns of PHI-base.

    :param phi_df: the PHI-base DataFrame
    :type phi_df: pandas.DataFrame
    :raises AssertionError: if any value fails validation
    """

    def make_gene_inducer_pattern():
        repeat = lambda pat, sep: f'{pat}(?:{sep} {pat})*'
        chebi = 'CHEBI:\d+'
        cas = 'CAS:\d+-\d+-\d+'
        chem_id = f'(?:{chebi}|{cas}|\d+)'
        chem_ids_L1 = repeat(chem_id, ';')
        chem_ids_L2 = repeat(chem_id, ',')
        chem_name = '.+(?=([;,]|$))'
        chem_names = repeat(chem_name, ',')
        anti_infs = repeat(f'anti-infective: {chem_names}: {chem_ids_L2}', ';')
        labelled_ids = repeat(f'{chem_names}: {chem_ids_L2}', ';')
        pattern = f'(?:{anti_infs}|{labelled_ids}|{chem_ids_L1}|{chem_names})'
        return pattern

    validation_patterns = {
        'record_id': 'Record \d+',
        'phi_id': 'PHI:\d+',
        'protein_id_source': 'UniProt',
        'protein_id': '[0-9A-Z]+(?:-[0-9A-Z]+)?|no data found',
        'gene_id_source': (
            '(EMBL|GenBank|Broad|Ensembl Genomes|MUMDB|ASAP|FCGP|JGI|BROAD|FGDB'
            '|Ecogene|FTFD|Geo|FVG|MIPS|Author)'
        ),
        'gene_id': (
            '(?:AER|ABF)-\d+|\w+-\w+|(Ensembl: )?[\w.]+?'
            '(; (Ensembl: )?[\w.]+?)*|Myc .+|SPA0021 sRNA'
        ),
        'nt_sequence': '[ACGT]+',
        'multiple_mutation': 'PHI:\d+(?:; PHI:\d+)*',
        'pathogen_species': "[A-Z][a-z]+ (?:sp\. '.+?'|[a-z]+(?:-[a-z]+)?)(?: VGIII)?",
        'host_species': (
            '[A-Z][a-z]+(?: (?:[a-z]+|x [a-z]+|[a-z]+ x [A-Z][a-z]+ [a-z]+))? \(.+?\)'
        ),
        'host_genotype_id': (
            '(?:.+ )?(?:UniProt: [0-9A-Z]+|(?:GenBank|Ensembl): \w+)'
            '(?:; (?:.+, )?(?:UniProt: [0-9A-Z]+|(?:GenBank|Ensembl): \w+))*'
        ),
        'go_annotation': (
            'GO:\d{7}(?:, (?:IDA|IEA|IGI|IMP|IPI|ISS|NAS|ND|TAS))?'
            '(?:; GO:\d{7}(?:, (?:IDA|IEA|IGI|IMP|IPI|ISS|NAS|ND|TAS))?)*'
        ),
        'database': 'GO',
        'mating_defect': '(?:yes|no)(?: \(.+?\))?',
        'pre_penetration_defect': '(?:yes|no)(?: \(.+?\))?',
        'penetration_defect': '(?:yes|no)(?: \(.+?\))?',
        'post_penetration_defect': '(?:yes|no|yes/no)(?: \(.+?\))?',
        'essential_gene': '(?:yes|no)',
        'gene_inducer_id': make_gene_inducer_pattern(),
        'host_target_id': (
            '(?:.+ )?(?:UniProt: [0-9A-Z]+|GenBank: \w+|Ensembl: \S+)'
            '(?:; (?:.+, )?(?:UniProt: [0-9A-Z]+|GenBank: \w+|Ensembl: \S+))*'
        ),
        'species_expert': '[A-Z]+(?:; [A-Z]+)*',
        'entered_by': '[A-Z]+(?:; [A-Z]+)*',
        'reference_source': 'PubMed|ISBN|Not in PubMed',
        'doi': '\d+(?:\.\d+)?/.+|no data found',
        'curator_organization': '(?:AC|MC|MU|RRes)(?:; (?:AC|MC|MU|RRes))*',
    }
    validation_patterns = {k: re.compile(v) for k, v in validation_patterns.items()}

    for column_name, pattern in validation_patterns.items():
        column = phi_df[column_name]
        if column.isna().all():
            continue
        is_invalid = ~column.str.fullmatch(pattern, na=True)
        if is_invalid.any():
            index = is_invalid[lambda x: x].index
            invalid_rows = column[index].drop_duplicates()
            invalid_values = '\n'.join(invalid_rows.values)
            error_message = f'column {column_name} has invalid values:\n{invalid_values}'
            assert False, error_message
