from kivy.config import Config
from kivy.config import Config

# 0 выключен 1 включен как true / false
# Вы можете использовать 0 или 1 && True или False

Config.set('graphics', 'resizable', False)

# Импорт всех классов
from kivy.uix.gridlayout import GridLayout
import pickle
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from kivy.core.window import Window
#Window.clearcolor = (1, 1, 1, 1)
from kivy.uix.behaviors import ButtonBehavior
# Глобальные настройки
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button

from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.screenmanager import Screen
class ImageButton(ButtonBehavior,FloatLayout, Image):
    pass
from kivy.lang import Builder
from kivymd.app import MDApp

from kivymd.uix.boxlayout import MDBoxLayout
class Game(Screen):
    def __init__(self, **kwargs):
        #self.f1 = Widget()
        super().__init__(**kwargs)
        #self.size_hint = (1,1)
        self.bitcoin = 0

    def on_tap(self):
        self.bitcoin+=0.000001
        #print(App.get_running_app().root.ids['hi'])
        App.get_running_app().root.ids['bitcoins_num'].text = '{0:.6f}'.format(self.bitcoin)
class app(MDApp):


    def build(self):
        game = Game()
        #self.title = "Tap-Fight"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        #Clock.schedule_interval(game.loop,1.0)
    #self.background_color=(1,0.1,0.1)
        return game

# Запуск проекта
if __name__ == "__main__":
    app().run()