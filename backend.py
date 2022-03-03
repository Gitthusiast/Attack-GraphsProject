import re
import DataPreperation as dp
import pandas as pd
from xml.dom import minidom


def create_data_structures(dfMulVAl):
    dp.create_ir_dict(dfMulVAl)
    dp.create_ir_name_dict()
    dp.create_explanation_keyword_dict(dfMulVAl['Explanation'])
    dp.create_MITRE_technique_dict(dfMulVAl['MITRE Enterprise Technique'])
    print()


def search_by_technique(technique):
    """
    :param technique: MITRE attack technique
    :return: list of row numbers or None if no match is found
    """

    return dp.TECHNIQUE_DICT.get(technique)


def search_by_keywods_in_description(keywords):
    """
    :param keyword: keyword or keywords to search in description
    :return: list of row numbers or None if no match is found
    """
    res = []
    for keyword in keywords.split():
        if dp.KEYWORDS_DICT.get(keyword.lower()):
            res.extend(dp.KEYWORDS_DICT[keyword.lower()])
    if len(res) == 0:
        return None
    return list(set(res))  # remove duplicates


def search_ir_by_head(ir_head):
    """
    :param name of interaction rule head
    :return: list of tuples (row,ir_body) or None if no match is found
    """

    return dp.INTERACTION_RULES_BY_HEAD.get(ir_head)


def search_by_rule_name(ir_head_name):
    """
    :param name of rule head
    :return: list of tuples (row,ir_body) or None if no match is found
    """

    return dp.INTERACTION_RULES_BY_HEAD_NAME.get(ir_head_name)


def help_search(lst, a_list):
    if a_list is not None:
        if len(lst) != 0:
            tup_list = set()
            for row in lst:
                if row not in a_list:
                    tup_list.add(row)
            for num_row in tup_list:
                lst.remove(num_row)
        else:
            tmp_list = [num for num in a_list]
            for item in tmp_list:
                if type(item) == int:
                    lst.add(item)
                else:
                    lst.add(item[0])
    return lst


def search(search_sir_head, search_rule, search_in_description, technique_spinner):

    """
    :param instance - of click on show results button
    :return: find all the common rows and return array of tuples that conntains explanation, ir and technique name
    """
    # sir head
    sir_head, rule, description, technique = None, None, None, None
    if search_sir_head != '':
        sir_head = search_ir_by_head(search_sir_head)
    # rule
    if search_rule != '':
        rule = [tup[0] for tup in search_by_rule_name(search_rule)]
    # description
    if search_in_description != '':
        description = search_by_keywods_in_description(search_in_description)
    # technique
    if technique_spinner != '':
        technique = search_by_technique(technique_spinner)

    rows = set()
    # for sir head
    if sir_head is not None:
        rows.update([tup[0] for tup in sir_head])
    # for rule
    rows = help_search(rows, rule)
    # for keyword in description
    rows = help_search(rows, description)
    # for technique
    rows = help_search(rows, technique)

    if search_sir_head == '' and search_rule == '' and search_in_description == '' and technique_spinner == 'technique':
        rows = dp.ROW_TO_IR.keys()

    rows = sorted(rows)

    res = list()
    for row in rows:
        expla = dp.explanations.get(row)
        if expla is None:
            expla = ''
        ir_head = dp.ROW_TO_IR.get(row)
        ir = ''
        if ir_head is None:
            ir = ''
        else:
            ir_body_string = ":- "
            ir_bodies = search_ir_by_head(ir_head)
            for ir_body in ir_bodies:
                if ir_body[1] is None:
                    continue
                elif ir_body[0] == row:
                    for body_part in ir_body[1]:
                        ir_body_string += body_part[1] + ', '
            if ir_body_string != ":- ":
                ir_body_string = ir_body_string[:-2]  # to remove the last comma
                ir_body_string += '.'
                ir = ir_head + ir_body_string
            else:
                ir = ir_head + '.'

        techni = dp.techniques.get(row)
        if techni is None:
            techni = ""
        res.append((expla, ir, techni))
    print(res)
    print(rows)
    return res, rows


