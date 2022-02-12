
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


def create_xml(dfMulVAl, rows):
    """
    :param dfMulVAl: data frame containing the data from the xlsx file
    :param rows: list of row numbers to write to the xml file
    :return:
    """
    root = minidom.Document()

    xml = root.createElement('SIR')
    xml.setAttribute('Name', 'Geeks for Geeks')
    root.appendChild(xml)

    productChild = root.createElement('product')
    productChild.setAttribute('name', 'Geeks for Geeks')

    xml.appendChild(productChild)

    xml_str = root.toprettyxml(indent="\t")

    save_path_file = "output.xml"

    with open(save_path_file, "w") as f:
        f.write(xml_str)


if __name__ == "__main__":

    path = 'C:\\Users\\ADMIN\\Documents\\AttackGraphs\\Attack-GraphsProject\\MulVAL to MITRE-for IR Manager.xlsx'
    # create_data_structures(path)
    # print(dp.TECHNIQUE_DICT.keys())
    dfMulVAl = pd.read_excel(path)
    rows = [i for i in range(dfMulVAl.shape[0])]
    create_xml(dfMulVAl, rows)
