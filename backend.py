
import DataPreperation as dp
import pandas as pd


def create_data_structures(path):

    dfMulVAl = pd.read_excel(path)
    dp.create_ir_dict(dfMulVAl)
    dp.create_ir_name_dict()
    dp.create_explanation_keyword_dict(dfMulVAl)
    dp.create_MITRE_technique_dict(dfMulVAl)


def search_by_technique(technique):
    """
    :param technique: MITRE attack technique
    :return: list of row numbers or None if no match is found
    """

    return dp.TECHNIQUE_DICT.get(technique)


def search_by_keywods_in_description(keyword):
    """
    :param keyword: keyword
    :return: list of row numbers or None if no match is found
    """

    return dp.KEYWORDS_DICT.get(keyword)


def search_ir_by_head_name(ir_head_name):
    """
    :param name of interaction rule head
    :return: list of tuples (row,ir_body) or None if no match is found
    """

    return dp.INTERACTION_RULES_BY_HEAD_NAME.get(ir_head_name)


if __name__ == "__main__":

    path = 'C:\\Users\\ADMIN\\Documents\\AttackGraphs\\Attack-GraphsProject\\MulVAL to MITRE-for IR Manager.xlsx'
    create_data_structures(path)
    print(dp.TECHNIQUE_DICT.keys())
