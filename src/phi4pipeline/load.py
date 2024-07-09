# SPDX-FileCopyrightText: 2023-present James Seager <james.seager@rothamsted.ac.uk>
#
# SPDX-License-Identifier: MIT

import re

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


def get_normalized_column_names(mode='excel'):
    """Get a mapping from default PHI-base column names to snake case format.

    :returns: a mapping between old and new column names
    :rtype: dict
    """
    if mode == 'excel':
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
    elif mode == 'csv':
        return {
            'Record ID': 'record_id',
            'PHI_MolConn_ID': 'phi_id',
            'Protein ID source': 'protein_id_source',
            'Protein ID': 'protein_id',
            'Gene ID source': 'gene_id_source',
            'Gene ID': 'gene_id',
            'AA sequence': 'aa_sequence',
            'NT sequence': 'nt_sequence',
            'Sequence Strain': 'sequence_strain',
            'Gene': 'gene',
            'Chr location': 'chromosome_location',
            'Gene/Protein modification': 'gene_protein_modification',
            'Modified gene/protein Id': 'modified_gene_protein_id',
            'Interacting partner(s)': 'interacting_partners',
            'Interacting partner(s) Id': 'interacting_partners_id',
            'Multiple mutation': 'multiple_mutation',
            'Pathogen ID': 'pathogen_id',
            'Pathogen species': 'pathogen_species',
            'Pathogen strain ID': 'pathogen_strain_id',
            'Pathogen strain': 'pathogen_strain',
            'Disease': 'disease',
            'Host description': 'host_description',
            'Host ID': 'host_id',
            'Host species': 'host_species',
            'Host strain': 'host_strain',
            'Host genotype': 'host_genotype',
            'Host genotype-Id': 'host_genotype_id',
            'Tissue': 'tissue',
            'Gene Function': 'gene_function',
            'GO annotation': 'go_annotation',
            'Database': 'database',
            'Pathway': 'pathway',
            'Mutant Phenotype': 'mutant_phenotype',
            'Mating defect': 'mating_defect',
            'Prepenetration defect': 'pre_penetration_defect',
            'Penetration defect': 'penetration_defect',
            'Postpenetration defect': 'post_penetration_defect',
            'Disease manifestation': 'disease_manifestation',
            'Vegetative spores': 'vegetative_spores',
            'Sexual spores': 'sexual_spores',
            'Invitro growth': 'in_vitro_growth',
            'Spore germination': 'spore_germination',
            'Essential gene': 'essential_gene',
            'Gene inducer': 'gene_inducer',
            'Gene inducer Id': 'gene_inducer_id',
            'Host target': 'host_target',
            'Host target Id': 'host_target_id',
            'Interaction phenotype': 'interaction_phenotype',
            'Host response': 'host_response',
            'Exp. Technique-stable': 'exp_technique_stable',
            'Exp. Technique-transient': 'exp_technique_transient',
            'Species expert': 'species_expert',
            'Entered by': 'entered_by',
            'PMID': 'pmid',
            'Ref. Source': 'reference_source',
            'DOI': 'doi',
            'Ref. detail': 'reference_detail',
            'Author email': 'author_email',
            'Comments': 'comments',
            'Author reference': 'author_reference',
            'Year': 'year',
            'Curation details': 'curation_details',
            'File name': 'file_name',
            'Batch no.': 'batch_number',
            'Curation date': 'curation_date',
            'Curator organization': 'curator_organization',
        }


def normalize_column_names(phi_df):
    """Convert column names to snake case, removing multiple header rows.

    :param phi_df: the PHI-base DataFrame
    :type phi_df: pandas.DataFrame
    :return: the PHI-base DataFrame with columns renamed
    :rtype: pandas.DataFrame
    """
    # TODO: Replace this hack with a check at the start of the pipeline
    mode = 'csv' if phi_df.columns[0] == 'Record ID' else 'excel'
    renames = get_normalized_column_names(mode)
    if phi_df.columns.nlevels > 1:
        phi_df.columns = phi_df.columns.get_level_values(1).str.strip()
    phi_df = phi_df.rename(columns=renames)
    assert phi_df.columns.str.fullmatch(r'\w+').all()
    return phi_df


def load_excel(path):
    """Load the PHI-base Excel spreadsheet from a given path.

    :param path: the path to the Excel spreadsheet
    :type path: str
    :param sheet_name: the name of the sheet to be loaded
    :type sheet_name: str
    :returns: the sheet as a pandas DataFrame
    :rtype: pandas.DataFrame
    """

    def get_version_from_filename(path):
        match = re.search(r'(\d[-.]\d\d)', path)
        if match is None:
            raise ValueError(f'No PHI-base version number found in path: {path}')
        return match.group(1)

    phibase_version = get_version_from_filename(path)
    sheet_name = f'{phibase_version} phibase_all'
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
