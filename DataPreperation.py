import re
import pandas as pd
from nltk.corpus import stopwords
from xml.dom import minidom

INTERACTION_RULES_BY_HEAD = {}  # {ir_head: [(ROW, predicates),()]}
INTERACTION_RULES_BY_BODY = {}  # {predicate: [(row, ir_head),()]}
INTERACTION_RULES_BY_HEAD_NAME = {}  # {ir_head_name: [(ROW, predicates),()]}
INTERACTION_RULES_BY_BODY_NAME = {}  # {ir_body_name: INTERACTION_RULES_BY_BODY[ir_body]}
ROW_TO_IR = {}  # {row: ir_head}
KEYWORDS_DICT = {}  # {keyword.lower(): [row]}
TECHNIQUE_DICT = {}  # {technique: [row_number]}
PRIMITIVE_DERIVED_DICT = {}  # {row: ir_type}

explanations = {}  # {row, description}
techniques = {}  # {row, technique}


def create_ir_dict(dfMulVAl):
    """
    This function creates a dictionary {interaction_rule_head: (row_number, ir_body)}
    And a dictionary with {interaction_rule_head: (row_number, ir_head)}
    And a dict of {row_number, ir_head}
    :param path: data frame of the given xlsx file
    """

    for row, IR in enumerate(dfMulVAl['Interaction Rules']):

        if not pd.isna(dfMulVAl['Explanation'][row]):
            explanations.update({row: dfMulVAl['Explanation'][row]})
        else:
            explanations.update({row: ''})
        if not pd.isna(dfMulVAl['MITRE Enterprise Technique'][row]):
            techniques.update({row: dfMulVAl['MITRE Enterprise Technique'][row].strip()})
        else:
            techniques.update({row: ''})
        if not pd.isna(IR):

            PRIMITIVE_DERIVED_DICT.update({row: 'derived'})
            splited_ir = IR.split(":-")
            ir_head = splited_ir[0]
            if len(splited_ir[0].split('\n')) >= 2 and splited_ir[0].split('\n')[0][0] == '%':

                ir_head = ir_head.split('\n')[1]

            ir_head = ir_head.strip()
            ROW_TO_IR.update({row: ir_head})

            if len(splited_ir) >= 2:  # check body

                ir_body = re.split('\n', splited_ir[1])
                predicates = []
                for predicate in ir_body:

                    if len(predicate) >= 3 and predicate[1] != '%' and predicate[2] != '%':
                        if predicate[-1] == "," or predicate[-1] == '.':
                            predicate = predicate[:-1]
                        predicate = predicate.strip()
                        predicates.append((row, predicate))

                        if INTERACTION_RULES_BY_BODY.get(predicate) \
                                and (row, ir_head) not in INTERACTION_RULES_BY_BODY[predicate]:

                            if predicate not in INTERACTION_RULES_BY_BODY.keys():
                                INTERACTION_RULES_BY_BODY.update({predicate: [(row, ir_head)]})
                            else:
                                if ir_head not in INTERACTION_RULES_BY_BODY[predicate]:
                                    INTERACTION_RULES_BY_BODY[predicate] = [(row, ir_head)]
                                else:
                                    INTERACTION_RULES_BY_BODY[predicate].append(row, ir_head)
                add_to_ir_head_dict(ir_head, row, predicates)
            else:
                add_to_ir_head_dict(ir_head, row, None)
        else:
            ROW_TO_IR.update({row: dfMulVAl['Predicate'][row]})
            add_to_ir_head_dict(dfMulVAl['Predicate'][row], row, None)
            PRIMITIVE_DERIVED_DICT.update({row: 'primitive'})

        if not pd.isna(dfMulVAl['Primitive/Derived'][row]):
            PRIMITIVE_DERIVED_DICT.update({row: dfMulVAl['Primitive/Derived'][row].lower()})
        if not PRIMITIVE_DERIVED_DICT.get(row):
            PRIMITIVE_DERIVED_DICT.update({row: None})
    print()


def add_to_ir_head_dict(ir_head, row, predicates):

    if not INTERACTION_RULES_BY_HEAD.get(ir_head):
        INTERACTION_RULES_BY_HEAD.update({ir_head: [(row, predicates)]})
    else:
        INTERACTION_RULES_BY_HEAD[ir_head].append((row, predicates))


def create_ir_name_dict():

    for ir_head in INTERACTION_RULES_BY_HEAD.keys():
        ir_head_name = ir_head.split('(')[0]
        if not INTERACTION_RULES_BY_HEAD_NAME.get(ir_head_name):
            INTERACTION_RULES_BY_HEAD_NAME.update({ir_head_name: INTERACTION_RULES_BY_HEAD[ir_head]})
        else:
            INTERACTION_RULES_BY_HEAD_NAME[ir_head_name].extend(INTERACTION_RULES_BY_HEAD[ir_head])

    for ir_body in INTERACTION_RULES_BY_BODY.keys():
        ir_body_name = ir_body.split('(')[0]
        if not INTERACTION_RULES_BY_BODY_NAME.get(ir_body_name):
            INTERACTION_RULES_BY_BODY_NAME.update({ir_body_name: INTERACTION_RULES_BY_BODY[ir_body]})
        else:
            INTERACTION_RULES_BY_BODY_NAME[ir_body_name].extend(INTERACTION_RULES_BY_BODY[ir_body])
    print()


