import re
from nltk.corpus import stopwords


def create_ir_dict(dfMulVAl):
    """
    This function creates a dictionary which  {interaction_rule_head: (row_number, ir_body)}
    This function also creates a dictionary with {interaction_rule_head: ((row_number, ir_head))}
    :param path: data frame of the given xlsx file
    """

    for row, IR in enumerate(dfMulVAl['Interaction Rules']):

        interaction_rules_by_head = {}
        interaction_rules_by_body = {}

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

                        interaction_rules_by_head.update({ir_head: predicates})

                        if predicate not in interaction_rules_by_body.keys():
                            interaction_rules_by_body.update({predicate: [(row, ir_head)]})
                        else:
                            if ir_head not in interaction_rules_by_body[predicate]:
                                interaction_rules_by_body[predicate] = [(row, ir_head)]
                            else:
                                interaction_rules_by_body[predicate].append(row, ir_head)

            else:
                interaction_rules_by_head.update({ir_head: None})

        else:
            interaction_rules_by_head.update({dfMulVAl['Predicate'][row]: None})

        return interaction_rules_by_head, interaction_rules_by_body


def create_ir_name_dict(interaction_rules_by_head, interaction_rules_by_body):
    """
    This function creates two dictionaries: interaction_rules_by_head_name, interaction_rules_by_body_name
    that would enable easier search by names of interaction rules
    :param interaction_rules_by_head, interaction_rules_by_body
    :return:
    """

    interaction_rules_by_head_name = {}
    interaction_rules_by_body_name = {}
    for ir_head in interaction_rules_by_head.keys():
        ir_head_name = ir_head.split('(')[0]
        interaction_rules_by_head_name.update({ir_head_name: interaction_rules_by_head[ir_head]})

    for ir_body in interaction_rules_by_body.keys():
        ir_body_name = ir_body.split('(')[0]
        interaction_rules_by_head_name.update({ir_body_name: interaction_rules_by_body[ir_body]})

    return interaction_rules_by_head_name, interaction_rules_by_body_name


def create_explanation_keyword_dict(dfMulVAl):
    """
    This function creates the KEYWORDS_DICT  {keywords : [row_number]}
    :param dfMulVAl: data frame of the given xlsx file
    """
    keywords_dict = {}
    english_stopwords = frozenset(stopwords.words('english'))

    for row, explanation in enumerate(dfMulVAl['Explanation']):

        if isinstance(explanation, str):

            keywords = re.split("\n| |\.|,|\(|\)|\"|-|:|”|“|’", explanation)
            for keyword in keywords:
                if keyword.lower() not in english_stopwords and len(keyword) > 1:
                    if keyword.lower() not in keywords_dict.keys():
                        keywords_dict.update({keyword.lower(): [row]})
                    else:
                        if row not in keywords_dict[keyword.lower()]:
                            keywords_dict[keyword.lower()].append(row)
        return keywords_dict


def create_MITRE_technique_dict(dfMulVAl):

    """
    This function creates the TECHNIQUE_DICT : {technique: [row_number]}
    :param dfMulVAl: data frame of the given xlsx file
    """

    for row, explanation in enumerate(dfMulVAl['MITRE Enterprise Technique']):

        technique_dict = {}
        if isinstance(explanation, str):

            techniques = re.split("\n", explanation)
            for technique in techniques:
                if technique == '':
                    continue
                technique = technique.strip()
                if technique not in technique_dict.keys():
                    technique_dict.update({technique: [row]})
                else:
                    if row not in technique_dict[technique]:
                        technique_dict[technique].append(row)
        return technique_dict

