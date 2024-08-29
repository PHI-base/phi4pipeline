# SPDX-FileCopyrightText: 2023-present James Seager <james.seager@rothamsted.ac.uk>
#
# SPDX-License-Identifier: MIT

from datetime import datetime
import re

import numpy as np
import pandas as pd

from phi4pipeline.load import normalize_column_names


def remove_excluded_columns(phi_df):
    """Remove columns that should not be parsed into the PHI-base database.

    :param phi_df: the PHI-base DataFrame
    :type phi_df: pandas.DataFrame
    :return: the PHI-base DataFrame
    :rtype: pandas.DataFrame
    """
    excluded_columns_multi = [
        ('__FG_mycotoxin__', 'FGmycotoxin'),
        ('Anti-infective (Chemical)', 'AntiinfectiveagentId'),
        ('Compound', 'Antiinfectiveagent'),
        ('Target site', 'Antiinfectivecompound'),
        ('Group name', 'Antiinfectivetargetsite'),
        ('Chemical group', 'Antiinfectivegroupname'),
        ('Mode in planta', 'AntiinfectiveChemicalgroup'),
        ('Mode of action', 'AntiinfectiveModeinplanta'),
        ('FRAC CODE', 'FRACCODE'),
        ('Additional comments  on anti-infectives', 'Antiinfectivecomments'),
    ]
    second_header = (
        phi_df.columns.get_level_values(1).str.strip()
        if phi_df.columns.nlevels == 2
        else phi_df.columns
    )
    has_exclude_suffix = second_header.str.endswith('.Exclude')
    is_not_parsed = second_header == 'notParsed'
    in_excluded = (
        phi_df.columns.isin(excluded_columns_multi)
        if phi_df.columns.nlevels == 2
        else phi_df.columns.isin(c[1] for c in excluded_columns_multi)
    )
    exclude_index = has_exclude_suffix | is_not_parsed | in_excluded
    included_columns = phi_df.columns[~exclude_index]
    return phi_df[included_columns]


def fix_whitespace(phi_df):
    """Remove extra whitespace and replace all whitespace with spaces.

    :param phi_df: the PHI-base DataFrame
    :type phi_df: pandas.DataFrame
    :return: the PHI-base DataFrame
    :rtype: pandas.DataFrame
    """
    whitespace = re.compile(r'\s+')
    object_columns = phi_df.select_dtypes('object')
    for col in object_columns:
        na_count = phi_df[col].isna().sum()
        replaced = phi_df[col].str.replace(whitespace, ' ', regex=True).str.strip()
        phi_df[col] = phi_df[col].mask(replaced.notna(), replaced)
        assert na_count == phi_df[col].isna().sum()
    return phi_df


def get_formatted_disease_names(diseases):
    """Fix letter casing on all disease names.

    :param phi_df: the disease column from PHI-base
    :type phi_df: pandas.Series
    :return: the disease column with letter casing applied
    :rtype: pandas.Series
    """
    words_to_capitalize = [
        'a',
        'african',
        'alternaria',
        'american',
        'arabidopsis',
        'ascochyta',
        'b',
        'chagas',
        'citrus',
        'crohn',
        'cruciferae',
        'cucurbitaceae',
        'curvularia',
        'dothistroma',
        'far east',
        'fusarium',
        'glasser',
        'haemophilus',
        'legionnaires',
        'lyme',
        'phoma',
        'phytophthora',
        'pierce',
        'q',
        'septoria',
        'stagonospora',
        'stewart',
        'traveler',
        'valsa',
        'verticillium',
        'witches',
    ]
    pattern = re.compile(fr"\b({'|'.join(words_to_capitalize)})\b")
    replacements = {word: word.title() for word in words_to_capitalize}
    replace = lambda match: replacements[match.group(0)]
    return diseases.str.lower().str.replace(pattern, replace, regex=True)


def format_tissue_names(tissues):
    """Lowercase tissue names that are wrongly formatted as title case.

    :param phi_df: the tissue column from PHI-base
    :type phi_df: pandas.Series
    :return: the tissue column with letter casing applied
    :rtype: pandas.Series
    """
    words_to_lowercase = [
        'Adult',
        'Blood',
        'Bone',
        'Brain',
        'Colon',
        'Embryo',
        'Fruit',
        'Gastrointestinal',
        'Gut',
        'Heart',
        'Kidney',
        'Larva',
        'Liver',
        'Lung',
        'Macrophage',
        'Petiole',
        'Popliteal',
        'Root',
        'Skin',
        'Spikelet',
        'Spleen',
        'Stem',
        'Tuber',
        'Urinary',
        'Urine',
    ]
    if tissues.isna().all():
        return tissues
    pattern = re.compile(fr"\b({'|'.join(words_to_lowercase)})\b")
    replacements = {word: word.lower() for word in words_to_lowercase}
    replace = lambda match: replacements[match.group(0)]
    return tissues.str.replace(pattern, replace, regex=True)