def create_xml(rows):
    """
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
        explenation = dp.explanations.get(row)
        if not explenation:
            explenation = ''
        desc.appendChild(doc.createTextNode(explenation.strip()))
        ir.appendChild(desc)

        technique = doc.createElement('Technique')
        technique.appendChild(doc.createTextNode(dp.techniques[row].strip()))
        ir.appendChild(technique)

    xml_str = doc.toprettyxml(indent="\t")

    save_path_file = "output.xml"

    with open(save_path_file, "w") as f:
        f.write(xml_str)


def create_pddl(rows):
    """
    :param list of rows to include in the pddl
    :return:
    """
    with open('pddl.txt', 'w') as f:
        f.write('/*************************/\n'
                '/ Predicates Declarations /\n'
                '/*************************/\n')
        primitives = []
        for row in rows:
            if not dp.ROW_TO_IR.get(row):
                continue
            ir_head = dp.ROW_TO_IR[row]
            if dp.PRIMITIVE_DERIVED_DICT[row] == 'primitive' and ir_head not in primitives:
                f.write('primitive(' + ir_head.strip('. ') + ').\n')
                primitives.append(ir_head)
        f.write('\n')

        derivedes = []
        for row in rows:
            if not dp.ROW_TO_IR.get(row):
                continue
            ir_head = dp.ROW_TO_IR[row]
            if dp.PRIMITIVE_DERIVED_DICT[row] == 'derived' and ir_head not in derivedes:
                f.write('derived(' + ir_head.strip() + ').\n')
                derivedes.append(ir_head)
        f.write('\nmeta(attackGoal(_)).\n\n')

        f.write('/*******************************************/\n'
                '/****      Tabling Predicates          *****/\n'
                '/* All derived predicates should be tabled */''\n'
                '/*******************************************/\n')
        derivedes= []
        for row in rows:
            if not dp.ROW_TO_IR.get(row):
                continue
            ir_head = dp.ROW_TO_IR[row]
            ir_head_parts = re.split("\(|,|\)", ir_head)
            ir_head_name = ir_head_parts[0]
            if dp.PRIMITIVE_DERIVED_DICT[row] == 'derived' and ir_head_name not in derivedes:
                f.write(':- table ' + ir_head_name.strip('. ') + '/1.\n')
                derivedes.append(ir_head_name)
        f.write('\n')
        f.write('/*******************/\n'
                '/ Interaction Rules /\n'
                '/*******************/\n')

        for row in rows:
            if not dp.ROW_TO_IR.get(row):
                continue
            ir_head = dp.ROW_TO_IR[row]
            for ir in dp.INTERACTION_RULES_BY_HEAD[ir_head]:
                if not ir[1]:
                    continue
                if ir[0] == row:
                    predicates = ir[1]
                    ir_to_wirte = 'interaction_rule(\n(' + ir_head + ' :- \n'
                    if predicates:
                        for i, predicate in enumerate(predicates):
                            if i == len(predicates) - 1:
                                ir_to_wirte += predicate[1] + '),\n'
                            else:
                                ir_to_wirte += predicate[1] + ',\n'
                        ir_to_wirte += 'rule_desc(\'' + dp.explanations[row].strip('. ') + '\', 1.0)).\n\n'
                    f.write(ir_to_wirte)


def empty_dicts():
    dp.INTERACTION_RULES_BY_HEAD = {}
    dp.INTERACTION_RULES_BY_BODY = {}
    dp.INTERACTION_RULES_BY_HEAD_NAME = {}
    dp.INTERACTION_RULES_BY_BODY_NAME = {}
    dp.ROW_TO_IR = {}
    dp.KEYWORDS_DICT = {}
    dp.TECHNIQUE_DICT = {}
    dp.PRIMITIVE_DERIVED_DICT = {}
    dp.explanations = {}
    dp.techniques = {}

def read_from_xml(path):
    dp.read_from_xml(path)

# if __name__ == "__main__":
#     path = "MulVAL to MITRE-for IR Manager.xlsx"
#     dfMulVAl = pd.read_excel(path)
#     create_data_structures(dfMulVAl)
#     rows = dp.ROW_TO_IR.keys()
    # create_xml(rows)

def build(path):
    # path = "MulVAL to MITRE-for IR Manager.xlsx"
    dfMulVAl = pd.read_excel(path)
    create_data_structures(dfMulVAl)
    rows = dp.ROW_TO_IR.keys()
