from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivy.core.text import LabelBase
Builder.load_file('test.kv')
class WindowManager(ScreenManager):
    pass

class LoadingWindow(Screen):
    def loading(self, *kwargs):
        loading_grid = self.ids.loading
        anim = Animation(height=80, width=80, spacing=[10, 10], duration=0.5)
        anim += Animation(height=60, width=60, spacing=[10, 10], duration=0.5)
        anim += Animation(angle = loading_grid.angle + 45, duration=0.5)
        anim.bind(on_complete=self.loading)
        anim.start(loading_grid)



class Example(MDApp):
    def build(self):
        LabelBase.register("custom_font", fn_regular="TakaoPGothic.ttf")
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return WindowManager()

if __name__ == "__main__":
    Example().run()


