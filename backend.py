import re

import DataPreperation as dp
import pandas as pd
from xml.dom import minidom


def create_data_structures(dfMulVAl):

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


def create_xml(dfMulVAl):
    """
    :param dfMulVAl: data frame containing the data from the xlsx file
    :return:
    """
    doc = minidom.Document()
    root = doc.createElement('SIRS')
    doc.appendChild(root)

    for row in dp.ROW_TO_IR.keys():

        ir_head = dp.ROW_TO_IR[row]
        ir_head_parts = re.split("\(|,|\)", ir_head)
        ir_head_name = ir_head_parts[0]

        if root.firstChild is None:
            ir = doc.createElement('SIR')
            ir.setAttribute('Name', ir_head_name)
            root.appendChild(ir)
            # parameters = doc.createElement('Parameters')
            # ir.appendChild(parameters)
        else:
            ir = doc.createElement('SIR')
            ir.setAttribute('Name', ir_head_name)
            root.insertBefore(ir, root.firstChild)

    xml_str = doc.toprettyxml(indent="\t")

    save_path_file = "output.xml"

    with open(save_path_file, "w") as f:
        f.write(xml_str)


if __name__ == "__main__":

    path = 'C:\\Users\\ADMIN\\Documents\\AttackGraphs\\Attack-GraphsProject\\MulVAL to MITRE-for IR Manager.xlsx'
    dfMulVAl = pd.read_excel(path)
    create_data_structures(dfMulVAl)
    create_xml(dfMulVAl)
