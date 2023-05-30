import socket
from kivy.uix.label import Label
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import platform
# from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.slider import Slider
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.uix.checkbox import CheckBox
from client import *
from threading import Thread
import threading

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# test_array [SeatHeight,OneL = 0/BothL = 1 , Score , Locomotion Age]
test_array = [[], [0.5, 0, 100, 16.00], [0.5, 0, 95, 27.95], [0.625, 0, 90, 39.9],
              [0.75, 0, 85, 51.85], [0.875, 0, 80, 63.8], [1.0, 0, 75, 75.75], [0.375, 1, 70, 87.7],
              [0.5, 1, 65, 99.65], [0.625, 1, 60, 111.6], [0.75, 1, 55, 123.55], [0.875, 1, 50, 135.5],
              [1.0, 1, 45, 147.45], [1.125, 0, 40, 159.4], [1.25, 35, 171.35]]
Builder.load_file("my.kv")
Config.set('graphics', 'resizable', '0')  # 0 being off 1 being on as in true/false
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '1000')
Config.write()
C = ["Error Check", "素晴らしい基礎運動力です",
     "良い基礎運動力です",
     "基礎運動力平均より低い、筋肉バランス感覚のトレーニングをしましょう",
     "ロコモシンドロームの傾向がありロコモ検診してください",
     "基礎運動能力がい著しく低下、ちかくの整形外科病院で受診してください"]


class TitleWindow(Screen):  # connection to server may start here

    def __init__(self, **kwargs):
        super(TitleWindow, self).__init__(**kwargs)

        self.sock = MySocket()
        Thread(target=self.get_data).start()
        Thread(target=self.send_data).start()
        self.text = 0
        self.send_text = 0

    def get_data(self):
        while True:
            self.text = self.sock.get_data()
            print(self.text.decode('utf-8'))

    def send_data(self):
        while True:
            seat = MainWindow.seat_height
            self.sock.send_data(seat)
            break

    def next_screen(self):
        self.manager.current = "main"
        self.manager.transition.direction = "up"

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

        age_text = main_screen.ids.age.text

        test1_screen.ids.test2_label.text = ht_text

        # "Not Implemented yet"
        # Input will Fail if Blank Fields, Age is not a number, Age > 150 , Height > 2.50M (Done)
        # Address API
        # Radio Button for Gender
        # Space or Tab will be neglected
        if ht_text == "" or str(ht_text.isnumeric()) == "False":
            main_screen.ids.error_label_main.text = "身長を入力してください！"
            return 0
        if age_text == "" or str(age_text.isnumeric()) == "False":
            main_screen.ids.error_label_main.text = "年齢を入力してください！"
            return 0

        MainWindow.age = int(age_text)
        MainWindow.ht = int(ht_text)
        MainWindow.seat_height = 0.25 * MainWindow.ht - 1
        if MainWindow.age < 15 or MainWindow.age > 150:
            main_screen.ids.error_label_main.text = "年齢にエラー (15~150)"
            return 0
        elif MainWindow.age >= 81:
            MainWindow.nt = 8
            pre_score = 65
        elif MainWindow.age >= 35:
            MainWindow.nt = 6
            pre_score = 75
        elif MainWindow.age >= 35:
            MainWindow.nt = 4
            pre_score = 85

        elif MainWindow.age >= 15:
            MainWindow.nt = 2
            pre_score = 95
        print(MainWindow.nt)
        self.manager.current = "loading"
        self.manager.transition.direction = "left"
        self.manager.get_screen(
            "test").ids.test2_label.text = f'Test{TestWindow.c + 1}/3,Seat Height is {MainWindow.seat_height}'
        seat=MainWindow.seat_height
        a = TitleWindow()
        a.send_data(seat)

        main_screen.ids.ht.text = ""
        main_screen.ids.age.text = ""

        pass


