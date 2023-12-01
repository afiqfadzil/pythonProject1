import sys
from kivy.clock import Clock
import webbrowser
from kivy.factory import Factory
import socket
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from threading import Thread
from kivy.core.window import Window
from kivy.core.text import LabelBase, DEFAULT_FONT  # 追加分
from kivy.resources import resource_add_path  # 追加分
from kivy.config import Config
import pickle
from time import sleep
from kivy.core.text import LabelBase
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard

LabelBase.register(DEFAULT_FONT, 'meiryo.ttc')  # 追加分

# Add Guideline
# Check Program (Maintenance window responsiveness) Popup window
# main window

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# test_array [SeatHeight,OneL = 0/BothL = 1 , Score , Locomotion Age]
test_array = [[], [0.5, "One Leg", 100, 16.00], [0.5, "One Leg", 95, 27.95], [0.625, "One Leg", 90, 39.9],
              [0.75, "One Leg", 85, 51.85], [0.875, "One Leg", 80, 63.8], [1.0, "One Leg", 75, 75.75],
              [0.375, "Two Legs", 70, 87.7],
              [0.5, "Two Legs", 65, 99.65], [0.625, "Two Legs", 60, 111.6], [0.75, "Two Legs", 55, 123.55],
              [0.875, "Two Legs", 50, 135.5],
              [1.0, "Two Legs", 45, 147.45], [1.125, "Two Legs", 40, 159.4], [1.25, "Two Legs", 35, 171.35]]
Builder.load_file("project1.kv")
Config.set('graphics', 'resizable', '0')  # 0 being off 1 being on as in true/false
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '1000')
Config.write()
C = ["Error Check", "素晴らしい基礎運動力です",
     "良い基礎運動力です",
     "基礎運動力平均より低い、筋肉バランス感覚のトレーニングをしましょう",
     "ロコモシンドロームの傾向がありロコモ検診してください",
     "基礎運動能力がい著しく低下、ちかくの整形外科病院で受診してください"]
my_app = None


# Task
# server is included with the relay module program (サーバーとリレーモジュールのプログラムは一緒)
# configure so that the program do not crash if not connected to a server


