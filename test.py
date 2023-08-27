from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.text import LabelBase
KV = '''
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: "#1E1E15"

    MDTopAppBar:
        title_font_name: "custom_font"
        title: "\u3053\u3093\u306B\u3061\u306F\u3001\u4E16\u754C\uFF01"

    MDLabel:
        text: "\u3053\u3093\u306B\u3061\u306F\u3001\u4E16\u754C\uFF01"
        font_name: "custom_font"
        halign: "center"
'''


class Example(MDApp):
    def build(self):
        LabelBase.register("custom_font", fn_regular="TakaoPGothic.ttf")
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return Builder.load_string(KV)

if __name__ == "__main__":
    Example().run()


Example().run()