def parse_gene_inducer_ids(gene_inducer_ids):
    """Parse and convert the gene inducer ID column to a consistent format.

    :param phi_df: the gene inducer ID column from PHI-base
    :type phi_df: pandas.Series
    :return: the reformatted gene inducer ID column
    :rtype: pandas.Series
    """

    def make_pattern():
        # Make a regular expression to recognise all formats of gene inducer ID.
        anti_infective_label = '(?P<anti_inf>anti-infective)'
        chebi_id = 'CHEBI:\s*(?P<chebi_id>\d+)\s*'
        cas_id = '(?i:CAS\s*(?::|No[.:])\s*)?(?P<cas_id>\d+-\d+-\d+)'
        text = '(?P<text>[^\s:(]+|\(.+?\))'
        whitespace = '(?P<whitespace>\s+)'
        alternatives = (
            f'(?:{anti_infective_label}|{chebi_id}|{cas_id}|{text}|{whitespace})'
        )
        pattern = re.compile(alternatives)
        return pattern

    def lex_id_rows(rows, pattern):
        # Convert gene inducer IDs into a list of lexical tokens.
        lexed_rows = []
        for row in rows:
            if pd.isna(row):
                lexed_rows.append(row)
                continue
            symbols = []
            name = []
            in_name = False
            sep_pattern = re.compile('[:;,]$')
            for match in pattern.finditer(row):
                group = match.lastgroup
                text = match.group(group)
                if group not in ('text', 'whitespace') and in_name:
                    # Done parsing names; join and append the name parts
                    symbols.append(('name', ''.join(name).rstrip()))
                    in_name = False
                    name = []
                if group == 'chebi_id':
                    symbols.append(('chem_id', f'CHEBI:{text}'))
                elif group == 'cas_id':
                    symbols.append(('chem_id', f'CAS:{text}'))
                elif group == 'anti_inf':
                    symbols.append(('label', 'anti-infective'))
                elif group == 'whitespace':
                    if in_name:
                        name.append(' ')
                elif group == 'text':
                    if sep_pattern.fullmatch(text):
                        # Don't include separators
                        continue
                    if text.isdigit():
                        # Treat single digits as chemical IDs
                        symbols.append(('chem_id', text))
                        continue
                    # Otherwise assume the text is a chemical name
                    in_name = True
                    end_sep_match = sep_pattern.search(text)
                    if end_sep_match:
                        name.append(sep_pattern.sub('', text))
                        symbols.append(('name', ' '.join(name)))
                        name = []
                    else:
                        name.append(text)
            lexed_rows.append(symbols)
        return lexed_rows

    def parse_lexed_rows(rows):
        # Parse the lexical tokens and create a correctly formatted
        # representation of each gene inducer ID.
        parsed_rows = []
        for row in rows:
            if not isinstance(row, list):
                # Assume the row is NaN if it's not a list.
                parsed_rows.append(row)
                continue
            row_text = []
            context = None
            previous_token = None
            for token_type, value in row:
                if token_type == 'label':
                    if previous_token:
                        row_text.append('; ')
                    row_text.append(value)
                    context = 'label'

                elif token_type == 'name':
                    if previous_token == 'chem_id':
                        row_text.append('; ')
                    elif previous_token == 'name':
                        row_text.append(', ')
                    elif previous_token == 'label':
                        row_text.append(': ')
                    row_text.append(value)
                    context = 'name'

                elif token_type == 'chem_id':
                    if previous_token == 'name':
                        row_text.append(': ')
                    elif context:
                        row_text.append(', ')
                    elif previous_token:
                        row_text.append('; ')
                    row_text.append(value)
                else:
                    raise ValueError(f'unsupported token type {token_type}')
                previous_token = token_type

            parsed_rows.append(''.join(row_text))
        return parsed_rows

    if gene_inducer_ids.isna().all():
        return gene_inducer_ids
    # Trailing semicolons are a formatting error
    ids = gene_inducer_ids.str.rstrip(';').values
    pattern = make_pattern()
    lexed_rows = lex_id_rows(ids, pattern)
    parsed_rows = parse_lexed_rows(lexed_rows)
    series = pd.Series(
        parsed_rows,
        index=gene_inducer_ids.index,
        name=gene_inducer_ids.name,
    )
    return series


def parse_go_annotation(go_annotation):
    """Parse and convert the GO annotation column to a consistent format.

    :param phi_df: the GO annotation column from PHI-base
    :type phi_df: pandas.Series
    :return: the reformatted GO annotation column
    :rtype: pandas.Series
    """
    go_id = '(?P<go_id>GO:\d+)'
    evidence = '(?P<evidence>IDA|IEA|IGI|IMP|IPI|ISS|NAS|ND|TAS)'
    pattern = re.compile(f'{go_id}(?:[,;]\s*{evidence})?')
    parsed_rows = []
    for row in go_annotation.values:
        if row is np.nan:
            parsed_rows.append(row)
            continue
        parsed = []
        for match in pattern.finditer(row):
            go_id, evidence = match.group('go_id'), match.group('evidence')
            if go_id:
                parts = [go_id]
                if evidence:
                    parts.append(evidence)
                parsed.append(', '.join(parts))
        if parsed:
            parsed_rows.append('; '.join(parsed))
        else:
            parsed_rows.append(row)  # Keep the original value
    series = pd.Series(
        parsed_rows,
        index=go_annotation.index,
        name=go_annotation.name,
    )
    return series