class ClientMain:
    def __init__(self):
        global client
        client = self
        self.response = 0
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.stop_sign = 1

        self.response = None
        self.sock = None

    def connection(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(1)
            self.sock.connect((AddressScreen.ip, 8000))
            self.sock.settimeout(60)
            print("Connected")
            my_app.sm.current = "title"
            my_app.sm.transition.direction = "left"
        except Exception as e:
            print(str(e))
            my_app.sm.current = "connect"
            my_app.sm.transition.direction = "left"

    def get_data(self):
        if self.sock is not None:
            return self.sock.recv(1024)
        else:
            print("get_dataSocket is not initialized.")
            return None

    def send_data(self, msg):
        if self.sock is not None:
            try:
                if type(msg) == list:
                    data = pickle.dumps(msg)
                    self.sock.send(data)
                else:
                    self.sock.send(msg.encode())
            except Exception as e:
                my_app.sm.current = "connect"
                my_app.sm.transition.direction = "left"
        else:
            print("send_dataSocket is not initialized.")
            my_app.sm.current = "connect"
            my_app.sm.transition.direction = "left"

    def check_response(self):

        load_screen = my_app.sm.get_screen("loading")
        while True:
            self.response = self.get_data()
            data = self.response
            if data.decode('utf-8') == "OK":
                print(self.response)
                load_screen.ids.load_button.disabled = False

                break  # Exit the loop when we receive the expected data
            elif data.decode('utf-8') == "EXIT":
                self.stop_sign = 0

                break




            else:
                print("Wrong Data")
                print(f'Response: {self.response}')
                sleep(1)  # Adjust the sleep duration as needed

    def set_button_state(self, button_name, state):
        maintenance = my_app.sm.get_screen('maintenance')
        maintenance.ids[button_name].disabled = state

    def test_1(self):
        maintenance = my_app.sm.get_screen('maintenance')
        self.set_button_state('maintenance_button_1', True)
        self.set_button_state('maintenance_button_2', False)
        try:
            self.send_data("ONETIMEREAD")
            self.t1 = self.get_data()
            self.t1 = (self.t1.decode('utf-8'))
            print(self.t1)
            maintenance.ids.test1.text = f'現在の座面高さ{self.t1}㎝'
            sleep(0.5)
        except Exception as e:
            print(e)
            my_app.sm.current = "connect"
            my_app.sm.transition.direction = "left"
            return 0

    def test_2(self):
        maintenance = my_app.sm.get_screen('maintenance')
        self.set_button_state('maintenance_button_2', True)
        self.set_button_state('maintenance_button_3', False)
        try:

            self.send_data("ONETIMEREAD")
            self.t2 = self.get_data()
            self.t2 = (self.t2.decode('utf-8'))
            print(self.t2)
            maintenance.ids.test2.text = f'現在の座面高さ{self.t2}㎝'
            sleep(0.5)
        except Exception as e:
            print(e)
            my_app.sm.current = "connect"
            my_app.sm.transition.direction = "left"
            return 0

    def test_3(self):
        maintenance = my_app.sm.get_screen('maintenance')
        self.set_button_state('maintenance_button_3', True)
        self.set_button_state('maintenance_end', False)
        try:
            self.send_data("ONETIMEREAD")
            self.t3 = self.get_data()
            self.t3 = (self.t3.decode('utf-8'))

            maintenance.ids.test3.text = f'現在の座面高さ{self.t3}㎝'
            sleep(0.5)
        except Exception as e:
            print(e)
            my_app.sm.current = "connect"
            my_app.sm.transition.direction = "left"
            return 0
        t1 = float(self.t1)
        t2 = float(self.t2)
        t3 = float(self.t3)
        self.a = -((t3 - 50) - (t2 - 30)) / 20
        self.b = ((t1 - 10) - (t2 - 30)) / 20
        self.c = -(t2 - 30)
        self.d = -(t2 - 30) - (float(self.b) * 30)

        a = round(self.a, 3)
        b = round(self.b, 3)
        c = round(self.c, 3)
        d = round(self.d, 3)
        data = [a, b, c, d]
        client_main.send_data("MTVAL")
        client_main.send_data(data)

        print(data)


client_main = ClientMain()


class AddressScreen(Screen):
    def __init__(self, **kwargs):
        super(AddressScreen, self).__init__(**kwargs)
        AddressScreen.ip = 0

    def connect(self):
        title = self.manager.get_screen("title")
        address = self.manager.get_screen("address")
        AddressScreen.ip = address.ids.ip.text

        try:
            client_main.connection()

        except Exception as e:
            self.manager.current = "connect"
            self.manager.transition.direction = "left"


class TitleWindow(Screen):  # connection to server may start here
    def __init__(self, **kwargs):
        super(TitleWindow, self).__init__(**kwargs)
        self.sock = None
        self.text = 0

    def next_screen(self):
        self.manager.current = "main"
        self.manager.transition.direction = "up"

    def start_maintenance(self):
        self.manager.current = "maintenance"
        self.manager.transition.direction = "right"

    def info(self):
        self.manager.current = "explain"
        self.manager.transition.direction = "left"


########################################################################################################################
class CustomDropDown(DropDown):
    pass


class ContentNavigationDrawer(BoxLayout):
    pass


class ItemDrawer:
    icon = StringProperty()


# Popup Window section
class ShutdownPopup(Popup):
    def btn(self):
        try:
            client_main.send_data("SHUTDOWN")
            sys.exit()
        except Exception as e:
            app = MyMainApp.get_running_app()
            app.root.current = "connect"
            app.root.transition.direction = "right"

    pass


class DisconnectPopup(Popup):
    def btn(self):
        try:
            client_main.send_data("DISCONNECT")
        except Exception as e:
            app = MyMainApp.get_running_app()
            app.root.current = "connect"
            app.root.transition.direction = "right"

    pass


class ErrorPopup(Popup):
    def btn(self):
        TestWindow.c = 0
        app = MyMainApp.get_running_app()
        app.root.current = "main"
        app.root.transition.direction = "right"

    pass


class ConfirmPopup(Popup):
    pass


class MovingPopup(Popup):  # Popup when the seat is moving in loading screen
    pass


class CautionPopup(Popup):  # Popup when leaving loading test
    def btn(self):
        loading = my_app.sm.get_screen("loading")
        loading.ids.load_button.disabled = True
        TestWindow.c = 0
        app = MyMainApp.get_running_app()
        app.root.current = "main"
        app.root.transition.direction = "right"

    pass


class PracticePopup(Popup):
    def btn(self):
        loading = my_app.sm.get_screen("loading")
        loading.ids.load_button.disabled = True
        app = MyMainApp.get_running_app()
        app.root.current = "main"
        app.root.transition.direction = "right"

    pass


class LoadingPopup(Popup):
    def btn(self):
        app = MyMainApp.get_running_app()
        app.root.current = "main"
        app.root.transition.direction = "right"


class MD3Card(MDCard):
    pass


###############################################################################################################
class WindowManager(ScreenManager):
    pass


class GraphWindow(Screen):
    pass


class QRCodeWindow(Screen):
    pass


class FeedbackWindow(Screen):
    pass


class MainWindow(Screen):

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        MainWindow.load_flag = 0
        MainWindow.ht = 0
        MainWindow.nt = 0
        MainWindow.age = 0
        MainWindow.pre_score = 0
        MainWindow.seat_height = 0  # the one that will be sent to the chair
        MainWindow.std_height = 0  # Capital H
        self.seat = 0
        self.flag = 0  # 0 = practice / 1 = test

    def data_calculation(self):
        with open("calculation.txt", mode="r") as myfile:
            data = myfile.read()
            MainWindow.a = data.split(",")
            tmp = [float(e) for e in MainWindow.a]
            MainWindow.a, MainWindow.b = tmp
            myfile.close()

        test1_screen = self.manager.get_screen("test")
        main_screen = self.manager.get_screen("main")
        control = self.manager.get_screen('title')

        # Collect all the data from the Text Input Field in "project1.kv"

        ht_text = main_screen.ids.ht.text

        age_text = main_screen.ids.age.text

        test1_screen.ids.test2_label.text = ht_text

        # "Not Implemented yet"
        # Input will Fail if Blank Fields, Age is not a number, Age > 150 , Height > 2.50M (Done)
        # Address API
        # Radio Button for Gender
        # Space or Tab will be neglected
        ht_flag = 1
        age_flag = 1
        while ht_flag == 1 and age_flag == 1:
            if ht_text == "" or str(ht_text.isnumeric()) == "False":
                main_screen.ids.error_label_main.text = "*身長を入力してください！"

                return 0
            elif int(ht_text) <= 100 or int(ht_text) > 200:
                main_screen.ids.error_label_main.text = "*身長は　101cm～200cm　まで入力してください"

                return 0

            else:
                main_screen.ids.error_label_main.text = ""
                ht_flag = 0

            if age_text == "" or str(age_text.isnumeric()) == "False":
                main_screen.ids.error_label_main.text = "*年齢を入力してください！"

                return 0
            elif int(age_text) <= 15 or int(age_text) > 95:
                main_screen.ids.error_label_main.text = "*年齢にエラー (16~95)"
                return 0
            else:
                age_flag = 0
                main_screen.ids.error_label_main.text = ""

        try:

            client_main.send_data("START")
            my_app.sm.current = "loading"
            my_app.sm.transition.direction = "left"

            sleep(0.5)
        except Exception as e:
            self.manager.current = "connect"
            self.manager.transition.direction = "left"
            return 0

        MainWindow.age = int(age_text)
        MainWindow.ht = int(ht_text)
        MainWindow.std_height = 0.25 * MainWindow.ht - 1

        if MainWindow.age >= 81:
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

        self.seat = MainWindow.seat_height

        if self.flag == 0:
            self.practice()
        elif self.flag == 1:
            self.test()

    def practice_flag(self):
        self.flag = 0

    def test_flag(self):
        self.flag = 1

    def test(self):
        sleep(0.5)
        control = self.manager.get_screen('title')
        MainWindow.load_flag = 0
        try:
            client_main.send_data(str(self.seat))


        except Exception as e:
            print(str(e))
            sleep(0.1)
            self.manager.current = "connect"
            self.manager.transition.direction = "left"
            return 0

        if test_array[MainWindow.nt][1] == "One Leg":
            self.manager.get_screen(
                "test").ids.test_image.source = 'assets/one_leg.png'
            self.manager.get_screen(
                "test").ids.test2_label.text = '片足で立ち上がり，３秒間姿勢を維持してください\n．その後，椅子に座って，結果を選んでください．'
        elif test_array[MainWindow.nt][1] == "Two Legs":
            self.manager.get_screen(
                "test").ids.test_image.source = 'assets/two_leg.png'
            self.manager.get_screen(
                "test").ids.test2_label.text = '両足で立ち上がり，３秒間姿勢を維持してください．\n．その後，椅子に座って，結果を選んでください．'

        pass

    def practice(self):
        sleep(0.5)
        control = self.manager.get_screen('title')
        MainWindow.load_flag = 1
        try:
            client_main.send_data(str(self.seat))


        except Exception as e:
            print(str(e))
            sleep(0.1)
            self.manager.current = "connect"
            self.manager.transition.direction = "left"
            return 0

        if test_array[MainWindow.nt][1] == "One Leg":
            self.manager.get_screen(
                "practice").ids.practice_image.source = 'assets/one_leg.png'
            self.manager.get_screen(
                "practice").ids.practice_label.text = '片足で立ち上がり，３秒間姿勢を維持してください.\n練習終わったら”練習終了”のボタンを押してください.'
        elif test_array[MainWindow.nt][1] == "Two Legs":
            self.manager.get_screen(
                "practice").ids.practice_image.source = 'assets/two_leg.png'
            self.manager.get_screen(
                "practice").ids.practice_label.text = '両足で立ち上がり，３秒間姿勢を維持してください.\n練習終わったら”練習終了”のボタンを押してください.'

        pass

    def back(self):
        self.manager.current = "title"
        self.manager.transition.direction = "right"
        pass


class PracticeWindow(Screen):

    def home(self):
        Factory.CautionPopup().open()

    pass


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
        self.one_leg = Image(source='assets/one_leg.png')
        self.two_leg = Image(source='assets/two_leg.png')

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
            if self.rating < -20:

                result_screen.ids.result_label_comment.text = C[self.cnt]
                result_screen.ids.result_label_rage.text = f'貴殿のロコモ年齢は :{str(test_array[MainWindow.nt][3])}'

            else:
                result_screen.ids.result_label_comment.text = C[self.cnt]
                result_screen.ids.result_label_rage.text = f'貴殿のロコモ年齢は :{str(test_array[MainWindow.nt][3])}'

        pass

    def change(self):
        self.manager.get_screen(
            "test").ids.test_image.source = 'assets/one_leg.png'

    def next_screen_result(self):
        if TestWindow.c == 3:
            self.manager.current = "result"
            self.manager.transition.direction = "left"
            TestWindow.c = 0

    def next_screen_loading(self):
        if TestWindow.c < 3:
            self.manager.current = "loading"
            self.manager.transition.direction = "left"

    def retry(self):

        self.manager.get_screen(
            "test").ids.test2_label.text = 'もう一度着席して、もう一度試してください'

        pass

    def passed(self):
        if TestWindow.c < 3:
            if TestWindow.c < 3:
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

            if test_array[MainWindow.nt][1] == "One Leg":
                self.manager.get_screen(
                    "test").ids.test_image.source = 'assets/one_leg.png'
                self.manager.get_screen(
                    "test").ids.test2_label.text = '片足で立ち上がり，３秒間姿勢を維持してください\n．その後，椅子に座って，結果を選んでください．'
            elif test_array[MainWindow.nt][1] == "Two Legs":
                self.manager.get_screen(
                    "test").ids.test_image.source = 'assets/two_leg.png'
                self.manager.get_screen(
                    "test").ids.test2_label.text = '両足で立ち上がり，３秒間姿勢を維持してください．\n．その後，椅子に座って，結果を選んでください．'
            else:
                return 0

            self.prev = 0
            TestWindow.c = TestWindow.c + 1
            MainWindow.seat_height = int(MainWindow.std_height * test_array[MainWindow.nt][0])

            print(f'seat Height is {MainWindow.seat_height} and do it with {test_array[MainWindow.nt][1]}')
            control = self.manager.get_screen('title')
            self.send_text = MainWindow.seat_height
            if TestWindow.c < 3:
                try:
                    client_main.send_data("START")
                    client_main.send_data(str(self.send_text))
                    sleep(0.5)
                except Exception as e:
                    self.manager.current = "connect"
                    self.manager.transition.direction = "left"
                    return 0


        else:
            pass

    def failed(self):
        if TestWindow.c < 3:
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
            if test_array[MainWindow.nt][1] == "One Leg":
                self.manager.get_screen(
                    "test").ids.test_image.source = 'assets/one_leg.png'
                self.manager.get_screen(
                    "test").ids.test2_label.text = '片足で立ち上がり，３秒間姿勢を維持してください\n．その後，椅子に座って，結果を選んでください．'
            elif test_array[MainWindow.nt][1] == "Two Legs":
                self.manager.get_screen(
                    "test").ids.test_image.source = 'assets/two_leg.png'
                self.manager.get_screen(
                    "test").ids.test2_label.text = '両足で立ち上がり，３秒間姿勢を維持してください．\n．その後，椅子に座って，結果を選んでください．'
            else:
                return 0,

            self.prev = 1
            TestWindow.c = TestWindow.c + 1
            MainWindow.seat_height = int(MainWindow.std_height * test_array[MainWindow.nt][0])

            print(f'seat Height is {MainWindow.seat_height} and do it with {test_array[MainWindow.nt][1]}')

            self.send_text = MainWindow.seat_height
            control = self.manager.get_screen('title')
            if TestWindow.c < 3:
                try:
                    client_main.send_data("START")
                    client_main.send_data(str(self.send_text))
                except Exception as e:
                    print(str(e))
                    sleep(0.1)
                    self.manager.current = "connect"
                    self.manager.transition.direction = "left"
                    return 0
        else:
            pass

    def home(self):
        Factory.CautionPopup().open()


class LoadingWindow(Screen):  # incomplete
    # disable the button until the chair had been set up (+OK signal from raspberry pi)
    # insert in between every test window (done)
    # (Extra) add loading bar

    def __init__(self, **kw):
        super(LoadingWindow, self).__init__(**kw)

        self.response = 0
        self.tmp = 0
        self.load = None
        self.stop_loading = 0

    def popup_parent(self):
        loading = self.manager.get_screen("loading")
        if loading.ids.load_button.disabled:
            Factory.MovingPopup().open()
        else:
            Factory.CautionPopup().open()

    def stop_signal(self, dt):  # If dead, stop program return to menu
        if client_main.stop_sign == 1:
            pass
        else:
            Factory.ErrorPopup().open()

            client_main.stop_sign = 1
            pass

    def on_leave(self):
        self.stop_loading = 1
        sleep(0.5)
        self.stop_loading = 0

    def on_enter(self):
        self.load = Thread(target=self.loading)
        self.load.start()
        check = Thread(target=client_main.check_response)
        check.start()
        Clock.schedule_interval(self.stop_signal, 1.0)

    def loading(self, *kwargs):
        if self.stop_loading == 1:
            return 0
        if not self.manager.current == "loading":
            return 0
        else:
            loading_grid = self.ids.loading
            anim = Animation(height=200, width=200, spacing=[20, 20], duration=0.5)
            anim += Animation(height=150, width=150, spacing=[20, 20], duration=0.5)
            anim += Animation(angle=loading_grid.angle + 45, duration=0.5)
            anim.bind(on_complete=self.loading)
            anim.start(loading_grid)

    def disable_load_button(self):
        load_screen = self.manager.get_screen("loading")

        load_screen.ids.load_button.disabled = True

    def kill_load(self):
        self.load.terminate()

    def home(self):
        self.manager.current = "main"
        self.manager.transition.direction = "left"

    def switch(self):
        print("load_flag =", MainWindow.load_flag)
        if MainWindow.load_flag == 0:
            self.manager.current = "test"
            self.manager.transition.direction = "left"

        elif MainWindow.load_flag == 1:
            self.manager.current = "practice"
            self.manager.transition.direction = "left"


class MaintenanceWindow(Screen):

    def __init__(self, **kw):
        super(MaintenanceWindow, self).__init__(**kw)
        self.response = 0
        self.thread_1 = None
        self.thread_2 = None
        self.popup = LoadingPopup()
        self.interval = None

    # Send Maintenance command code to the server to run maintenance mode
    def set_button_state(self, button_name, state):
        maintenance = self.manager.get_screen('maintenance')
        maintenance.ids[button_name].disabled = state

    def back(self):
        self.manager.current = "title"
        self.manager.transition.direction = "left"
        pass

    def test_1(self):
        Clock.unschedule(self.interval)
        self.popup.open()
        self.thread_1 = Thread(target=client_main.test_1)
        self.thread_1.start()
        if self.thread_1.is_alive():
            self.interval = Clock.schedule_interval(self.dismiss_1, 1.0)

    def test_2(self):
        Clock.unschedule(self.interval)
        self.popup.open()
        self.thread_2 = Thread(target=client_main.test_2)
        self.thread_2.start()
        if self.thread_2.is_alive():
            self.interval = Clock.schedule_interval(self.dismiss_2, 1.0)

    def test_3(self):
        Clock.unschedule(self.interval)
        self.popup.open()
        self.thread_3 = Thread(target=client_main.test_3)
        self.thread_3.start()
        if self.thread_3.is_alive():
            self.interval = Clock.schedule_interval(self.dismiss_3, 1.0)

    def dismiss_1(self, dt):
        if not self.thread_1.is_alive():
            self.popup.dismiss()

    def dismiss_2(self, dt):
        if not self.thread_2.is_alive():
            self.popup.dismiss()

    def dismiss_3(self, dt):
        if not self.thread_3.is_alive():
            self.popup.dismiss()

    def test_end(self):
        client_main.send_data("EXIT")
        self.set_button_state('maintenance_button_1', False)
        self.set_button_state('maintenance_end', True)
        self.manager.current = "title"
        self.manager.transition.direction = "left"
        print(client_main.get_data())
        pass

    pass


class ResultWindow(Screen):
    pass


class ExplanationWindow(Screen):

    def back(self):
        self.manager.current = "title"
        self.manager.transition.direction = "right"
        pass

    pass
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
        self.manager.current = "address"
        self.manager.transition.direction = "up"

    pass


class Overlay(BoxLayout):
    pass


class NavDrawer(BoxLayout):
    pass


class MyMainApp(MDApp):
    def turn_off(self):
        Factory.ShutdownPopup().open()
        pass

    def build(self):
        global my_app

        my_app = self
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = "300"
        self.theme_cls.secondary_palette = "White"
        self.sm = WindowManager()
        self.client = ClientMain()
        return self.sm


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    MyMainApp().run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
