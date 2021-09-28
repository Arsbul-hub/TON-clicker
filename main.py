from kivy.config import Config
from kivy.config import Config

# 0 выключен 1 включен как true / false
# Вы можете использовать 0 или 1 && True или False



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
import pickle
from kivymd.uix.boxlayout import MDBoxLayout
class Game(BoxLayout):

    def __init__(self, **kwargs):

        #self.f1 = Widget()
        super().__init__(**kwargs)
        try:
            with open("player.pickle","rb") as f:
                self.player_data = pickle.load(f)
        except:

            with open("player.pickle", "wb") as f:
                self.player_data = {"bitcoins": 0, "doubling": 1}
                pickle.dump(self.player_data,f)



                #self.bitcoin = 0
        #self.size_hint = (1,1)
        self.doubling_price = 0.001
    def update_data(self):
        with open("player.pickle", "wb") as f:
            pickle.dump(self.player_data, f)

    def on_tap(self):
        self.player_data["bitcoins"]+=0.000001*self.player_data["doubling"]
        #print(App.get_running_app().root.ids['hi'])

    def doubling(self):

        if self.player_data["bitcoins"]- 0.001 > 0:
            self.player_data["doubling"] = self.player_data["doubling"] +2
            self.doubling_price*=5
            self.player_data["bitcoins"]-= self.doubling_price

    def loop(self,dt):
        self.update_data()
        App.get_running_app().root.ids[
            'text_doubling'].text = f'''Удвоение майнинга до:{self.player_data["doubling"] + 1}x\nЦена: {self.doubling_price}'''
        App.get_running_app().root.ids['bitcoins_num'].text = '{0:.6f}'.format(self.player_data["bitcoins"])
        App.get_running_app().root.ids['doubling'].text = f'''Удвоение майнинга:{self.player_data["doubling"]}x'''
class app(MDApp):


    def build(self):
        game = Game()
        #self.title = "Tap-Fight"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        Clock.schedule_interval(game.loop,1/60)
    #self.background_color=(1,0.1,0.1)
        return game

# Запуск проекта
if __name__ == "__main__":
    app().run()