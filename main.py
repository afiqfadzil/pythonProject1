# This is a sample Python script.
from kivy.app import App
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.config import Config
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

Builder.load_file('mainscreen.kv')
class LoginScreen(Widget):

    pass
    '''  def __init__(self, **kwargs):
       super(LoginScreen,self).__init__(**kwargs)
        self.add_widget(
            Button(
                text="Hello World",
                size_hint=(.20, .075),
                pos_hint={'center_x': .2, 'center_y': .10}))

        self.cols = 2
        self.add_widget(Label(text='Name',pos_hint={'center_x': .2, 'center_y': .75}))
        self.name = TextInput(multiline=False,size_hint=(.5,.07),pos_hint={'center_x': .5, 'center_y': .75})
        self.add_widget(self.name)
        self.add_widget(Label(text='BirthDate', pos_hint={'center_x': .2, 'center_y': .5}))
        self.birthdate = TextInput(multiline=False, size_hint=(.5, .07), pos_hint={'center_x': .5, 'center_y': .5})
        self.add_widget(self.birthdate)
        self.add_widget(Label(text='Height', pos_hint={'center_x': .2, 'center_y': .25}))
        self.ht = TextInput(multiline=False, size_hint=(.5, .07), pos_hint={'center_x': .5, 'center_y': .25})
        self.add_widget(self.ht)
'''


class Main(App):
    def build(self):
        Window.size = (620, 1024)
        return LoginScreen()
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Main().run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