def parse_interacting_partners_id(interacting_partners_ids):
    pattern = re.compile(
        r'(?P<db>UniProt|GenBank|EMBL|Ensembl Genomes)'
        r'|(?P<nan>no data found)'
        r'|(?P<word>\S+)'
    )
    parsed_rows = []
    for value in interacting_partners_ids.values:
        if pd.isna(value):
            parsed_rows.append(value)
            continue
        parsed = []
        partner = []
        state = None
        for match in pattern.finditer(value):
            text = match.group(0)
            match match.lastgroup:
                case 'db':
                    if state == 'gene':
                        parsed.append(f"{' '.join(partner)},")
                        partner = []
                    parsed.append(f'{text}:')
                    state = 'db'
                case 'nan':
                    parsed.append('no data found;')
                    state = None
                case 'word':
                    if text in (':', ';', ','):
                        continue
                    if state == 'db':
                        text = text.rstrip(';')
                        parsed.append(f'{text};')
                        state = None
                    else:
                        partner.append(text)
                        state = 'gene'
                case _:
                    raise NotImplementedError
        parsed_rows.append(' '.join(parsed).rstrip(';'))

    series = pd.Series(
        parsed_rows,
        index=interacting_partners_ids.index,
        name=interacting_partners_ids.name,
    )
    return series


def get_converted_curation_dates(curation_dates):
    """Convert curation dates in PHI-base to ISO 8601 format.

    :param curation_dates: the curation dates from PHI-base
    :type curation_dates: pandas.Series
    :returns: the converted curation dates
    :rtype: pandas.Series
    """

    # First we need to fix inconsistent month-year and year-month dates
    # with two-digit years, else these will fail to parse.
    month_year_pattern = r'^([A-Z][a-z]{2})-(\d{2})$'
    year_month_pattern = r'^(\d{2})-([A-Z][a-z]{2})$'
    fixed_dates = (
        curation_dates
        .astype(str)
        .str.strip()
        .str.replace(month_year_pattern, r'\1-20\2', regex=True)
        .str.replace(year_month_pattern, r'\2-20\1', regex=True)
    )
    converted_dates = pd.to_datetime(
        fixed_dates, format='mixed', dayfirst=True,
    )
    return converted_dates


