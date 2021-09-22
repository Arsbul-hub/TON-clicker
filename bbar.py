from kivy.config import Config
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 0)
Config.set('graphics', 'top', 0)
Config.set('graphics', 'height', 1366)
Config.set('graphics', 'width', 768)
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.app import App
class MainApp(MDApp):
    def build(self):
        #self.theme_cls.theme_style = "Dark"
        #self.theme_cls.primary_palette = "BlueGray"
        return Label(text="hi")


MainApp().run()
