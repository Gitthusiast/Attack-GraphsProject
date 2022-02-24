from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from kivy.core.window import Window
import backend as b
import DataPreperation as DataPrep
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.screen import Screen


class grid(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_tables = None
        self.search_sir_head = ObjectProperty(None)
        self.search_rule = ObjectProperty(None)
        self.search_in_description = ObjectProperty(None)
        self.xml_file_path = ObjectProperty(None)
        self.technique_spinner = None

    def build(self):
        page_layout = GridLayout(cols=1)
        input_layout = GridLayout(cols=2)
        buttons_layout = GridLayout(cols=3, spacing=10, padding=[200, 30, 0, 0])
        import_xml_layout = GridLayout(cols=2)

        sir_search_label = Label(text='[color=ff000] Search by SIR head name: [/color]', markup=True)
        input_layout.add_widget(sir_search_label)
        self.search_sir_head = TextInput(multiline=True, size_hint=(0.7, None), height=35)
        input_layout.add_widget(self.search_sir_head)

        rulename_search_label = Label(text='[color=ff000] Search by rule name: [/color]', markup=True)
        input_layout.add_widget(rulename_search_label)
        self.search_rule = TextInput(multiline=False, size_hint=(0.7, None), height=35)
        input_layout.add_widget(self.search_rule)

        desc_search_label = Label(text='[color=ff000] Search by keywords in description: [/color]', markup=True)
        input_layout.add_widget(desc_search_label)
        self.search_in_description = TextInput(multiline=True, size_hint=(0.7, None), height=35)
        input_layout.add_widget(self.search_in_description)

        technique_search_label = Label(text='[color=ff000] Search by technique name:', markup=True)
        input_layout.add_widget(technique_search_label)
        self.technique_spinner = Spinner(text='technique', size_hint=(0.7, None), height=35,
                                         values=['Derived Environment Rule', 'Fact', 'T1078 - Valid Accounts',
                                                 'Exploitation for Client Execution (DT)',
                                                 'T1068 - Exploitation for Privilege Escalation (NB)',
                                                 'Exploitation for Privilege Escalation (DT)',
                                                 'T1190 - Exploit Public-Facing Application (NB)',
                                                 'Abuse Elevation Control Mechanism (DT)',
                                                 'T1078 - Valid Accounts (NB)',
                                                 'T1203 - Exploitation for Client Execution (NB)',
                                                 'T1204 - User Execution (NB)', 'T1566 - Phishing (NB)',
                                                 'T1005 - Data from Local System (NB)',
                                                 'T1003 - OS Credential Dumping (NB)', 'Data from Local System (DT)',
                                                 'Building Block (NB)', 'Data from Network Shared Drive (DT)',
                                                 'Data from Network Shared Drive',
                                                 'Exploitation for Credential Access (DT)',
                                                 'T1003- OS Credential Dumping (NB)',
                                                 'T1558 - Steal or Forge Kerberos Tickets (NB)',
                                                 'TA1078 - Valid Account (NB)', 'Building Block', 'Man-in-the-Middle',
                                                 'Endpoint Denial of Service', 'Network Denial of Service',
                                                 'Password Policy Discovery', 'Network Sniffing (NB)',
                                                 'Network Sniffing', 'T1129 - Shared Modules (NB)',
                                                 'T1203 - Exploitation for Client Execution', 'T1204 - User Execution',
                                                 'Exploitation for Privilege Escalation',
                                                 'T1021 - Remote Services (NB)',
                                                 'T1563 - Remote Service Sessions Hijacking (NB)',
                                                 'Building Block (DT)', 'T1569 - System Services (NB)',
                                                 'T1055 - Process injection', 'T1565 - Data Manipulation',
                                                 'External Remote Services (NB)', 'Drive-by Compromise (NB)',
                                                 'Remote Service (NB)', 'Steal Application Access Token (NB)',
                                                 'Steal or Forge Kerberos Tickets (NB)',
                                                 'Command and Scripting Interpreter',
                                                 'Exploitation of Remote Services?', 'Remote Services? (DT)',
                                                 'Process Injection? (NB)', 'Exfiltration Over Alternative Protocol',
                                                 'OS Credential Dumping (NB)', 'Data Manipulation',
                                                 'Exploitation for Client Execution', 'Valid Accounts',
                                                 'User Execution (NB)', 'Exploit Public-Facing Application (NB)',
                                                 'Valid Accounts (DT)', 'Exploitation for Client Execution (NB)',
                                                 'Data from Local System', 'Credentials from Password Stores',
                                                 'Credentials from Password Stores (DT)',
                                                 "(Specific to 3d printing, doesn't exist in MITRE yet)",
                                                 'Exfiltration Over Other Network Medium',
                                                 'File and Directory Discovery (DT)',
                                                 'Exfiltration Over Physical Medium', 'Derived Environment Rule (NB)',
                                                 'Fact & Derived Environment Rule', 'Disk Wipe'])
        input_layout.add_widget(self.technique_spinner)

        show_results = \
            Button(text='Show results', size_hint=(None, None), height=35, width=120, pos_hint=(500, 0.7),
                   background_color=(0.3, 0.4, 0.5, 0.7))
        show_results.bind(on_press=self.search)

        export_pddl = Button(text='export pddl', size_hint=(None, None), height=35, width=120, pos_hint=(500, 0.7),
                             background_color=(0.3, 0.4, 0.5, 0.7))

        export_XML = Button(text='export XML', size_hint=(None, None), height=35, width=120, pos_hint=(500, 0.7),
                            background_color=(0.3, 0.4, 0.5, 0.7))

        buttons_layout.add_widget(show_results)
        buttons_layout.add_widget(export_pddl)
        buttons_layout.add_widget(export_XML)

        self.xml_file_path = TextInput(multiline=True, size_hint=(0.1, None), height=35)
        import_xml_layout.add_widget(self.xml_file_path)

        import_XML = Button(text='import XML', size_hint=(None, None), height=35, width=120, pos_hint=(500, 0.7),
                            background_color=(0.3, 0.4, 0.5, 0.7))
        import_xml_layout.add_widget(import_XML)

        self.data_tables = MDDataTable(
            column_data=[
                ("Interaction Rule Set", dp(40)),
                ("Description", dp(40)),
                ("Technique", dp(40))
            ]
        )

        page_layout.add_widget(input_layout)
        page_layout.add_widget(buttons_layout)
        page_layout.add_widget(import_xml_layout)
        page_layout.add_widget(self.data_tables)
        # screen.add_widget(self.data_tables)
        b.build()
        return page_layout

    def help_search(self, lst, a_list):
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

    # function that do the search
    def search(self, instance):
        # sir head
        sir_head, rule, description, technique = None, None, None, None
        if self.search_sir_head.text != '':
            sir_head = b.search_ir_by_head_name(self.search_sir_head.text)
        # rule
        if self.search_rule.text != '':
            rule = b.search_by_rule_name(self.search_rule.text)
        # description
        if self.search_in_description.text != '':
            description = b.search_by_keywods_in_description(self.search_in_description.text)
        # technique
        if self.technique_spinner.text != '':
            technique = b.search_by_technique(self.technique_spinner.text)

        rows = set()
        # for sir head
        if sir_head != None:
            rows.update([tup[0] for tup in sir_head])
        # for rule
        rows = self.help_search(rows, rule)
        # for keyword in description
        rows = self.help_search(rows, description)
        # for technique
        rows = self.help_search(rows, technique)
        rows = sorted(rows)

        res = list()
        for row in rows:
            expla = DataPrep.explanations.get(row)
            # if expla == None:
            #     expla = ""
            ir_head = DataPrep.ROW_TO_IR.get(row)
            ir = ""
            if ir_head == None:
                ir = ""
            else:
                ir = ir_head + ":- "
                ir_bodies = b.search_ir_by_head(ir_head)
                for ir_body in ir_bodies:
                    if ir_body[1] == None:
                        break
                    elif len(ir_body[1]) != 1:
                        ir += ir_body[1][1][1] + ", "
                if ir != "":
                    ir = ir[:-2]
                    ir += '.'
            techni = DataPrep.techniques.get(row)
            if techni == None:
                techni = ""
            res.append((expla, ir, techni))
        # self.create_datatables()
        print(res)
        return res


"""
@:return main that started the application
"""
if __name__ == "__main__":
    grid().run()
