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

    def help_search(self, lst, a_list):
        if a_list != None:
            if len(lst) != 0:
                tup_list = list()
                for row in lst:
                    if row not in a_list:
                        tup_list.append(row)
                for num_row in tup_list:
                    lst.remove(num_row)
            else:
                lst.update([num for num in a_list])
        return lst


    #function that do the search
    def search(self):
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
        # techjique
        if self.ids.technique.text != '':
            technique = b.search_by_technique(self.ids.technique.text)

        lst = set()
        #for sir head
        if sir_head != None:
            lst.update([tup[0] for tup in sir_head])
        #for rule
        lst = self.help_search(lst, rule)
        #for keyword in description
        lst = self.help_search(lst, description)
        #for technique
        lst = self.help_search(lst, technique)

        
        # self.create_datatables()
        print(lst)
        return lst


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