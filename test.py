from kivy.app import App
from kivy.uix.image import Image
import os
os.environ['KIVY_METRICS_DENSITY'] = '2'
os.environ['KIVY_TEXT'] = 'pil'
os.environ['KIVY_IMAGE'] = 'pil,sdl2'


class GifApp(App):
    def build(self):
        gif_path = 'assets/loading.zip'  # Replace with the path to your GIF file
        gif_image = Image(source=gif_path, anim_delay=1 / 30.0)  # Adjust the delay as needed for your GIF

        return gif_image


if __name__ == '__main__':
    GifApp().run()