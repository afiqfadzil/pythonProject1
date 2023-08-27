import sys

from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivymd.app import MDApp

from kivy.core.window import Window

from kivy.config import Config

from client import *

from time import sleep
from kivy.core.text import LabelBase

LabelBase.register(name='takao', fn_regular="TakaoPGothic.ttf")

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


class TextWindow(Screen):
    def press(self):
        data = self.manager.get_screen('text')
        name = data.ids.name.text
        email = data.ids.email.text
        with open("calculation.txt", mode="w") as myfile:
            myfile.writelines(f"{name},{email}\n")
            print("Name: ", name, "\nEmail: ", email, "\nADDED!")

        data.ids.name.text = ""
        data.ids.email.text = ""

    pass


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

    def start_maintenance(self):
        try:
            self.manager.current = "maintenance"
            self.manager.transition.direction = "up"
        except Exception as e:
            self.manager.current = "connect"
            self.manager.transition.direction = "left"

            pass

    def connection(self):
        try:
            self.sock = MySocket(host=AddressScreen.ip)
            print(self.sock)
            # Thread(target=self.send_data).start()
            # Thread(target=self.get_data).start()
            self.manager.current = "title"
            self.manager.transition.direction = "left"
        except Exception as e:
            print(str(e))
            sleep(0.1)
            self.manager.current = "connect"
            self.manager.transition.direction = "left"

    def get_data(self):
        while True:
            return self.sock.get_data()

    def send_data(self, msg=None):
        while True:
            # msg = input()
            self.sock.send_data(msg)
            break


class AddressScreen(Screen):
    def __init__(self, **kwargs):
        super(AddressScreen, self).__init__(**kwargs)

    def connect(self):
        title = self.manager.get_screen("title")
        address = self.manager.get_screen("address")
        AddressScreen.ip = address.ids.ip.text

        try:
            title.connection()
        except Exception as e:
            self.manager.current = "connect"
            self.manager.transition.direction = "left"


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
        MainWindow.std_height = 0  # Capital Ho
        self.seat = 0


    def data_call(self):
        with open("calculation.txt", mode="r") as myfile:
            data = myfile.read()
            MainWindow.a = data.split(",")
            tmp = [float(e) for e in MainWindow.a]
            MainWindow.a, MainWindow.b = tmp
            myfile.close()
        age_flag = 0
        ht_flag = 0
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
        if ht_text == "" or str(ht_text.isnumeric()) == "False":
            main_screen.ids.error_label_main.text = "身長を入力してください！"
            ht_flag = 1
            return 0
        if age_text == "" or str(age_text.isnumeric()) == "False":
            main_screen.ids.error_label_main.text = "年齢を入力してください！"
            age_flag = 1
            return 0
        if age_flag == 0 and ht_flag == 0 :
            try:
                control.send_data("START")
                sleep(0.1)
            except Exception as e:
                self.manager.current = "connect"
                self.manager.transition.direction = "left"

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
        MainWindow.seat_height = MainWindow.a * MainWindow.seat_height + MainWindow.b
        self.manager.current = "loading"
        self.manager.transition.direction = "left"
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
        self.seat = MainWindow.seat_height
        try:
            control.send_data(str(self.seat))
        except Exception as e:
            print(str(e))
            sleep(0.1)
            self.manager.current = "connect"
            self.manager.transition.direction = "left"
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
            result_screen.ids.result_label_comment.text = C[self.cnt]
            result_screen.ids.result_label_age.text = f'貴殿の年齢は :{(str(MainWindow.age))}'
            result_screen.ids.result_label_rage.text = f'貴殿のロコモ年齢は :{str(test_array[MainWindow.nt][3])}'

            print(self.rating)
            print(MainWindow.age)
            print(test_array[MainWindow.nt][3])

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
                    "test").ids.test2_label.text = 'もう一度せき着席して、もう一度試してください'

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
            MainWindow.seat_height = MainWindow.a*MainWindow.seat_height+MainWindow.b
            print(f'seat Height is {MainWindow.seat_height} and do it with {test_array[MainWindow.nt][1]}')
            control = self.manager.get_screen('title')
            self.send_text = MainWindow.seat_height
            if TestWindow.c < 3:
                try:
                    control.send_data("START")
                    control.send_data(str(self.send_text))
                except Exception as e:
                    self.manager.current = "connect"
                    self.manager.transition.direction = "left"
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
            MainWindow.seat_height = MainWindow.a * MainWindow.seat_height + MainWindow.b
            print(f'seat Height is {MainWindow.seat_height} and do it with {test_array[MainWindow.nt][1]}')

            self.send_text = MainWindow.seat_height
            control = self.manager.get_screen('title')
            if TestWindow.c < 3:
                try:
                    control.send_data("START")
                    control.send_data(str(self.send_text))
                except Exception as e:
                    print(str(e))
                    sleep(0.1)
                    self.manager.current = "connect"
                    self.manager.transition.direction = "left"
        else:
            pass


