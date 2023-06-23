import socket
from kivy.uix.label import Label
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import platform
from kivymd.app import MDApp
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
from time import sleep

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# test_array [SeatHeight,OneL = 0/BothL = 1 , Score , Locomotion Age]
test_array = [[], [0.5, "One Leg", 100, 16.00], [0.5, "One Leg", 95, 27.95], [0.625, "One Leg", 90, 39.9],
              [0.75, "One Leg", 85, 51.85], [0.875, "One Leg", 80, 63.8], [1.0, "One Leg", 75, 75.75],
              [0.375, "Two Legs", 70, 87.7],
              [0.5, "Two Legs", 65, 99.65], [0.625, "Two Legs", 60, 111.6], [0.75, "Two Legs", 55, 123.55],
              [0.875, "Two Legs", 50, 135.5],
              [1.0, "Two Legs", 45, 147.45], [1.125, "Two Legs", 40, 159.4], [1.25, "Two Legs", 35, 171.35]]
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


# Task
# server is included with the relay module program (サーバーとリレーモジュールのプログラムは一緒)
# configure so that the program do not crash if not connected to a server
class TitleWindow(Screen):  # connection to server may start here
    def __init__(self, **kwargs):
        super(TitleWindow, self).__init__(**kwargs)
        self.sock = None
        self.text = 0
        self.send_text = 0

    def next_screen(self):
        self.manager.current = "main"
        self.manager.transition.direction = "up"

    def connection(self):
        try:
            self.sock = MySocket()
            print(self.sock)
            Thread(target=self.send_data).start()
            Thread(target=self.get_data).start()
            self.manager.current = "main"
            self.manager.transition.direction = "left"
        except Exception as e:
            print(str(e))
            sleep(0.1)
            self.manager.current = "connect"
            self.manager.transition.direction = "left"

    def get_data(self):
        while True:
            self.text = self.sock.get_data()
            print(self.text.decode('utf-8'))
            return self.text

    def send_data(self, msg=None):
        while True:
            # msg = input()
            self.sock.send_data(msg)
            break


class ControlScreen(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class MainWindow(Screen):

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        MainWindow.ht = 0
        MainWindow.nt = 0
        MainWindow.age = 0
        MainWindow.pre_score = 0
        MainWindow.seat_height = 0  # the one that will be sent to the chair
        MainWindow.std_height = 0  # Capital H

        self.seat = 0

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
        MainWindow.std_height = 0.25 * MainWindow.ht - 1
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
        MainWindow.seat_height = int(MainWindow.std_height * test_array[MainWindow.nt][0])
        self.manager.current = "loading"
        self.manager.transition.direction = "left"
        self.manager.get_screen(
            "test").ids.test2_label.text = f'seat Height is {MainWindow.seat_height} and do it with {test_array[MainWindow.nt][1]}'

        self.seat = MainWindow.seat_height
        control = self.manager.get_screen('title')
        control.send_data(str(self.seat))
        main_screen.ids.ht.text = ""
        main_screen.ids.age.text = ""

        pass


# Have to add the picture on the posture + what is やり直しmeans
class TestWindow(Screen):
    # R = MainWindow.age - test_array[MainWindow.nt][3]

    def __init__(self, **kw):
        super(TestWindow, self).__init__(**kw)
        TestWindow.c = 0
        TestWindow.score = 0

        self.prev = 0
        self.rating = 0
        self.cnt = 0
        self.send_text = 0

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

    def next_screen_result(self):
        if TestWindow.c == 3:
            self.manager.current = "result"
            self.manager.transition.direction = "left"
            TestWindow.c = 0

    def next_screen_loading(self):
        if TestWindow.c < 3:
            self.manager.current = "loading"
            self.manager.transition.direction = "left"

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

        if TestWindow.c == 2:  # FinalMarking
            self.rating = float(test_array[MainWindow.nt][3]) - float(MainWindow.age)

        self.prev = 0
        TestWindow.c = TestWindow.c + 1
        MainWindow.seat_height = int(MainWindow.std_height * test_array[MainWindow.nt][0])
        self.manager.get_screen(
            "test").ids.test2_label.text = f'seat Height is {MainWindow.seat_height} and do it with {test_array[MainWindow.nt][1]}'
        print(f'seat Height is {MainWindow.seat_height} and do it with {test_array[MainWindow.nt][1]}')
        control = self.manager.get_screen('title')
        self.send_text = MainWindow.seat_height
        control.send_data(str(self.send_text))

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

            elif TestWindow.c == 1 and int(self.prev) == 0:  # PassFail
                MainWindow.nt = MainWindow.nt + 1
                if MainWindow.nt > 14:
                    MainWindow.nt = 14

        if TestWindow.c == 2:  # FinalMarking
            MainWindow.nt = MainWindow.nt + 1
            self.rating = float(MainWindow.age) - float(test_array[MainWindow.nt][3])

        self.prev = 1
        TestWindow.c = TestWindow.c + 1
        MainWindow.seat_height = int(MainWindow.std_height * test_array[MainWindow.nt][0])
        self.manager.get_screen(
            "test").ids.test2_label.text = f'seat Height is {MainWindow.seat_height} and do it with {test_array[MainWindow.nt][1]}'
        print(f'seat Height is {MainWindow.seat_height} and do it with {test_array[MainWindow.nt][1]}')

        self.send_text = MainWindow.seat_height
        control = self.manager.get_screen('title')
        control.send_data(str(self.send_text))
        return MainWindow.nt

    pass


class LoadingWindow(Screen):  # incomplete
    # disable the button until the chair had been set up (+OK signal from raspberry pi)
    # insert in between every test window (done)
    # (Extra) add loading bar
    def __init__(self, **kw):
        super(LoadingWindow, self).__init__(**kw)
        self.response = 0

    def disable_load_button(self):
        load_screen = self.manager.get_screen("loading")
        # self.response = control.get_data()
        # print(self.response)
        load_screen.ids.load_button.disabled = True

    def enable_load_button(self):
        load_screen = self.manager.get_screen("loading")
        control = self.manager.get_screen('title')
        while True:
            try:

                self.response = control.get_data()
                if self.response.decode('utf-8') == "OK":
                    print(self.response.decode('utf-8'))
                    sleep(1)
                    load_screen.ids.load_button.disabled = False
                    break
                else:
                    print("Wrong Data")
                    print(self.response)
            finally:
                pass


class MaintenanceWindow(Screen):


    def enable_test(self):
        maintenance = self.manager.get_screen('maintenance')
        maintenance.ids.maintenance_button_1.disabled = False

        pass
    def test_1(self):
        maintenance = self.manager.get_screen('maintenance')
        maintenance.ids.maintenance_button_1.disabled = True
        maintenance.ids.maintenance_button_2.disabled = False
        pass

    def test_2(self):
        maintenance = self.manager.get_screen('maintenance')
        maintenance.ids.maintenance_button_2.disabled = True
        maintenance.ids.maintenance_end.disabled = False
        pass
    def test_end(self):


        pass
    pass


class ResultWindow(Screen):
    pass

class ExplanationWindow(Screen):
    pass

class ConnectionWindow(Screen):  # establish connection Here if not then have a button to retry
    def __init__(self, **kwargs):
        super(ConnectionWindow, self).__init__(**kwargs)

    def reconnect(self):
        control = self.manager.get_screen('title')
        try:
            control.connection()
        except WindowsError:
            print("No Connection")

    def top(self):
        self.manager.current = "title"
        self.manager.transition.direction = "up"

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
