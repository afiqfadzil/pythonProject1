# This is a sample Python script.
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import platform
# from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
test_array = [[], [], [0.5, 0], [0.625, 0], [0.75, 0], [0.875, 0], [1.0, 0], [0.375, 1], [0.5, 1],
              [0.625, 1], [0.75, 1], [0.875, 1], [1.0, 1], [1.125, 0], [1.25, 0]]
Builder.load_file("my.kv")
Config.set('graphics', 'resizable', '0')  # 0 being off 1 being on as in true/false
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '1000')
Config.write()
seat_height = 0


class ControlPanel(object):

    def calculate(self):
        # Calculate Seat Height
        self.seat_height = 0.25 * self.ht - 1
        print(self.seat_height)
        # BothLeg = 1
        # OneLeg = 0\
        return self.ht, self.nt, self.seat_height

    def results(self):
        print("seat height is:", test_array[self.nt])

        return 0

    pass


class MainWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        MainWindow.ht = 0
        MainWindow.nt = 0
        MainWindow.age = 0
        MainWindow.pre_score = 0
        MainWindow.seat_height = 0

    def data_call(self):

        test1_screen = self.manager.get_screen("test")
        main_screen = self.manager.get_screen("main")

        # Collect all the data from the Text Input Field in "my.kv"

        ht_text = main_screen.ids.ht.text
        address_text = main_screen.ids.address.text
        age_text = main_screen.ids.age.text
        gender_text = main_screen.ids.gender.text

        test1_screen.ids.test2_label.text = ht_text

        # "Not Implemented"
        # Input will Fail if Blank Fields, Age is not a number, Age > 150 , Height > 2.50M
        # Address API
        # Radio Button for Gender
        if ht_text == "" or str(ht_text.isnumeric()) == "False":
            main_screen.ids.error_label_main.text = "身長を入力してください！"
            return 0
        if age_text == "" or str(age_text.isnumeric()) == "False":
            main_screen.ids.error_label_main.text = "年齢を入力してください！"
            return 0

        age = int(age_text)
        MainWindow.ht = int(ht_text)
        if age >= 15:
            MainWindow.nt = 2
            pre_score = 95
        elif age >= 35:
            MainWindow.nt = 4
            pre_score = 85
        elif age >= 35:
            MainWindow.nt = 6
            pre_score = 75
        elif age >= 81:
            MainWindow.nt = 8
            pre_score = 65
        elif age < 15 or age > 150:
            main_screen.ids.error_label_main.text = "年齢にエラー (15~150)"

            return 0

        self.manager.current = "test"
        self.manager.transition.direction = "left"



    pass


class TestWindow(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        MainWindow.nt = 0

    def passed(self):
        # Send Data to python to adjust Seat Height
        MainWindow.nt = MainWindow.nt + 2
        print(test_array[MainWindow.nt])
        return MainWindow.nt

    def failed(self):
        MainWindow.nt = self.nt - 2
        return self.nt

    pass


class ResultWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class MyMainApp(App):
    def build(self):
        if platform == 'android' or platform == 'ios':
            Window.maximize()
        else:
            Window.size = (620, 1024)

        return WindowManager()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    MyMainApp().run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