# Have to add the picture on the posture + what is やり直しmeans
class TestWindow(Screen):
    # R = MainWindow.age - test_array[MainWindow.nt][3]

    def __init__(self, **kw):
        super().__init__(**kw)
        TestWindow.c = 0
        TestWindow.score = 0
        self.prev = 0
        self.rating = 0
        self.cnt = 0

    def rating_func(self):
        self.rating = MainWindow.age - test_array[MainWindow.nt][3]
        if TestWindow.c == 3:

            if int(self.rating) > 20:
                self.cnt = 1
                print(C[self.cnt])
                pass

            elif int(self.rating) > 0:
                self.cnt = 2
                print(C[self.cnt])
                pass

            elif int(self.rating) > (-20):
                self.cnt = 3
                print(C[self.cnt])
                pass

            elif int(self.rating) > (-30):
                self.cnt = 4
                print(C[self.cnt])
                pass

            else:
                self.cnt = 5
                print(C[self.cnt])
                pass

            result_screen = self.manager.get_screen("result")
            result_screen.ids.result_label_comment.text = C[self.cnt]
            result_screen.ids.result_label_age.text = f'貴殿の年齢は :{(str(MainWindow.age))}'
            result_screen.ids.result_label_rage.text = f'貴殿のロコモ年齢は :{str(test_array[MainWindow.nt][3])}'

            print(self.rating)
            print(MainWindow.age)
            print(test_array[MainWindow.nt][3])

        pass

    def next_screen(self):
        if TestWindow.c == 3:
            self.manager.current = "result"
            self.manager.transition.direction = "left"
            TestWindow.c = 0

    def passed(self):
        if TestWindow.c < 2:
            if TestWindow.c == 0:  # Pass
                # Send Data to python to adjust Seat Height
                MainWindow.nt = MainWindow.nt - 2
                # if nt score is lower than 1 set MainWindow.nt == 1

                if MainWindow.nt < 1:
                    MainWindow.nt = 1


            elif TestWindow.c == 1 and int(self.prev) == 0:  # PassPass
                MainWindow.nt = MainWindow.nt - 2
                if MainWindow.nt < 1:
                    MainWindow.nt = 1


            elif TestWindow.c == 1 and int(self.prev) == 1:  # FailPass
                MainWindow.nt = MainWindow.nt - 1
                if MainWindow.nt < 1:
                    MainWindow.nt = 1
            else:
                pass

        if TestWindow.c == 2:  # FinalMarking
            self.rating = float(test_array[MainWindow.nt][3]) - float(MainWindow.age)
            print(self.rating)

        self.prev = 0
        TestWindow.c = TestWindow.c + 1
        self.manager.get_screen("test").ids.test2_label.text = f'Test{TestWindow.c}/3,You Passed!'

        print(MainWindow.nt)

        return MainWindow.nt

    def failed(self):
        if TestWindow.c < 2:

            if TestWindow.c == 0:  # Pass
                MainWindow.nt = MainWindow.nt + 2
                if MainWindow.nt > 14:
                    MainWindow.nt = 14

            elif TestWindow.c == 1 and int(self.prev) == 1:  # FailFail
                MainWindow.nt = MainWindow.nt + 2
                if MainWindow.nt > 14:
                    MainWindow.nt = 14

                print("FailFail")


            elif TestWindow.c == 1 and int(self.prev) == 0:  # PassFail
                MainWindow.nt = MainWindow.nt + 1
                if MainWindow.nt > 14:
                    MainWindow.nt = 14
                print("PassFail")

        if TestWindow.c == 2:  # FinalMarking
            MainWindow.nt = MainWindow.nt + 1
            self.rating = float(MainWindow.age) - float(test_array[MainWindow.nt][3])

            print(self.rating)
            pass

        self.prev = 1
        TestWindow.c = TestWindow.c + 1
        self.manager.get_screen("test").ids.test2_label.text = f'Test{TestWindow.c}/3,You Failed!'

        return MainWindow.nt

    pass  ##


class LoadingWindow(Screen):  # incomplete
    pass


class MaintenanceWindow(Screen):
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
