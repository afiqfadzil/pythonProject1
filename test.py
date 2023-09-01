import kivymd

'''
from android.permissions import request_permissions, Permission
request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.CHANGE_WIFI_STATE, Permission.ACCESS_WIFI_STATE, Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_COARSE_LOCATION])
'''
from kivymd.app import MDApp
import jnius
from kivymd.uix.toolbar import MDToolbar
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton
from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
# from kivy.utils import platform
from jnius import autoclass

Builder.load_string('''
<Principal>:

    MDToolbar:
        title: 'WifiScan'
        pos_hint: {'center_x': .5, 'center_y': .97}
        right_action_items: [['reload',lambda x: root.wifi()]]
    MDFlatButton:
        text: 'Disabled'
        pos_hint: {"center_x": .5, "center_y": .15}
        on_press:
            root.wifi() 
            root.desconecta()



    MDFlatButton:
        id: boton
        text: ''
        size_hint: 12, .10
        on_press: root.info()
        pos_hint: {"center_x": .4, "center_y": .85}

    MDFlatButton:
        id: boton2
        size_hint: 12, .10
        text: ''
        on_press: root.info2()
        pos_hint: {"center_x": .4, "center_y": .75}

    MDFlatButton:
        id: boton3
        size_hint: 12, .10
        text: ''
        on_press: root.info3()
        pos_hint: {"center_x": .4, "center_y": .65}


    MDFlatButton:
        id: boton4
        text: ''
        size_hint: 12, .10
        on_press: root.info3()
        user_font_size: '16sp'
        pos_hint: {"center_x": .4, "center_y": .55}


    MDFlatButton:
        id: boton5
        text: ''
        on_press: root.info4()
        size_hint: 12, .10
        user_font_size: '16sp'
        pos_hint: {"center_x": .4, "center_y": .45}



    Label:
        id: label1
        text: "" 
        pos_hint: {"center_x": .1, "center_y": .85}   

    Label:
        id: label2
        text: "" 
        pos_hint: {"center_x": .1, "center_y": .75}                       

    Label:
        id: label3
        text: "" 
        pos_hint: {"center_x": .1, "center_y": .65}   

    Label:
        id: label4
        text: "" 
        pos_hint: {"center_x": .1, "center_y": .55}   

    Label:
        id: label5
        text: "" 
        pos_hint: {"center_x": .1, "center_y": .45}     



''')


class Principal(Screen):
    def __init__(self, **kwargs):

        super(Principal, self).__init__(**kwargs)

    try:

        def wifi(self):

            PythonActivity = autoclass('org.renpy.android.PythonActivity')
            WifiManager = autoclass('android.net.wifi.WifiManager')
            activity = PythonActivity.mActivity
            service = activity.getSystemService(PythonActivity.WIFI_SERVICE)

            service.startScan()

            variable = WifiManager.getScanResults()

            for i in range(0, variable.size() - 1):
                nameymac = variable.get(i).SSID + '\n' + variable.get(i).BSSID
                level1 = str(variable.get(i).level)
                chanel = str(variable.get(i).channelWidth)
                wps = str(variable.get(i).capabilities)
                # wpa2 = wps.replace('WPA2', 'WPA2')
                self.Capa = str(variable.get(i).capabilities)

                self.ids.label1.text = "   " + level1  # +"\n" + wpa2[1:5]

                self.ids.boton.text = nameymac

            for i in range(0, variable.size() - 2):
                self.nameymac2 = variable.get(i).SSID + '\n' + variable.get(i).BSSID
                level2 = str(variable.get(i).level)
                self.Capa2 = str(variable.get(i).capabilities)
                self.ids.label2.text = level2

                self.ids.boton2.text = self.nameymac2

            for i in range(0, variable.size() - 3):
                nameymac3 = variable.get(i).SSID + '\n' + variable.get(i).BSSID
                level3 = str(variable.get(i).level)
                self.Capa3 = str(variable.get(i).capabilities)

                self.ids.label3.text = level3
                self.ids.boton3.text = nameymac3

            for i in range(0, variable.size() - 4):
                nameymac4 = variable.get(i).SSID + '\n' + variable.get(i).BSSID
                level4 = str(variable.get(i).level)
                self.Capa4 = str(variable.get(i).capabilities)
                self.ids.label4.text = level4
                self.ids.boton4.text = nameymac4

            for i in range(0, variable.size() - 5):
                nameymac5 = variable.get(i).SSID + '\n' + variable.get(i).BSSID
                level5 = str(variable.get(i).level)
                self.Capa5 = str(variable.get(i).capabilities)
                self.ids.label5.text = level5
                self.ids.boton5.text = nameymac5

    except:
        pass

    def desconecta(self):
        PythonActivity = autoclass('org.renpy.android.PythonActivity')
        WifiManager = autoclass('android.net.wifi.WifiManager')
        activity = PythonActivity.mActivity
        service = activity.getSystemService(PythonActivity.WIFI_SERVICE)

        service.disconnect()
        service.reconnect()

    def info(self):
        # if self.ids.boton.text != "":
        self.msg = MDDialog(
            type='custom',
            size_hint=(.9, .1),
            text=self.ids.boton.text + "\n\n"
                 + "Seguridad:  \n" + self.Capa)

        self.msg.open()

    def info2(self):
        # if self.ids.boton2.text != "":
        self.msg = MDDialog(
            type='custom',
            size_hint=(.9, .1),
            text=self.ids.boton2.text + "\n\n"
                 + "Seguridad:  \n" + self.Capa2

        )
        self.msg.open()

    def info3(self):
        #   if self.ids.boton3.text != "":
        self.msg = MDDialog(
            type='custom',
            size_hint=(.9, .1),
            text=self.ids.boton3.text + "\n\n"
                 + "Seguridad:  \n" + self.Capa3

        )
        self.msg.open()

    def info4(self):
        #  if self.ids.boton4.text != "":
        self.msg = MDDialog(
            type='custom',
            size_hint=(.9, .1),
            text=self.ids.boton4.text + "\n\n"
                 + "Seguridad:  \n" + self.Capa4

        )
        self.msg.open()

    def info5(self):
        # if self.ids.boton5.text != "":
        self.msg = MDDialog(
            type='custom',
            size_hint=(.9, .1),
            text=self.ids.boton5.text + "\n\n"
                 + "Seguridad:  \n" + self.Capa5

        )
        self.msg.open()


'''
    def del_widget(self):
        if self.ids.boton.text == self.ids.boton2.text or self.ids.boton =='':
            self.remove_widget(self.ids.boton)  

            self.remove_widget(self.ids.boton2)             
            self.ids.label1.text = ""
            self.ids.label2.text = ""
        else:
            pass   

        if self.ids.boton3.text ==self.ids.boton4.text or self.ids.boton3.text=='':
            self.remove_widget(self.ids.boton3)             
            self.ids.label3.text = ""

            self.remove_widget(self.ids.boton4)
            self.ids.label4.text = ""
        else:
            pass

        if self.ids.boton5.text ==self.ids.boton4.text or self.ids.boton5.text =="":
            self.remove_widget(self.ids.boton5)
            self.ids.label5.text = ""
        else:
            pass
'''


class Runnin(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        sm = ScreenManager()
        principal = Principal(name='principal')
        sm.add_widget(principal)
        return sm


Runnin().run()