def apply_replacements(phi_df):
    """Replace incorrect values in PHI-base.

    :param phi_df: the PHI-base DataFrame
    :type phi_df: pandas.DataFrame
    :returns: the PHI-base DataFrame with replacements applied
    :rtype: pandas.DataFrame
    """
    yes_no_replacement = {
        '(?i)(yes)': 'yes',
        '(?i)(no)': 'no',
    }
    mpp_doi = (
        'Mol Plant Pathol. 2023 Mar 13. doi: 10.1111/mpp.13321. Online ahead of print'
    )
    replacements = {
        'protein_id_source': {
            '(?i)uniprot': 'UniProt',
        },
        'gene_id_source': {
            '(?i)(genbank|genban)': 'GenBank',
            'F\. virguliforme genome database.*': 'FVG',
        },
        'protein_id': {
            'A0A0V3MA40.1': 'A0A0V3MA40',
            'A0A060VRS3n': 'A0A060VRS3',
            'SSRP_XANCP': 'Q8PAL7',
        },
        'gene_id': {
            'EU 984498': 'EU984498',
            'HM 486909': 'HM486909',
            'HM 486908': 'HM486908',
            'EU770253/EU746409': 'EU770253; EU746409',
            'SeD_A1212 to SeD_A1243': 'SeD_A1212-SeD_A1243',
            'WP_012027976.1\)': 'WP_012027976',
            'xp 007930394 1': 'XP_007930394',
            '- ': '-',
        },
        'chromosome_location': {
            '(?i)unknown': 'unknown',
            '(?i)chromosome?': 'chromosome',
            'chromosome-6': 'chromosome 6',
            'chromosome8': 'chromosome 8',
        },
        'interacting_partners_id': {
            'Uniport': 'UniProt',
            '(?i)uniprot': 'UniProt',
            '(?i)gene?bank': 'GenBank',
            'AAA23130; CAR54869; CAR53776': (
                'GenBank: AAA23130; GenBank: CAR54869; GenBank: CAR53776'
            ),
            '^EHA50760$': 'GenBank: EHA50760',
            '^EAL89498$': 'GenBank: EAL89498',
            '^Q9M5J9$': 'UniProt: Q9M5J9',
            ';$': '',
            ':(?! )': ': ',
            '\s*;\s*': '; ',
        },
        'multiple_mutation': {
            '^no$': np.nan,
        },
        'pathogen_species': {
            'Botrytis Cinerea': 'Botrytis cinerea',
        },
        'host_description': {
            '&': 'and',
            'No host tests done': np.nan,
            '(?i)lethal pathogen phenotype': np.nan,
        },
        'host_id': {
            'No host tests done': np.nan,
            'Lethal pathogen phenotype': np.nan,
        },
        'host_species': {
            'No host tests done': np.nan,
            'Lethal pathogen phenotype': np.nan,
        },
        'host_genotype_id': {
            '(?i)uniprot': 'UniProt',
            '(?i)gene?bank': 'GenBank',
        },
        'gene_function': {
            'Adenyly l Cyclase': 'adenylyl cyclase',
            '\s*-\s*': '-',
            r'Arf\b': 'ARF',
            'Bi-functional': 'Bifunctional',
            'p erithecial': 'perithecial',
            'Class-?II': 'Class II',
            'Endo-β': 'Endo-beta',
            'Esat-6': 'ESAT-6',
            'Myc(?=\b)': 'MYC',
            'Serine h ydroxymethyltra nsferase': 'Serine hydroxymethyltransferase',
            '(?i)bzip': 'bZip',
            'lps biosynthesis': 'LPS biosynthesis',
            'Dmt': 'DMT',
            'Ga\b': 'G\N{GREEK SMALL LETTER ALPHA}',
            'Rnase': 'RNase',
            'TeLOmere': 'telomere',
            'Dnase': 'DNase',
            'LziP': 'LZIP',
        },
        'go_annotation': {
            'GO:00016020': 'GO:0001602',
        },
        'mating_defect': yes_no_replacement,
        'pre_penetration_defect': {
            **yes_no_replacement,
            'no data found \(as no conidiation\)': np.nan,
            'wild type': 'no',
        },
        'penetration_defect': yes_no_replacement,
        'post_penetration_defect': {
            **yes_no_replacement,
            '^yes reduced': 'yes (reduced)',
            '^reduced': 'yes (reduced)',
        },
        'essential_gene': yes_no_replacement,
        'gene_inducer': {
            r'Caffein\b': 'caffeine',
            r'Cong\b': 'Congo',
            'nikkomycinZ': 'nikkomycin Z',
            '\N{ACUTE ACCENT}': '\N{PRIME}',
        },
        'gene_inducer_id': {
            '^reduced': np.nan,
            'carbendazim: CHEBI_3392:sensitivity_wild type': 'carbendazim: CHEBI:3392',
            'normal sensitivity toward carbendazim': 'carbendazim: CHEBI:3392',
            '\N{ACUTE ACCENT}': '\N{PRIME}',
            r'Cong\b': 'Congo',
            'Calcofuor': 'Calcofluor',
        },
        'host_target_id': {
            '(?i)uniprot': 'UniProt',
            '(?i)gene?bank': 'GenBank',
            '(?i)(UniProt|Ensembl):(?! )': r'\1: ',
            'np 001105479': 'NP_001105479',
            'Rcr3: ': 'Rcr3 ',
            'AT4G39090': 'Ensembl: AT4G39090',
        },
        'entered_by': {
            ',': ';',
        },
        'author_reference': {
            r'\bL\si\b': 'Li',
            r'\bSan\stiago\b': 'Santiago',
            '- ': '-',
            '[,*]$': '',
            '\N{LATIN SMALL LETTER DOTLESS I}\N{DIAERESIS}': 'ï',
            '\N{LATIN SMALL LETTER DOTLESS I}\N{ACUTE ACCENT}': 'í',
            'e\N{ACUTE ACCENT}\s*|\s*\N{ACUTE ACCENT}e': 'é',
            'o\N{ACUTE ACCENT}\s*|\s*\N{ACUTE ACCENT}o': 'ó',
            'Mol Microbiol. 2015 Oct 30': np.nan,
        },
        'reference_source': {
            '(?i)pubmed': 'PubMed',
        },
        'pmid': {
            '978-1-908230-25-6': np.nan,
        },
        'doi': {
            '10.1094./MPMI-10-100-0233': '10.1094/MPMI-10-10-0233',
            '\s*/\s*': '/',
            mpp_doi: '10.1111/mpp.13321',
        },
        'curator_organization': {
            '(?i)rres': 'RRes',
            '\s*/\s*': '; ',
        },
        'comments': {
            r'^s$': np.nan,
            r'\.\\': '.',
            r'^Asence\b': 'absence',
            '\( ': '(',
            ' \)': ')',
            'H\. Pylori': 'H. pylori',
            ' & ': ' and ',
            ';$': '',
            '\N{WHITE UP-POINTING SMALL TRIANGLE}': '\N{GREEK CAPITAL LETTER DELTA}',
            '\N{RIGHT TRIANGLE}': '\N{GREEK CAPITAL LETTER DELTA}',
        }
    }
    return phi_df.replace(replacements, regex=True)


