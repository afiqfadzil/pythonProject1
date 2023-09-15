

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

KV = '''
BoxLayout:
    orientation: 'vertical'

    MDBoxLayout:
        orientation: 'vertical'

        MDLabel:
            text: 'Label on Top'
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]

        MDGridLayout:
            cols: 3
            row_force_default: True
            row_default_height: '50dp'
            col_force_default: True
            col_default_width: '50dp'

            MDLabel:
                text: '1'
            MDLabel:
                text: '2'
            MDLabel:
                text: '3'
            MDLabel:
                text: '4'
            MDLabel:
                text: '5'
            MDLabel:
                text: '6'
'''


class GridLayoutApp(MDApp):
    def build(self):
        return Builder.load_string(KV)


if __name__ == '__main__':
    GridLayoutApp().run()