
import DataPreperation
import pandas as pd

INTERACTION_RULES_BY_HEAD = {}
INTERACTION_RULES_BY_HEAD_NAME = {}
INTERACTION_RULES_BY_BODY_NAME = {}
INTERACTION_RULES_BY_BODY = {}
KEYWORDS_DICT = {}
TECHNIQUE_DICT = {}


def create_data_structures(path):

    dfMulVAl = pd.read_excel(path)
    INTERACTION_RULES_BY_HEAD, INTERACTION_RULES_BY_BODY = DataPreperation.create_ir_dict(dfMulVAl)
    INTERACTION_RULES_BY_HEAD_NAME, INTERACTION_RULES_BY_BODY_NAME \
        = DataPreperation.create_ir_name_dict(INTERACTION_RULES_BY_HEAD, INTERACTION_RULES_BY_BODY)
    KEYWORDS_DICT = DataPreperation.create_explanation_keyword_dict(dfMulVAl)
    TECHNIQUE_DICT = DataPreperation.create_MITRE_technique_dict(dfMulVAl)


def search_by_technique(technique):
    """
    :param technique: MITRE attack technique
    :return: list of row numbers or None if no match is found
    """

    return TECHNIQUE_DICT.get(technique)


def search_by_keywods_in_description(keyword):
    """
    :param keyword: keyword
    :return: list of row numbers or None if no match is found
    """

    return KEYWORDS_DICT.get(keyword)


def search_ir_by_head_name(ir_head_name):
    """
    :param name of interaction rule head
    :return: list of tuples (row,ir_body) or None if no match is found
    """

    return INTERACTION_RULES_BY_HEAD_NAME.get(ir_head_name)

path = 'C:\\Users\\ADMIN\\Documents\\AttackGraphs\\Attack-GraphsProject\\MulVAL to MITRE-for IR Manager.xlsx'
create_data_structures(path)
print(TECHNIQUE_DICT.keys())