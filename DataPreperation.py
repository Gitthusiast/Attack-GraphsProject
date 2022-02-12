import pandas as pd
import re
from nltk.corpus import stopwords

INTERACTION_RULES_BY_HEAD = {}
INTERACTION_RULES_BY_HEAD_NAME = {}
INTERACTION_RULES_BY_BODY = {}
KEYWORDS_DICT = {}
TECHNIQUE_DICT = {}


def create_ir_dict(dfMulVAl):
    """
    This function creates a dictionary which  {interaction_rule_head: (row_number, ir_body)}
    This function also creates a dictionary with {interaction_rule_head: ((row_number, ir_head))}
    :param path: data frame of the given xlsx file
    """

    for row, IR in enumerate(dfMulVAl['Interaction Rules']):

        if isinstance(IR, str):

            splited_ir = IR.split(":-")

            if len(splited_ir[0].split('\n')) >= 2 and splited_ir[0].split('\n')[0][0] == '%':

                ir_head = splited_ir[0].split('\n')[1]
            else:
                if splited_ir[0][-1] == ' ':
                    ir_head = splited_ir[0][:-1]
                else:
                    ir_head = splited_ir[0]

            if len(splited_ir) >= 2:  # check body

                ir_body = re.split('\n', splited_ir[1])
                predicates = []
                for predicate in ir_body:

                    if len(predicate) >= 3 and predicate[1] != '%' and predicate[2] != '%':
                        if predicate[-1] == "," or predicate[-1] == '.':
                            predicate = predicate[:-1]
                        predicate = predicate.strip()
                        predicates.append((row, predicate))

                        INTERACTION_RULES_BY_HEAD.update({ir_head: predicates})

                        if predicate not in INTERACTION_RULES_BY_BODY.keys():
                            INTERACTION_RULES_BY_BODY.update({predicate: [(row, ir_head)]})
                        else:
                            if ir_head not in INTERACTION_RULES_BY_BODY[predicate]:
                                INTERACTION_RULES_BY_BODY[predicate] = [(row, ir_head)]
                            else:
                                INTERACTION_RULES_BY_BODY[predicate].append(row, ir_head)

            else:
                INTERACTION_RULES_BY_HEAD.update({ir_head: None})

        else:
            INTERACTION_RULES_BY_HEAD.update({dfMulVAl['Predicate'][row]: None})

def create_ir_head_name_dict():

    for ir_head in INTERACTION_RULES_BY_HEAD.keys():
        ir_head_name = ir_head.split('(')[0]
        INTERACTION_RULES_BY_HEAD_NAME.update({ir_head_name: INTERACTION_RULES_BY_HEAD[ir_head]})

def create_explanation_keyword_dict(dfMulVAl):
    """
    This function creates the KEYWORDS_DICT which keys are keywords and values are row numbers
    :param dfMulVAl: data frame of the given xlsx file
    """

    english_stopwords = frozenset(stopwords.words('english'))

    for row, explanation in enumerate(dfMulVAl['Explanation']):

        if isinstance(explanation, str):

            keywords = re.split("\n| |\.|,|\(|\)|\"|-|:|”|“|’", explanation)
            for keyword in keywords:
                if keyword.lower() not in english_stopwords and len(keyword) > 1:
                    if keyword.lower() not in KEYWORDS_DICT.keys():
                        KEYWORDS_DICT.update({keyword.lower(): [row]})
                    else:
                        if row not in KEYWORDS_DICT[keyword.lower()]:
                            KEYWORDS_DICT[keyword.lower()].append(row)


def create_MITRE_technique_dict(dfMulVAl):

    """
    This function creates the TECHNIQUE_DICT : {technique: row_number}
    :param dfMulVAl: data frame of the given xlsx file
    """

    for row, explanation in enumerate(dfMulVAl['MITRE Enterprise Technique']):

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


path = 'C:\\Users\\ADMIN\\Documents\\AttackGraphs\\Attack-GraphsProject\\MulVAL to MITRE-for IR Manager.xlsx'
dfMulVAl = pd.read_excel(path)
create_ir_dict(dfMulVAl)
create_ir_head_name_dict()
print(INTERACTION_RULES_BY_BODY.keys())
