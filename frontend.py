from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
# import backend as b

kv = Builder.load_file("kivy.kv")


class grid(Widget):
    search_sir_head = ObjectProperty(None)
    search_rule = ObjectProperty(None)
    search_in_description = ObjectProperty(None)

    #function that do the search
    def search(self):
        # for key in dp.TECHNIQUE_DICT:
        #     print(key)
        pass


"""
This class inherited from App: should be like App
@:return instance of class that build the main window of the app
"""
class app(App):

    def build(self):
        Window.clearcolor = (240/250,240/250,240/250,240/250)
        # b.build()
        return grid()

"""
@:return main that started the application
"""
if __name__ == "__main__":
    app().run()