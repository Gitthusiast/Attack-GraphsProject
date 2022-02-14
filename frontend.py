from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

kv = Builder.load_file("kivy.kv")

class grid(Widget):
    search_for = ObjectProperty(None)

    #function that do the search
    def fun_button(self):
        pass


"""
This class inherited from App: should be like App
@:return instance of class that build the main window of the app
"""
class app(App):

    def build(self):
        return grid()

"""
@:return main that started the application
"""
if __name__ == "__main__":
    app().run()