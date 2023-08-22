from platform import platform

from kivy.animation import Animation
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp

Builder.load_file("test.kv")

class WindowManager(ScreenManager):
    pass



class LoadingWindow(Screen):

    angle = 45

    def __init__(self, **kwargs):
        super(LoadingWindow, self).__init__(**kwargs)



    def loading(self,  *kwargs):
        load = self.manager.get_screen("loadingwindow")
        anim = Animation(height=80, width=80, spacing=[10, 10], duration=0.5)
        anim += Animation(height=60, width=60, spacing=[5, 5], duration=0.5)
        anim += Animation(angle =  load.angle ,duration=0.5)
        print(self.angle)
        load.angle += 45
        anim.bind(on_complete=self.loading)
        anim.start(load.ids.loading)






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