def convert_integer_columns(phi_df):
    """Convert numeric columns in PHI-base to an integer type.

    Specifically, convert to Int64, which supports NaN without coercing
    numeric values to float.
    """
    integer_columns = (
        'pathogen_id',
        'pathogen_strain_id',
        'host_id',
        'pmid',
        'year',
    )
    for col in integer_columns:
        phi_df[col] = pd.to_numeric(phi_df[col]).astype('Int64')
    return phi_df


def fix_casing(phi_df):
    """Convert columns to lowercase while preserving special casing.

    :param phi_df: the PHI-base DataFrame
    :type phi_df: pandas.DataFrame
    :returns: the PHI-base DataFrame with case conversion applied
    :rtype: pandas.DataFrame
    """

    def variable_casing(column, excluded_words):
        exclude_pattern = re.compile(
            fr"\b({'|'.join(re.escape(word) for word in excluded_words)})\b"
        )
        ignore_pattern = re.compile(r'[^A-Z]|[A-Z](?=[0-9A-Z-]|\b)')
        separators = re.compile(r'(\s+|[()\[\]:;,./-])')
        cased = []
        for value in column.values:
            if pd.isna(value):
                cased.append(value)
                continue
            words = separators.split(value)
            cased_words = []
            for word in words:
                if not word:
                    # Skip empty strings from re.split
                    continue
                ignore = (
                    ignore_pattern.match(word)
                    or separators.match(word)
                    or exclude_pattern.match(word)
                )
                if ignore:
                    cased_words.append(word)
                else:
                    cased_word = word[0].lower() + word[1:]
                    cased_words.append(cased_word)
            cased.append(''.join(cased_words))
        assert len(cased) == len(column)
        return pd.Series(cased, index=column.index, name=column.name)

    pathway_exclusions = [
        'AbaA',
        'BfmR',
        'BfmS',
        'Ca2+',
        'Cek1',
        'Che2',
        'Chm1',
        'Chp',
        'Coxiella',
        'CrzA',
        'Doudoroff',
        'Embden',
        'FabA',
        'FabB',
        'Fus3',
        'GalN',
        'GalNAc',
        'GlcNAc',
        'Gpmk1',
        'Hog1',
        'HrpB',
        'HrpG',
        'HrpX',
        'HrpY',
        'Kennedy',
        'Kiss1',
        'Kss1',
        'Leloir',
        'LuxS',
        'Meyerhof',
        'MgRac1',
        'Mgv1',
        'Mla',
        'MpkA',
        'Mps1',
        'NulO',
        'Pal',
        'Parnas',
        'Pfs',
        'Pil',
        'Pmk1',
        'PprB',
        'PrhG',
        'Ras',
        'RhlR',
        'Rim',
        'RopB',
        'RpoN',
        'RpoS',
        'SahH',
        'SakA',
        'Slt2',
        'Ste11',
        'Ste7',
        'Tat',
        'TeA',
        'Toll',
        'VacJ',
        'WetA',
        'Wzx',
        'Wzy',
    ]
    gene_function_exclusions = [
        'Abi',
        'Ada',
        'AdeH',
        'AdeK',
        'AflR',
        'AgI',
        'Agr',
        'AirSR',
        'Ala',
        'Alderase',
        'AorFlbE',
        'ApbE',
        'AphB',
        'Ara4N',
        'AraC',
        'ArgJ',
        'ArnT',
        'ArsR',
        'AspB',
        'Aspergillus',
        'AtfA',
        'Atg20',
        'AtxA',
        'AvrE',
        'AvrXa21',
        'Ax21',
        'AzgA',
        'Beta2',
        'Bfa1',
        'BfeA',
        'Biedl',
        'Bin',
        'Borrelia',
        'Bsa',
        'Bub2',
        'Burkholderia',
        'Ca',
        'Ca2',
        'Ca2+',
        'Ca2C',
        'CaM',
        'Cag',
        'Candida',
        'Cap1',
        'Cdc2',
        'CebEFG',
        'CesD',
        'Cholera',
        'ChsE',
        'Cl',
        'ClcA',
        'Clp',
        'CoA',
        'CoAdehydrogenase',
        'CoAligase',
        'ComD',
        'CorA',
        'CovR',
        'CpcA',
        'Cps2F',
        'CpsA',
        'CpxR',
        'CstA',
        'Cu',
        'Curli',
        'CyoA',
        'Cys',
        'Cys6',
        'DedA',
        'DegP',
        'DeoR',
        'Derlin',
        'Diels',
        'Dis1',
        'DnaK',
        'DsbA',
        'DspA',
        'DtxR',
        'EamA',
        'Eg',
        'Egh16',
        'EmrAB',
        'Epc',
        'EscC',
        'EscD',
        'EscE',
        'EspB',
        'EsxA',
        'EsxB',
        'Fcr3',
        'Fe',
        'Fe2+',
        'Fe3+',
        'Fec',
        'FecI',
        'FepE',
        'FimA',
        'Fis',
        'FlgA',
        'FlhD',
        'FliR',
        'Flp',
        'FonAP',
        'Francisella',
        'Fur',
        'Fus3',
        'Fusarium',
        'Ga',
        'GalNAc',
        'Gas1',
        'Gcn5',
        'GdpX1',
        'GlcA',
        'GlcN',
        'GlcN6P',
        'GlcNAc',
        'GlcNAcP',
        'GldG',
        'GldK',
        'GldM',
        'Gldk',
        'Glk',
        'Gly',
        'GntR',
        'Grx3',
        'Gtr',
        'HadBC',
        'HapX',
        'Hcp',
        'Hcp1',
        'Hex1',
        'HexR',
        'Hfq',
        'Hha',
        'HlyD',
        'Hog1p',
        'Holliday',
        'Hpr',
        'HrcC',
        'HrcQb',
        'Hrp',
        'HrpG',
        'HrpL',
        'HrpQ',
        'HrpX',
        'HrpY',
        'HsdM',
        'Hsp20',
        'Hsp40',
        'HtrA',
        'HxfA',
        'Hþ',
        'IbeR',
        'IclR',
        'Icm',
        'IcmF',
        'IcsA',
        'Ig',
        'IgG',
        'IgM',
        'IglE',
        'InvL',
        'IroN',
        'JlbA',
        'JmjC',
        'Js',
        'Jumonji',
        'Kelch',
        'Kss1',
        'LacI',
        'Laccase2',
        'Lae1',
        'Lancefield',
        'LasR',
        'LcrH',
        'LipA',
        'Lon',
        'LpxO2',
        'Lsr2',
        'LuxI',
        'LuxR',
        'LysM',
        'LysR',
        'LytM',
        'LytR',
        'LziP',
        'MadM',
        'MalF',
        'MaoC',
        'MarR',
        'MbtH',
        'Mce',
        'MeaB',
        'MerR',
        'MesA',
        'MetQ',
        'MetR',
        'Mg',
        'Mg2+',
        'Mga',
        'MinC',
        'MinD',
        'MipA',
        'MlaABCDEF',
        'MmpL',
        'MmpS',
        'Mn',
        'Mn2+',
        'Mnh',
        'MoAP1',
        'MoSNF1',
        'MobA',
        'MocR',
        'ModABC',
        'MpkC',
        'MurA',
        'MutT',
        'Myb',
        'Myc',
        'Mycobacterium',
        'Na',
        'Na+',
        'Nep1',
        'NlpA',
        'NorR',
        'Nox',
        'NtrC',
        'NusB',
        'OhrR',
        'OmpA',
        'OmpC',
        'OmpD',
        'OmpF',
        'OmpV',
        'Omt',
        'OpiA',
        'Opp',
        'OppD1',
        'OprD',
        'PaR',
        'PaaK',
        'PadR',
        'Pal',
        'PalF',
        'PalH',
        'PdeK',
        'PdeR',
        'PdxS',
        'PdxT',
        'Pex11',
        'Pgp3',
        'PhoP',
        'PhoPQ',
        'PhoQ',
        'PhoU',
        'PiGPB1',
        'PilE',
        'PilW',
        'Plasmodium',
        'Ply',
        'PncA',
        'PobR',
        'Pol',
        'PorT',
        'PqaB',
        'PrrF1',
        'PrrF2',
        'PrsW',
        'Pseudomonas',
        'PspA',
        'PspB',
        'Psr',
        'PstA',
        'Ptc2',
        'Pts',
        'PvdI',
        'PvdJ',
        'PvdL',
        'Qc',
        'QseB',
        'QseC',
        'Rab',
        'Rab5',
        'Rab7',
        'Rac',
        'Ran',
        'RanGTP',
        'Ras',
        'RasGEF',
        'RcsA',
        'RcsB',
        'RfpC',
        'Rgg',
        'RhlR',
        'Rho',
        'Rho4',
        'RhoA',
        'RicR',
        'Rich',
        'Rim21',
        'Rim8',
        'RmIC',
        'Rpd3L',
        'RpfFBc',
        'RpfG',
        'RpfR',
        'RpiR',
        'RpoS',
        'Rvs',
        'RxLR',
        'SaeR',
        'SaeS',
        'SakA',
        'Salmonella',
        'SarA',
        'Sca',
        'Sdr',
        'Sec',
        'SecA',
        'SecY',
        'Sel1',
        'SerB',
        'Set3',
        'Shiga',
        'SifA',
        'Sit4',
        'Slt2',
        'Sn',
        'Snf1',
        'SnodProt1',
        'Sod_Cu',
        'SopB',
        'SpoIIE',
        'SpoT',
        'Spt',
        'SrrAB',
        'SsaE',
        'SsaV',
        'SsrA',
        'Ste12',
        'Streptococcus',
        'Stu2',
        'Su',
        'SycD',
        'Tad',
        'TagF',
        'TauD',
        'TcGALE',
        'TcaA',
        'TcpC',
        'TeA',
        'TehB',
        'TerC',
        'TetR',
        'Th1',
        'ThiS',
        'Thr',
        'TldD',
        'Tol',
        'Toll',
        'TonB',
        'Tps1',
        'Trk',
        'Trp',
        'Tu',
        'TviC',
        'Tyr',
        'Uds1',
        'UreF',
        'UvrD',
        'Vam6',
        'Vgr',
        'VgrG',
        'Vi',
        'VipB',
        'VirB8',
        'Vl43',
        'Vpma',
        'VpmaUprecursor',
        'VpmaVprecursor',
        'VpmaWprecursor',
        'VpmaXprecusor',
        'VpmaYprecursor',
        'VpmaZprecursor',
        'WalR',
        'Wor1',
        'Xanthomonas',
        'Xoo',
        'Yersinia',
        'YfiBNR',
        'YopJ',
        'YqeH',
        'Ysa',
        'Ysc',
        'YscC',
        'YscD',
        'YscE',
        'Zn',
        'Zn2',
        'Zn2+',
        'Zn2Cys6',
        'Zur',
    ]
    gene_inducer_exclusions = [
        'AgNO3',
        'Al3+',
        'Arg',
        'Br',
        'Ca',
        'Ca+',
        'Ca2+',
        'CaCl2',
        'Cd2+',
        'CdCl2',
        'CdSO4',
        'CoCl2',
        'Congo',
        'Cr',
        'CsA',
        'CsCl',
        'Cu',
        'Cu2+',
        'CuCl2',
        'CuOOH',
        'CuSO4',
        'CySNO',
        'EtBr',
        'Fe',
        'Fe3+',
        'FeCl3',
        'FeSO4',
        'HgCl2',
        'Leu',
        'LiCl',
        'Mg',
        'Mg2+',
        'MgCl2',
        'MgSO4',
        'Mn2+',
        'MnCl2',
        'MnSO4',
        'MreB',
        'MsDef1',
        'Na',
        'NaCl',
        'NaHCO3',
        'NaNO2',
        'NaNO3',
        'NaOCl',
        'Ni2+',
        'NiCl2',
        'NiSO4',
        'RsAFP2',
        'SbIII',
        'SnP',
        'TeO3',
        'Zn',
        'Zn2+',
        'ZnCl2',
        'ZnSO4',
    ]
    gene_inducer_id_exclusions = [
        'AgNO3',
        'Al3+',
        "Angeli's",
        'Arg',
        'Bort',
        'Br',
        'Ca',
        'Ca2+',
        'CaCl2',
        'Cd2+',
        'CdCl2',
        'CdSO4',
        'CoCl2',
        'Congo',
        'Cr',
        'CsA',
        'CsCl',
        'Cu2+',
        'CuCl2',
        'CuOOH',
        'CuSO4',
        'EtBr',
        'Fe',
        'Fe3+',
        'FeCl3',
        'FeSO4',
        'Flud',
        'HgCl2',
        'Ipro',
        'Ko2',
        'Leu',
        'LiCl',
        'Luperox',
        'Mg',
        'MgCl2',
        'MgSO4',
        'Mn2+',
        'MnCl2',
        'MnSO4',
        'Na',
        'NaCl',
        'NaHCO3',
        'NaNO2',
        'NaNO3',
        'NaNo2',
        'NaOCl',
        'Ni2+',
        'NiCl2',
        'NiSO4',
        'Nile',
        'Philabuster',
        'Rap',
        'SnP',
        'TeO3',
        'Triton',
        'Uvitex',
        'Zn',
        'Zn2+',
        'ZnCl2',
        'ZnSO4',
    ]
    exp_technique_transient_exclusions = [
        'Agrobacterium',
        'Arabidopsis',
        'Avr',
        'Avr3bP132A',
        'BiFC',
        'CfHNNI1',
        'Col',
        'GmNDR1',
        'GmNDR1a',
        'GmRINa',
        'GmRINb',
        'GmRINc',
        'GmRINd',
        'His',
        'MyC',
        'Mycobacterium',
        'Nb',
        'ProBs314EBE',
        'ProBs31EBE',
        'PsPSR2',
        'Western',
        'WsB',
        'XopK',
    ]
    # TODO: Decide whether to include anti_infective_agent for Zenodo
    columns = [
        'disease_manifestation',
        'exp_technique_stable',
        'exp_technique_transient',
        'gene_function',
        'gene_inducer',
        'gene_inducer_id',
        'host_description',
        'host_response',
        'in_vitro_growth',
        'interaction_phenotype',
        'pathway',
        'sexual_spores',
        'spore_germination',
        'vegetative_spores',
    ]
    exclusions = {
        'disease_manifestation': ['CFUs'],
        'exp_technique_stable': ['RpoN', 'Candida'],
        'exp_technique_transient': exp_technique_transient_exclusions,
        'host_response': ['PemG1'],
        'in_vitro_growth': ['CM'],
        'interaction_phenotype': ['BiCF', 'BiFC'],
        'pathway': pathway_exclusions,
        'gene_function': gene_function_exclusions,
        'gene_inducer': gene_inducer_exclusions,
        'gene_inducer_id': gene_inducer_id_exclusions,
    }
    for col in columns:
        column = phi_df[col]
        if column.isna().all():
            continue
        column_exclusions = exclusions.get(col)
        if column_exclusions:
            phi_df[col] = variable_casing(column, column_exclusions)
        else:
            phi_df[col] = column.str.lower()

    # Fix some already lowercased values
    if phi_df.vegetative_spores.notna().any():
        phi_df.vegetative_spores = phi_df.vegetative_spores.str.replace(
            r'\bwt\b', 'WT', regex=True
        )
    return phi_df


