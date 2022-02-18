import re
import DataPreperation as dp
import pandas as pd
from xml.dom import minidom


def create_data_structures(dfMulVAl):
    dp.create_ir_dict(dfMulVAl)
    dp.create_ir_name_dict()
    dp.create_explanation_keyword_dict(dfMulVAl['Explanation'])
    dp.create_MITRE_technique_dict(dfMulVAl['MITRE Enterprise Technique'])


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


def create_xml_from_df(explanations, techniques, rows):
    """
    :param explanations: list of explanations strings
    :param techniques: list of MITRE technique strings
    :param list of rows to inlcude in the xml
    :return:
    """
    doc = minidom.Document()
    root = doc.createElement('SIRS')
    doc.appendChild(root)
    rows = reversed(sorted(rows))

    for row in rows:

        if not dp.ROW_TO_IR.get(row):
            continue
        ir_head = dp.ROW_TO_IR[row]
        ir_head_parts = re.split("\(|,|\)", ir_head)
        ir_head_name = ir_head_parts[0]

        ir = doc.createElement('SIR')
        ir.setAttribute('Name', ir_head_name)

        if root.firstChild is None:
            root.appendChild(ir)
        else:
            root.insertBefore(ir, root.firstChild)
        parameters = doc.createElement('Parameters')
        ir.appendChild(parameters)

        for i, entity in enumerate(ir_head_parts[::-1]):
            if entity.strip() == ir_head_name or entity.strip() == '':
                continue
            ent = doc.createElement('Parameter')
            ent.setAttribute('Type', "IR_Head")
            ent.appendChild(doc.createTextNode(entity.strip()))
            if parameters.firstChild is None:
                parameters.appendChild(ent)
            else:
                parameters.insertBefore(ent, parameters.firstChild)

        body = doc.createElement('Body')
        ir.appendChild(body)
        for interaction_rule in dp.INTERACTION_RULES_BY_HEAD_NAME[ir_head_name]:
            if not interaction_rule[1]:
                continue
            for interaction_rule_body_part in reversed(interaction_rule[1]):
                if interaction_rule[0] != row:
                    continue
                ir_body_parts = re.split("\(|,|\)", interaction_rule_body_part[1])
                body_rule_name = ir_body_parts[0]

                rule = doc.createElement('Rule')
                rule.setAttribute('Name', body_rule_name)

                if root.firstChild is None:
                    body.appendChild(rule)
                else:
                    body.insertBefore(rule, body.firstChild)
                parameters = doc.createElement('Parameters')
                rule.appendChild(parameters)

                for i, entity in enumerate(ir_body_parts[::-1]):
                    if entity.strip() == body_rule_name or entity.strip() == '':
                        continue
                    ent = doc.createElement('Parameter')
                    ent.setAttribute('Type', "Entity")
                    ent.appendChild(doc.createTextNode(entity.strip()))
                    if parameters.firstChild is None:
                        parameters.appendChild(ent)
                    else:
                        parameters.insertBefore(ent, parameters.firstChild)

        desc = doc.createElement('Description')
        explenation = explanations.get(row)
        if not explenation:
            explenation = ''
        desc.appendChild(doc.createTextNode(explenation.strip()))
        ir.appendChild(desc)

        technique = doc.createElement('Technique')
        technique.appendChild(doc.createTextNode(techniques[row].strip()))
        ir.appendChild(technique)

    xml_str = doc.toprettyxml(indent="\t")

    save_path_file = "output.xml"

    with open(save_path_file, "w") as f:
        f.write(xml_str)


if __name__ == "__main__":
    path = 'C:\\Users\\ADMIN\\Documents\\AttackGraphs\\Attack-GraphsProject\\MulVAL to MITRE-for IR Manager.xlsx'
    dfMulVAl = pd.read_excel(path)
    create_data_structures(dfMulVAl)
    rows = dp.ROW_TO_IR.keys()
    create_xml_from_df(dp.explanations, dp.techniques, rows)
    print()
