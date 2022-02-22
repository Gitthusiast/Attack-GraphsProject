from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
import backend as b
import DataPreperation as DataPrep
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.screen import Screen

kv = Builder.load_file("kivy.kv")


class grid(Widget):
    search_sir_head = ObjectProperty(None)
    search_rule = ObjectProperty(None)
    search_in_description = ObjectProperty(None)

    def choose_technique(self, value):
        self.ids.technique.text = value

    def create_datatables(self):
        table = MDDataTable(
            column_data=[
                ("Interaction Rule Set", dp(30)),
                ("Description", dp(30)),
                ("Technique", dp(30))
        ]
    )

    def help_search(self, rows, a_list):
        if a_list != None:
            if len(rows) != 0:
                tup_list = list()
                for row in rows:
                    if row not in a_list:
                        tup_list.append(row)
                for num_row in tup_list:
                    rows.remove(num_row)
            else:
                print("a_list: ", a_list)
                print("rows", rows)
                rows = set([tup[0] if type(tup) != int else tup for tup in a_list])
        return rows


    #function that do the search
    def search(self):
        #search for the common rows
        # sir head
        sir_head, rule, description, technique = None, None, None, None
        if self.search_sir_head.text != '':
            sir_head = b.search_ir_by_head(self.search_sir_head.text)
        # rule
        if self.search_rule.text != '':
            rule = b.search_by_rule_name(self.search_rule.text)
        # description
        if self.search_in_description.text != '':
            description = b.search_by_keywods_in_description(self.search_in_description.text)
        # technique
        if self.ids.technique.text != '':
            technique = b.search_by_technique(self.ids.technique.text)

        rows = set()
        #for sir head
        if sir_head != None:
            rows.update([tup[0] for tup in sir_head])
        #for rule
        rows = self.help_search(rows, rule)
        #for keyword in description
        rows = self.help_search(rows, description)
        #for technique
        rows = self.help_search(rows, technique)

        res = list()
        for row in rows:
            expla = DataPrep.explanations.get(row)
            if expla == None:
                expla = ""
            ir_head = DataPrep.ROW_TO_IR.get(row)
            ir = ""
            if ir_head == None:
                ir = ""
            else:
                ir = ir_head + ":- "
                ir_bodies = b.search_ir_by_head(ir_head)
                for ir_body in ir_bodies:
                    if len(ir_bodies) != 1:
                        ir += ir_body + ", "
                if ir != None:
                    ir = ir[:-1]
                    ir += '.'
            techni = DataPrep.techniques.get(row)
            if techni == None:
                techni = ""
            res.append((expla, ir, techni))
        # self.create_datatables()
        print(res)
        return res


class app(App):
    """
    This class inherited from App: should be like App
    @:return instance of class that build the main window of the app
    """

    def build(self):
        Window.clearcolor = (240/250,240/250,240/250,240/250)
        b.build()
        return grid()

"""
@:return main that started the application
"""
if __name__ == "__main__":
    app().run()