class LoadingWindow(Screen):  # incomplete
    # disable the button until the chair had been set up (+OK signal from raspberry pi)
    # insert in between every test window (done)
    # (Extra) add loading bar
    kv ='''
    <Grid@MDGridLayout>
        canvas.before:
            PushMatrix
            Rotate:
                angle: root.angle
                origin: self.center
        canvas.after:
            PopMatrix
    MDFloatLayout:
        md_bg_color : 1,1,1,1
        Grid:
            id:loading_anim
            angle:0
            rows:2
            cols:2
            size_hint: None,None
            height:60
            width:60
            pos_hint:{"center_x":.5,"center_y":.5}
            spacing:5
            MDFloatLayout:
                md_bg_color:rgba(242,80,34,255)
            MDFloatLayout:
                md_bg_color:rgba(242,80,34,255)
            MDFloatLayout:
                md_bg_color:rgba(242,80,34,255)
            MDFloatLayout:
                md_bg_color:rgba(242,80,34,255)
    '''
    def __init__(self, **kw):
        super(LoadingWindow, self).__init__(**kw)
        self.response = 0
        self.angle = 45


    def loading(self, *args):
        anim = Animation(height = 80 , width = 80 ,spacing = [10,10], duration = 0.5)
        anim += Animation(height = 80 , width = 80 ,spacing = [10,10], duration = 0.5)
        anim += Animation(height = 80 , width = 80 ,spacing = [10,10], duration = 0.5)
        anim.bind(on_complete=self.loading)
        anim.start(self.root.ids.loading_anim)
        self.angle += 45



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
                    print(self.response.decode('utf-8'))
            finally:
                pass


class MaintenanceWindow(Screen):

    def __init__(self, **kw):
        super(MaintenanceWindow, self).__init__(**kw)
        self.response = 0
        self.a = 0
        self.b = 0
        self.v2 = 0
        self.v1 = 0

    # Send Maintenance command code to the server to run maintenance mode

    def set_button_state(self, button_name, state):
        maintenance = self.manager.get_screen('maintenance')
        maintenance.ids[button_name].disabled = state

    def get_data(self):
        while True:
            control = self.manager.get_screen('title')
            return control.get_data()

    def send_data(self, msg=None):
        control = self.manager.get_screen('title')
        control.send_data(msg)

    def enable_test(self):
        self.set_button_state('maintenance_button_1', False)

    def test_1(self):
        maintenance = self.manager.get_screen('maintenance')
        self.set_button_state('maintenance_button_1', True)
        self.set_button_state('maintenance_button_2', False)
        try:
            self.send_data("ONETIMEREAD")
            self.v1 = self.get_data()
            self.v1 = (self.v1.decode())
            print(self.v1)
            maintenance.ids.test1.text = f'現在の座面高さ{self.v1}㎝'
        except Exception as e:
            print(e)
            self.manager.current = "connect"
            self.manager.transition.direction = "left"

    def test_2(self):
        maintenance = self.manager.get_screen('maintenance')
        self.set_button_state('maintenance_button_2', True)
        self.set_button_state('maintenance_end', False)
        try:

            self.send_data("ONETIMEREAD")
            self.v2 = self.get_data()
            self.v2 = (self.v2.decode())
            print(self.v1)
            maintenance.ids.test2.text = f'現在の座面高さ{self.v2}㎝'
        except Exception as e:
            print(e)
            self.manager.current = "connect"
            self.manager.transition.direction = "left"
        self.a = (40 - 10) / (float(self.v2) - float(self.v1))
        self.b = (10 * float(self.v2) - 40 * float(self.v1)) / (float(self.v2) - float(self.v1))
        a = round(self.a, 1)
        b = round(self.b, 1)
        maintenance.ids.result.text = f'A：{a}\nB：{b}'
        with open("calculation.txt", mode="w") as myfile:
            myfile.writelines(f"{a},{b}")
            print("A: ", a, "\nB: ", b, "\nADDED!")
            myfile.close()

    def test_end(self):
        self.send_data("EXIT")
        pass

    def exit(self):
        try:
            control = self.manager.get_screen('title')
            control.send_data("EXIT")
            recv = (control.get_data())
            print(recv.decode())
            self.manager.current = "title"
            self.manager.transition.direction = "down"
        except Exception as e:
            print(e)
            self.manager.current = "connect"
            self.manager.transition.direction = "left"

    pass


class ResultWindow(Screen):
    pass


class ExplanationWindow(Screen):

    def connection(self):
        control = self.manager.get_screen('title')
        try:
            control.connection()
        except WindowsError:
            print("No Connection")

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
class TopBar(BoxLayout):
    pass
class NavDrawer(Widget):
    pass
class MyMainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"  # Choose a darker color palette, like "Gray"
        self.theme_cls.primary_hue = "800"
        self.theme_cls.secondary_palette = "Grey"

        if platform == 'android' or platform == 'ios':
            Window.maximize()
        else:
            Window.size = (620, 1024)
        return WindowManager()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    MyMainApp().run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