def create_explanation_keyword_dict(explanations):
    """
    This function creates the KEYWORDS_DICT which keys are keywords and values are row numbers
    :param explanations: list of explanations
    """
    english_stopwords = frozenset(stopwords.words('english'))

    for row, explanation in enumerate(explanations):

        if isinstance(explanation, str):

            keywords = re.split("\n| |\.|,|\(|\)|\"|-|:|”|“|’", explanation)
            for keyword in keywords:
                if keyword.lower() not in english_stopwords and len(keyword) > 1:
                    if keyword.lower() not in KEYWORDS_DICT.keys():
                        KEYWORDS_DICT.update({keyword.lower(): [row]})
                    else:
                        if row not in KEYWORDS_DICT[keyword.lower()]:
                            KEYWORDS_DICT[keyword.lower()].append(row)


def create_MITRE_technique_dict(techniques):

    """
    This function creates the TECHNIQUE_DICT : {technique: [row_number]}
    :param techniques: list of techniques
    """

    for row, explanation in enumerate(techniques):

        if isinstance(explanation, str):

            techniques = re.split("\n", explanation)
            for technique in techniques:
                if technique == '':
                    continue
                technique = technique.strip()
                if technique not in TECHNIQUE_DICT.keys():
                    TECHNIQUE_DICT.update({technique: [row]})
                else:
                    if row not in TECHNIQUE_DICT[technique]:
                        TECHNIQUE_DICT[technique].append(row)


def read_from_xml(path):

    file = minidom.parse(path)
    IRs = file.getElementsByTagName('SIR')

    # one specific item attribute
    for sir_num, IR in enumerate(IRs):

        ir_head = IR.attributes['Name'].value

        for ir_part in IR.childNodes:
            head_entities = []
            if ir_part.nodeType == minidom.Node.ELEMENT_NODE:
                if ir_part.localName == 'Parameters':
                    for parameter in ir_part.childNodes:
                        if parameter.nodeType == minidom.Node.ELEMENT_NODE and parameter.localName == 'Parameter':
                            head_entities.append(parameter.firstChild.data)

                    if len(head_entities) != 0:
                        ir_head = ir_head + '(' + ','.join(head_entities) + ')'

                elif ir_part.localName == 'Body':
                    if len(ir_part.childNodes) != 0:
                        PRIMITIVE_DERIVED_DICT.update({sir_num: 'derived'})
                    else:
                        PRIMITIVE_DERIVED_DICT.update({sir_num: 'primitive'})
                    predicates = []
                    for rule in ir_part.childNodes:
                        body_entities = []
                        body_rule = ''
                        if rule.nodeType == minidom.Node.ELEMENT_NODE:
                            body_rule = rule.attributes['Name'].value
                            for parameters in rule.childNodes:
                                body_entities = []
                                if parameters.nodeType == minidom.Node.TEXT_NODE:
                                    continue
                                if parameters.nodeType == minidom.Node.ELEMENT_NODE:
                                    if parameters.localName == 'Parameters':
                                        for parameter in parameters.childNodes:
                                            if parameter.nodeType == minidom.Node.ELEMENT_NODE and \
                                                    parameter.localName == 'Parameter':
                                                body_entities.append(parameter.firstChild.data)
                                        body_rule = body_rule + '(' + ','.join(body_entities) + ')'
                                        predicates.append((sir_num, body_rule))

                                    if not INTERACTION_RULES_BY_BODY.get(body_rule):
                                        INTERACTION_RULES_BY_BODY.update({body_rule: [(sir_num, ir_head)]})
                                        INTERACTION_RULES_BY_BODY_NAME.update({body_rule.split('(')[0]: [(sir_num, ir_head)]})

                                    elif (sir_num, ir_head) not in INTERACTION_RULES_BY_BODY[body_rule]:
                                        INTERACTION_RULES_BY_BODY[body_rule].append((sir_num, ir_head))
                                        INTERACTION_RULES_BY_BODY_NAME[body_rule.split('(')[0]].append((sir_num, ir_head))
                            if not INTERACTION_RULES_BY_HEAD.get(ir_head):
                                INTERACTION_RULES_BY_HEAD.update({ir_head: [(sir_num, predicates)]})
                                INTERACTION_RULES_BY_HEAD_NAME.update({ir_head.split('(')[0]: [(sir_num, predicates)]})
                            elif (sir_num, predicates) not in INTERACTION_RULES_BY_HEAD[ir_head]:
                                INTERACTION_RULES_BY_HEAD[ir_head].append((sir_num, predicates))
                                INTERACTION_RULES_BY_HEAD_NAME[ir_head.split('(')[0]].append((sir_num, predicates))
                            ROW_TO_IR.update({sir_num: ir_head})

                elif ir_part.localName == 'Description':
                    for description in ir_part.childNodes:
                        if description.nodeType == minidom.Node.TEXT_NODE:
                            explanations.update({sir_num: description.data})
                elif ir_part.localName == 'Technique':
                    for technique in ir_part.childNodes:
                        if technique.nodeType == minidom.Node.TEXT_NODE:
                            techniques.update({sir_num: technique.data})
    create_explanation_keyword_dict(explanations)
    create_MITRE_technique_dict(techniques)

# path = 'C:\\Users\\ADMIN\\Documents\\AttackGraphs\\Attack-GraphsProject\\input.xml'
# read_from_xml(path)
