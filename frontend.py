from kivy.app import App
from kivy.lang import Builder
import os.path
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.properties import ObjectProperty, ListProperty
from kivy.core.window import Window
import backend as b
from kivy.uix.popup import Popup
import DataPreperation as DataPrep
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen

kv = Builder.load_file("kivy.kv")
Window.clearcolor = (240 / 250, 240 / 250, 240 / 250, 240 / 250)
Window.size = (1000, 500)

class app(App):

    def build(self):
        b.build('MulVAL to MITRE-for IR Manager.xlsx')
        return grid()


class Popups(FloatLayout):
    res_data = ListProperty([])
    pass


class grid(Widget):

    data_tables = None
    search_sir_head = ObjectProperty(None)
    search_rule = ObjectProperty(None)
    search_in_description = ObjectProperty(None)
    technique_spinner = None
    xml_file_path = None
    page_layout = None
    input_layout = None

    def show_popup(self):
        show = Popups()
        pop_window = Popup(title="Results", content=show, size_hint=(0.9, 1))
        pop_window.open()

    def perform_results(self):

        results = b.search(self.search_sir_head.text, self.search_rule.text, self.search_in_description.text,
                           self.technique_spinner.text)[0]
        lst = []
        lst.extend([{'text': 'Description:\n'}])
        lst.extend([{'text': 'Interaction Rule Set:\n'}])
        lst.extend([{'text': 'Techniques:\n'}])
        for res in results:
            for type, line in enumerate(res):
                s = ''
                for word_count, w in enumerate(line.split(), 1):

                    if type == 1 and word_count % 3 == 0:
                        s += '\n' + w
                    elif type != 1 and word_count % 4 == 0:
                        s += '\n' + w
                    else:
                        s += ' ' + w
                lst.extend([{'text': s[1:]}])
        Popups.res_data = lst
        print(results)
        # self.data_table.row_data = results
        self.show_popup()

    def create_XML(self):

        rows = []
        res = b.search(self.search_sir_head.text, self.search_rule.text, self.search_in_description.text,
                             self.technique_spinner.text)
        if res is not None:
            rows = res[1]
        b.create_xml(rows)

    def create_pddl(self):

        rows = []
        res = b.search(self.search_sir_head.text, self.search_rule.text, self.search_in_description.text,
                       self.technique_spinner.text)
        if res is not None:
            rows = res[1]
        b.create_pddl(rows)

    def read_from_file(self):

        path = self.xml_file_path.text
        if os.path.isfile(path):
            if path[-4:] == '.xml':
                b.empty_dicts()
                b.read_from_xml(path)
            elif path[-5:] == '.xlsx':
                b.empty_dicts()
                b.build(path)


"""
@:return main that started the application.
"""
if __name__ == "__main__":
    app().run()