def replace_missing_data_placeholders(phi_df):
    """Replace missing data placeholders with NaN.

    Missing data placeholders are preserved in the columns 'protein_id' and
    'doi.'

    :param phi_df: the PHI-base DataFrame
    :type phi_df: pandas.DataFrame
    :return: the PHI-base DataFrame with missing data placeholders replaced
    :rtype: pandas.DataFrame
    """
    pattern = re.compile(r'(?i)^no data found$')
    ignore_columns = ['protein_id', 'doi']
    columns = phi_df.columns.difference(ignore_columns)
    phi_df[columns] = phi_df[columns].replace(pattern, np.nan)
    return phi_df


def clean_phibase(phi_df):
    """Apply cleaning functions to the PHI-base DataFrame.

    :param phi_df: the PHI-base DataFrame
    :type phi_df: pandas.DataFrame
    :return: the cleaned PHI-base DataFrame
    :rtype: pandas.DataFrame
    """
    phi_df = phi_df.rename(columns=lambda x: x.strip())  # strip column names
    phi_df = remove_excluded_columns(phi_df)
    phi_df = fix_whitespace(phi_df)
    phi_df = normalize_column_names(phi_df)
    phi_df = replace_missing_data_placeholders(phi_df)

    # Normalize Unicode characters
    phi_df = phi_df.replace(
        {
            '\N{LATIN SMALL LIGATURE FFI}': 'ffi',
            '\N{LATIN SMALL LIGATURE FL}': 'fl',
            '\N{LATIN SMALL LIGATURE FF}': 'ff',
            '\N{LATIN SMALL LIGATURE FFL}': 'ffl',
            '\N{LATIN SMALL LIGATURE FI}': 'fi',
            '\N{LEFT SINGLE QUOTATION MARK}': "'",
            '\N{RIGHT SINGLE QUOTATION MARK}': "'",
            '\N{LEFT DOUBLE QUOTATION MARK}': '"',
            '\N{RIGHT DOUBLE QUOTATION MARK}': '"',
            '\N{HYPHEN}': '-',
            '\N{NON-BREAKING HYPHEN}': '-',
            '\N{HEAVY WIDE-HEADED RIGHTWARDS ARROW}': '\N{RIGHTWARDS ARROW}',
            '\N{LEFT-TO-RIGHT MARK}': '',
            '\N{INCREMENT}': '\N{GREEK CAPITAL LETTER DELTA}',
            '\N{WHITE UP-POINTING TRIANGLE}': '\N{GREEK CAPITAL LETTER DELTA}',
            # Invalid characters
            '\uf020': '',
            '\uf031': '',
            '\uf044': '',
        },
        regex=True,
    )

    columns_to_clear = ['curation_comments', 'todo', 'aa_sequence', 'nt_sequence']
    phi_df[columns_to_clear] = np.nan

    phi_df = apply_replacements(phi_df)
    phi_df = convert_integer_columns(phi_df)
    phi_df = fix_casing(phi_df)

    if phi_df.multiple_mutation.notna().any():
        # Extract PHI IDs and rejoin them to fix whitespace
        phi_df.multiple_mutation = (
            phi_df.multiple_mutation
            .str.findall('PHI:\d+')
            .str.join('; ')
        )

    phi_df.curation_date = get_converted_curation_dates(phi_df.curation_date)
    phi_df.disease = get_formatted_disease_names(phi_df.disease)
    phi_df.tissue = format_tissue_names(phi_df.tissue)
    phi_df.mutant_phenotype = phi_df.mutant_phenotype.str.lower()
    phi_df.gene_inducer_id = parse_gene_inducer_ids(phi_df.gene_inducer_id)
    phi_df.go_annotation = parse_go_annotation(phi_df.go_annotation)
    phi_df.interacting_partners_id = (
        parse_interacting_partners_id(phi_df.interacting_partners_id)
    )

    return phi_df
