# This is a sample Python script.
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import platform
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

Builder.load_file("my.kv")

def calculate(self, ht, nt, pre_score):
    # Calculate Seat Height
    seat_height = 0.25 * ht - 1
    print(seat_height)
    BL = 1
    OL = 0
    test_counter = 3
    test_array = [[], [], [0.5, 0], [0.625, 0], [0.75, 0], [0.875, 0], [1.0, 0], [0.375, 1], [0.5, 1],
                  [0.625, 1], [0.75, 1], [0.875, 1], [1.0, 1], [1.125, 0], [1.25, 0]]
    for test_counter in range(3):
        print(test_array[nt])
        nt = nt + 2

    '''


    nt = 2 [0.5H , 0]
    nt = 3 [0.625 ,0]
    nt = 4 [0.75, 0]
    nt = 5 [0.875 ,0]
    nt = 6 [1.0,  0]
    nt = 7 [0.375 ,1]
    nt = 8 [0.5, 1]
    nt = 9 [0.625 ,1]
    nt = 10 [0.75, 1]
    nt = 11 [0.875, 1]
    nt = 12 [1.0, 1]
    nt = 13 [1.125, 0]
    nt = 14 [1.25, 0]





    '''

class MainWindow(Screen):
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
        ht = int(ht_text)
        if age >= 15:
            nt = 2
            pre_score = 95
        elif age >= 35:
            nt = 4
            pre_score = 85
        elif age >= 35:
            nt = 6
            pre_score = 75
        elif age >= 81:
            nt = 8
            pre_score = 65
        elif age < 15 or age > 150:
            main_screen.ids.error_label_main.text = "年齢にエラー (15~150)"

            return 0

        calculate(self, ht, nt, pre_score)
        self.manager.current = "test"
        self.manager.transition.direction = "left"
    pass



class TestWindow(Screen):
    pass








class ResultWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class MyMainApp(App):
    def build(self):
        return WindowManager()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    MyMainApp().run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
