import pandas as pd
import re

INTERACTION_RULES = {}


def create_ir_dict(dfMulVAl):
    """
    This function creates a dictionary which keys are tuples of (row_number, interaction_rule_head)
     and values are lists of ir bodies
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
                        predicates.append(predicate.strip())
                INTERACTION_RULES.update({(row, ir_head): predicates})
            else:
                INTERACTION_RULES.update({(row, ir_head): None})
        else:
            INTERACTION_RULES.update({(row, dfMulVAl['Predicate'][row]): None})


path = 'C:\\Users\\ADMIN\\Documents\\AttackGraphs\\Attack-GraphsProject\\MulVAL to MITRE-for IR Manager.xlsx'
dfMulVAl = pd.create_ir_dict(path)

