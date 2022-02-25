from kivy.app import App
from kivy.lang import Builder
import os.path
from kivy.uix.gridlayout import GridLayout
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
        self.xml_file_path = None
        self.technique_spinner = None
        self.page_layout = None
        self.input_layout = None
        self.data_table = None

    # def create_datatables(self):
    #     data_tables = MDDataTable(
    #         column_data=[
    #             ("Interaction Rule Set", dp(40)),
    #             ("Description", dp(40)),
    #             ("Technique", dp(40))
    #         ]
    #     )
    #     return data_tables

    def build(self):
        page_layout = GridLayout(cols=1)  # pos_hint ={'center_x':.43, 'center_y':.6})
        input_layout = GridLayout(cols=2)
        buttons_layout = GridLayout(cols=5, spacing=10, padding=[100, 30, 0, 0])
        # import_xml_layout = GridLayout(cols=2)

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
                                         values=['', 'Derived Environment Rule', 'Fact', 'T1078 - Valid Accounts',
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
        show_results.bind(on_press=self.perform_results)

        export_pddl = Button(text='export pddl', size_hint=(None, None), height=35, width=120, pos_hint=(500, 0.7),
                             background_color=(0.3, 0.4, 0.5, 0.7))
        export_pddl.bind(on_press=self.create_pddl)

        export_XML = Button(text='export XML', size_hint=(None, None), height=35, width=120, pos_hint=(500, 0.7),
                            background_color=(0.3, 0.4, 0.5, 0.7))
        export_XML.bind(on_press=self.create_XML)

        buttons_layout.add_widget(show_results)
        buttons_layout.add_widget(export_pddl)
        buttons_layout.add_widget(export_XML)

        self.xml_file_path = TextInput(multiline=True, size_hint=(0.1, None), height=35)
        buttons_layout.add_widget(self.xml_file_path)

        import_XML = Button(text='import file', size_hint=(None, None), height=35, width=120, pos_hint=(500, 0.7),
                            background_color=(0.3, 0.4, 0.5, 0.7))
        import_XML.bind(on_press=self.read_from_file)
        buttons_layout.add_widget(import_XML)

        self.data_table = MDDataTable(
            column_data=[
                ("Description", dp(50)),
                ("Interaction Rule Set", dp(50)),
                ("Technique", dp(50))
            ],
            use_pagination=True,
            rows_num=2
        )
        page_layout.add_widget(input_layout)
        page_layout.add_widget(buttons_layout)
        page_layout.add_widget(self.data_table)
        b.build('MulVAL to MITRE-for IR Manager.xlsx')
        return page_layout

    def perform_results(self, instance):

        results = b.search(self.search_sir_head.text, self.search_rule.text, self.search_in_description.text,
                           self.technique_spinner.text)[0]
        # print(results)
        self.data_table.row_data = results

    def create_XML(self, instance):

        rows = []
        res = b.search(self.search_sir_head.text, self.search_rule.text, self.search_in_description.text,
                             self.technique_spinner.text)
        if res is not None:
            rows = res[1]
        b.create_xml(rows)

    def create_pddl(self, instance):

        rows = []
        res = b.search(self.search_sir_head.text, self.search_rule.text, self.search_in_description.text,
                             self.technique_spinner.text)
        if res is not None:
            rows = res[1]
        b.create_pddl(rows)

    def read_from_file(self, instance):

        path = self.xml_file_path.text
        if os.path.isfile(path):
            if path[-4:] == '.xml':
                b.empty_dicts()
                b.read_from_xml(path)
            elif path[-5:] == '.xlsx':
                b.empty_dicts()
                b.build(path)


"""
@:return main that started the application
"""
if __name__ == "__main__":
    grid().run()
