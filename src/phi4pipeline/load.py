# SPDX-FileCopyrightText: 2023-present James Seager <james.seager@rothamsted.ac.uk>
#
# SPDX-License-Identifier: MIT

import pandas as pd


def get_column_header_mapping(phi_df):
    """Map from the normalized column names to the original column names.

    The MultiIndex header rows need to be restored after processing in order
    to export to a spreadsheet in the correct format.

    :param phi_df: the PHI-base DataFrame
    :type phi_df: pandas.DataFrame
    :return: a mapping between normalized column names and original names
    :rtype: dict
    """
    renames = get_normalized_column_names()
    columns = phi_df.rename(columns=lambda x: x.strip()).columns
    level_0 = columns.get_level_values(0)
    level_1 = columns.get_level_values(1)
    index = level_1.isin(renames)
    label_zip = zip(renames.values(), level_0[index], level_1[index])
    return {
        norm_name: (header_0, header_1) for norm_name, header_0, header_1 in label_zip
    }


def get_normalized_column_names():
    """Get a mapping from default PHI-base column names to snake case format.

    :returns: a mapping between old and new column names
    :rtype: dict
    """
    return {
        'CurationComments': 'curation_comments',
        'Todo': 'todo',
        'RecordID': 'record_id',
        'PHIMolConnID': 'phi_id',
        'ProteinIDsource': 'protein_id_source',
        'ProteinID': 'protein_id',
        'GeneIDsource': 'gene_id_source',
        'GeneID': 'gene_id',
        'AAsequence': 'aa_sequence',
        'NTsequence': 'nt_sequence',
        'SequenceStrain': 'sequence_strain',
        'Gene': 'gene',
        'Chrlocation': 'chromosome_location',
        'GeneProteinmodification': 'gene_protein_modification',
        'ModifiedgeneproteinId': 'modified_gene_protein_id',
        'Interactingpartners': 'interacting_partners',
        'InteractingpartnersId': 'interacting_partners_id',
        'Multiplemutation': 'multiple_mutation',
        'PathogenID': 'pathogen_id',
        'Pathogenspecies': 'pathogen_species',
        'PathogenstrainID': 'pathogen_strain_id',
        'Pathogenstrain': 'pathogen_strain',
        'Disease': 'disease',
        'Hostdescription': 'host_description',
        'HostID': 'host_id',
        'Hostspecies': 'host_species',
        'Hoststrain': 'host_strain',
        'Hostgenotype': 'host_genotype',
        'HostgenotypeId': 'host_genotype_id',
        'Tissue': 'tissue',
        'GeneFunction': 'gene_function',
        'GOannotation': 'go_annotation',
        'Database': 'database',
        'Pathway': 'pathway',
        'MutantPhenotype': 'mutant_phenotype',
        'Matingdefect': 'mating_defect',
        'Prepenetrationdefect': 'pre_penetration_defect',
        'Penetrationdefect': 'penetration_defect',
        'Postpenetrationdefect': 'post_penetration_defect',
        'Diseasemanifestation': 'disease_manifestation',
        'Vegetativespores': 'vegetative_spores',
        'Sexualspores': 'sexual_spores',
        'Invitrogrowth': 'in_vitro_growth',
        'Sporegermination': 'spore_germination',
        'Essentialgene': 'essential_gene',
        'Geneinducer': 'gene_inducer',
        'GeneinducerId': 'gene_inducer_id',
        'Hosttarget': 'host_target',
        'HosttargetId': 'host_target_id',
        'Interactionphenotype': 'interaction_phenotype',
        'Hostresponse': 'host_response',
        'ExpTechniquestable': 'exp_technique_stable',
        'ExpTechniquetransient': 'exp_technique_transient',
        'Speciesexpert': 'species_expert',
        'Enteredby': 'entered_by',
        'PMID': 'pmid',
        'RefSource': 'reference_source',
        'DOI': 'doi',
        'Refdetail': 'reference_detail',
        'Authoremail': 'author_email',
        'Comments': 'comments',
        'Authorreference': 'author_reference',
        'Year': 'year',
        'Curationdetails': 'curation_details',
        'Filename': 'file_name',
        'Batchno': 'batch_number',
        'Curationdate': 'curation_date',
        'Curatororganization': 'curator_organization',
        'Lab': 'lab',
        'FGmycotoxin': 'fg_mycotoxin',
        'AntiinfectiveagentId': 'anti_infective_agent_id',
        'Antiinfectiveagent': 'anti_infective_agent',
        'Antiinfectivecompound': 'anti_infective_compound',
        'Antiinfectivetargetsite': 'anti_infective_target_site',
        'Antiinfectivegroupname': 'anti_infective_group_name',
        'AntiinfectiveChemicalgroup': 'anti_infective_chemical_group',
        'AntiinfectiveModeinplanta': 'anti_infective_mode_in_planta',
        'FRACCODE': 'frac_code',
        'Antiinfectivecomments': 'anti_infective_comments',
    }


def normalize_column_names(phi_df):
    """Convert column names to snake case, removing multiple header rows.

    :param phi_df: the PHI-base DataFrame
    :type phi_df: pandas.DataFrame
    :return: the PHI-base DataFrame with columns renamed
    :rtype: pandas.DataFrame
    """
    renames = get_normalized_column_names()
    phi_df.columns = phi_df.columns.get_level_values(1).str.strip()
    phi_df = phi_df.rename(columns=renames)
    assert phi_df.columns.str.fullmatch(r'\w+').all()
    return phi_df


def load_excel(path, sheet_name):
    """Load the PHI-base Excel spreadsheet from a given path.

    :param path: the path to the Excel spreadsheet
    :type path: str
    :param sheet_name: the name of the sheet to be loaded
    :type sheet_name: str
    :returns: the sheet as a pandas DataFrame
    :rtype: pandas.DataFrame
    """
    return pd.read_excel(path, sheet_name, header=[0, 1])


def get_column_header_mapping(phi_df):
    """Map from the normalized column names to the original column names.

    The MultiIndex header rows need to be restored after processing in order
    to export to a spreadsheet in the correct format.

    :param phi_df: the PHI-base DataFrame
    :type phi_df: pandas.DataFrame
    :return: a mapping between normalized column names and original names
    :rtype: dict
    """
    renames = get_normalized_column_names()
    columns = phi_df.rename(columns=lambda x: x.strip()).columns
    level_0 = columns.get_level_values(0)
    level_1 = columns.get_level_values(1)
    index = level_1.isin(renames)
    label_zip = zip(renames.values(), level_0[index], level_1[index])
    return {
        norm_name: (header_0, header_1) for norm_name, header_0, header_1 in label_zip
    }
