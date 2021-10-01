# code - Arsbul's Guis
# textures: ASTghostHost
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
import time
import pickle
from kivymd.uix.boxlayout import MDBoxLayout
class Game(Screen):

    def __init__(self, **kwargs):

        #self.f1 = Widget()
        super().__init__(**kwargs)

        try:
            with open("player.pickle","rb") as f:
                self.player_data = pickle.load(f)
        except:

            with open("player.pickle", "wb") as f:
                self.player_data = {"bitcoins": 0, "doubling": 1,"doubling_price":0.001,"bot":{"alow_bot":False,"bot_speed":0,"bot_price": 1}}
                pickle.dump(self.player_data,f)



                #self.bitcoin = 0
        #self.size_hint = (1,1)
        self.bot_data = self.player_data["bot"]
    def update_data(self):
        with open("player.pickle", "wb") as f:
            pickle.dump(self.player_data, f)

    def on_tap(self):
        self.player_data["bitcoins"]+=0.000001*self.player_data["doubling"]
        #print(App.get_running_app().root.ids['hi'])

    def buy_doubling(self):

        if self.player_data["bitcoins"]- self.player_data["doubling_price"] > 0:
            self.player_data["doubling"] +=1

            self.player_data["bitcoins"]-= self.player_data["doubling_price"]
            self.player_data["doubling_price"] *= 3

    def buy_bot(self):
        print(self.bot_data["bot_price"])
        if self.player_data["bitcoins"]- self.bot_data["bot_price"] > 0:
            self.player_data["bitcoins"] -= self.bot_data["bot_price"]
            self.bot_data["alow_bot"] = True
            self.bot_data["bot_speed"] +=1
            self.bot_data["bot_price"] += 2

    def main_loop(self,dt):
        self.update_data()
        App.get_running_app().root.ids[
            'text_doubling'].text = f'''Удвоение майнинга до:{self.player_data["doubling"] + 1}x\nЦена: {'{0:.6f}'.format(self.player_data["doubling_price"])}'''
        App.get_running_app().root.ids['bitcoins_num'].text = '{0:.6f}'.format(self.player_data["bitcoins"])
        App.get_running_app().root.ids['doubling'].text = f'''Удвоение майнинга:{self.player_data["doubling"]}x'''

        App.get_running_app().root.ids[
            'text_bot'].text = f'''Клик-бот\nАвтоматически майнит\n скорость: {self.bot_data["bot_speed"]} клик в секунду,\nцена: {self.bot_data["bot_price"]} биткоин'''
    def bot_loop(self,dt):

        if self.bot_data["alow_bot"]:

            self.player_data["bitcoins"] += self.player_data["doubling"]
class app(MDApp):


    def build(self):
        game = Game()
        #self.title = "Tap-Fight"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        Clock.schedule_interval(game.main_loop,1/60)
        Clock.schedule_interval(game.bot_loop, 1/game.bot_data["bot_speed"])
    #self.background_color=(1,0.1,0.1)
        return game

# Запуск проекта
if __name__ == "__main__":
    app().run()