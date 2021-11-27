from kivy.config import Config
from kivy.config import Config

# 0 выключен 1 включен как true / false
# Вы можете использовать 0 или 1 && True или False
from kivy.uix.screenmanager import ScreenManager


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
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
from kivymd.app import MDApp
import pickle
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.tab import MDTabsBase
import random

#import numpy as np

main_font_size = 20
import os
import firebase_admin
from firebase_admin import db
import random

from threading import Thread



up_data = True
auth_succefull = False
offline = False
already_auth = False
data = {}
class SettingsTab(MDCard, MDTabsBase):
    pass

class Error_show(Screen):
    def __init__(self, **kwargs):

        #self.f1 = Widget()
        super().__init__(**kwargs)
        offline = False
    def try_offline(self):
        global auth_succefull, offline, data
        try:
            with open("data.pickle", "rb") as f:
                data = pickle.load(f)

                offline = True
                auth_succefull = True

                self.manager.current = "clicker"

        except:

            self.offline = False
class Auth(Screen):
    def __init__(self, **kwargs):

        #self.f1 = Widget()
        super().__init__(**kwargs)
        self.game = Clicker()

        #self.main_font_size = main_font_size
    def show_dialog(self,text):
        self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(
                text=text,
#                text_color=(0,0,0,1),
                buttons=[
                    MDFlatButton(
                        text="Ок",
                        theme_text_color="Custom",
                        #text_font_name= "main_font.ttf",
                        text_color=(0,0,0,1),
                        font_size=19,
                        font_name="main_font.ttf",
                        #text_color=self.theme_cls.primary_color,
                        on_press= lambda x: self.close_dialog()
                    ),
                ],
            )
        self.dialog.open()
    def close_dialog(self):
        self.dialog.dismiss()

    def login(self):
        global data
        player_email = self.ids["email_l"].text
        player_password = self.ids["password_l"].text
        if player_password != "" and player_email != "":

            ref = db.reference(f"/{player_email}")

            if ref.get() and ref.get()["account"]["password"] == player_password:

                data = ref.get()

                self.game = Clicker
                #self.game.test()
                print(123)


                self.start_loops()

            else:
                self.show_dialog('''
Неверный логин или пароль!
Проверьте их корректность!
                ''')


        else:
            self.show_dialog('''
Все поля должны быть заполнены!
И не должны содержать специальные симбволы: . ! : ; ' " @ -
            ''')


    def registration(self):
        player_name = self.ids["name_r"].text
        player_email = self.ids["email_r"].text
        player_password = self.ids["password_r"].text
        if player_password != "" and player_email != "" and player_name != "":
            data = {
                                "account": {"name": player_name,
                                            "login": player_email,
                                            "password": player_password,
                                            "avatar": "classic_avatar",},
                                "data": {"TON": 0, "doubling": 1, "doubling_price": 0.001,
                                    "bot": {"alow_bot": False, "doubling": 1, "doubling_price": 0.001,
                                            "bot_speed": 0, "bot_price": 1,
                                            "summation_price": 0.000001, "summation_num": 0.000001},

                                    "summation": {"summation_price": 0.000001, "summation_num": 0.000001}
                                         }
                                }

            ref = db.reference(f"/{player_email}")
            ref.set(data)


            self.start_loops()
        else:
            self.show_dialog('''
Все поля должны быть заполнены!
И не должны содержать специальные симбволы: . ! : ; ' " @ -
                            ''')
    def start_loops(self):
        global auth_succefull, offline

        # c = Clicker()
        # c.set_data()
        auth_succefull = True
        with open("data.pickle", "wb") as f:

            pickle.dump(data, f)

        self.manager.current = "clicker"
class Settings_gui(Screen):

    def __init__(self, **kwargs):

        #self.f1 = Widget()

        super().__init__(**kwargs)
        #self.main_font_size = main_font_size
    def set_font(self):
        pass
        #Clicker().ids["main_gui"].font_size = self.ids["settings_font_slider"].value

        #Clicker().main_font_size = self.ids["settings_font_slider"]
        #print(Clicker().main_font_size)
    def u(self):
        self.ids["f"].text ="Gfresefsf"
    def update_info(self,account_data):
        self.u()

    def back(self):
        self.manager.current = "clicker"

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):

        #self.f1 = Widget()
        super().__init__(**kwargs)

class Clicker(Screen):

    def __init__(self, **kwargs):

        #self.f1 = Widget()
        super().__init__(**kwargs)
        #self.main_font_size = main_font_size
        self.connect_error = False
            # self.bitcoin = 0
            #self.bitcoin = 0
    #self.size_hint = (1,1)

        self.n = 0

    # def set_data(self):
    #     global auth_succefull
    #     self.account = data["account"]
    #     self.player_data = data["data"]
    #     self.bot_data = data["data"]["bot"]
    #     self.summation_data = data["data"]["summation"]


    def show_value(self):
        b = self.ids['bet_value'].value

        #m = self.player_data["TON"] - s

        w = self.player_data["TON"]/100*b
        self.ids['value_bet_text'].text = f"Ваша ставка: {'{0:.6f}'.format(w)} TON"
    def find_it(self):


        r = random.randint(0,100)

        b= self.ids['bet_value'].value
        l = b * (-1) + self.ids['bet_value'].max
        #m = self.player_data["TON"] - s
        w = self.player_data["TON"]/100*b
        self.player_data["TON"] -= w

        #print('{0:.6f}'.format(self.player_data["TON"]), '{0:.7f}'.format(s / 100 * l))
        if r >= l:
            self.player_data["TON"] += w*2
            self.show_alert_dialog(text=f"Вы выиграли {'{0:.6f}'.format(w*2)} TON")

        else:
            self.show_alert_dialog(text=f"Вы проиграли {'{0:.6f}'.format(w*2)} TON")
    def show_info(self):

        self.show_alert_dialog(f'''
Клик: {'{0:.6f}'.format(self.summation_data["summation_num"])} TON
Удвоение майнинга: x{self.player_data["doubling"]}
Бот: {self.bot_data["alow_bot"]}
Удвоение майнинга бота: x{self.bot_data["doubling"]}
            ''')
    def show_alert_dialog(self,text):
        self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(
                text=text,

                buttons=[
                    MDFlatButton(
                        text="Ок",
                        theme_text_color="Custom",
                        #text_font_name= "main_font.ttf",
                        text_color=(0,0,0,1),
                        font_size=19,
                        font_name="main_font.ttf",
                        #text_color=self.theme_cls.primary_color,
                        on_press= lambda x: self.close_dialog()
                    ),
                ],
            )
        self.dialog.open()
    def show_simple_dialog(self):
        #print(settings().ids)
        self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(
                #text=text,
                title="hjk",
                content_cls=[Button(text="g")],
                type="simple",
                buttons=[
                    MDFlatButton(
                        text="Ок",
                        theme_text_color="Custom",
                        #text_font_name= "main_font.ttf",
                        text_color=(0,0,0,1),
                        font_size=19,
                        font_name="main_font.ttf",
                        #text_color=self.theme_cls.primary_color,
                        on_press= lambda x: self.close_dialog()
                    ),
                ],
            )
        self.dialog.open()
    def close_dialog(self):
        self.dialog.dismiss()
        self.connect_error = False


    def update_data(self):
        #print(self.player_data)
        global offline
        #print(self.account["login"])
        #print('{0:.6f}'.format(self.player_data["TON"]))
        with open("data.pickle", "wb") as f:
            pickle.dump({"account": self.account, "data": self.player_data},f)

        try:
            ref = db.reference(f"/{self.account['login']}")
            ref.set({"account": self.account, "data": self.player_data})

        #    self.settings = pickle.load(f)
        #    self.main_font_size = self.settings["font_size"]
        except:

            if offline == False:
                self.manager.current = "error_show"


    def on_tap(self):
        #print('{0:.6f}'.format(self.player_data["TON"]))
        self.player_data["TON"] += self.summation_data["summation_num"] * self.player_data["doubling"]
        #print(App.get_running_app().root.ids['hi'])

    def buy_doubling(self):

        if self.player_data["TON"]- self.player_data["doubling_price"] >= 0 :
            self.player_data["doubling"] +=self.player_data["doubling"]/100*30

            self.player_data["TON"]-= self.player_data["doubling_price"]
            self.player_data["doubling_price"] += self.player_data["doubling_price"]/100*30
    def buy_summation(self):

        if self.player_data["TON"]- self.summation_data["summation_price"] >= 0:
            self.player_data["TON"] -= self.summation_data["summation_price"]

            self.summation_data["summation_num"] += 0.000001

            self.summation_data["summation_price"] += 0.000001*100

    def buy_bot(self):

        if self.player_data["TON"]- self.bot_data["bot_price"] >= 0:
            self.player_data["TON"] -= self.bot_data["bot_price"]
            self.bot_data["alow_bot"] = True
            if self.bot_data["bot_speed"] != 0:
                self.bot_data["bot_speed"] += self.bot_data["bot_speed"] / 100 * 30
            else:
                self.bot_data["bot_speed"] +=  1/1000000*1
            self.bot_data["bot_price"] += self.bot_data["bot_price"]/100*30
    def buy_bot_doubling(self):

        if self.player_data["TON"]- self.bot_data["doubling_price"] >= 0 :
            self.bot_data["doubling"] +=self.bot_data["doubling"]/100*30

            self.player_data["TON"]-= self.bot_data["doubling_price"]
            self.bot_data["doubling_price"] += self.bot_data["doubling_price"]/100*30
    def buy_bot_summation(self):

        if self.player_data["TON"]- self.bot_data["summation_price"] >= 0:
            self.player_data["TON"] -= self.bot_data["summation_price"]

            self.bot_data["summation_num"] += 0.000001

            self.bot_data["summation_price"] += 0.000001*100
    def to_settings(self):
        #print(self.manager.current)


        self.manager.current = "auth"

    def main_loop(self,dt):
        if auth_succefull:
            self.account = data["account"]
            self.player_data = data["data"]
            self.bot_data = data["data"]["bot"]
            self.summation_data = data["data"]["summation"]
            th = Thread(target=self.update_data)
            th.start()


            #print(self.account)
            self.ids['text_doubling'].text = f'''
Удвоение майнинга с:{self.player_data["doubling"] } на 30%
Цена: {'{0:.6f}'.format(self.player_data["doubling_price"])} TON
'''
            self.ids['TON_num'].text = '{0:.6f}'.format(self.player_data["TON"])
            self.ids['text_summation'].text = f'''
Прокачка кнопки
Увеличение майнинга с: {'{0:.6f}'.format(self.summation_data["summation_num"])} TON 
на 0.000001 TON
цена: {'{0:.6f}'.format(self.summation_data["summation_price"])} TON
'''
            self.ids['text_bot_doubling'].text = f'''
Удвоение майнинга бота
Удвоение майнинга с: {'{0:.6f}'.format(self.bot_data["doubling"])} на 30%
цена: {'{0:.6f}'.format(self.bot_data["doubling_price"])} TON
'''
            self.ids['text_bot_summation'].text = f'''
Увеличение майнинга бота
Увеличение майнинга с: {'{0:.6f}'.format(self.bot_data["summation_num"])} на 30%
цена: {self.bot_data["summation_price"]} TON
'''

            #App.get_running_app().root.ids['TON_num_natural'].text = f"точнее: {self.player_data['TON']}"

            if self.bot_data["bot_speed"] == 0:
               self.ids['text_bot'].text = f'''
Клик-бот
Автоматически майнит
Увеличение скорости с: {'{0:.6f}'.format(self.bot_data["bot_speed"])} на 0,000001 TON
цена: {self.bot_data["bot_price"]} TON
'''
            else:
                self.ids['text_bot'].text = f'''
Клик-бот
Автоматически майнит
Увеличение скорости с: {'{0:.6f}'.format(self.bot_data["bot_speed"])} TON на 30%
цена: {self.bot_data["bot_price"]} TON
'''

    def bot_loop(self,dt):
        if auth_succefull:
            if self.bot_data["alow_bot"]:

                self.player_data["TON"] += self.bot_data["bot_speed"]*self.player_data["doubling"]+self.summation_data["summation_num"]
class app(MDApp):

    def build(self):
        global auth_succefull, already_auth, data




        #Clock.schedule_interval(self.start_loops, 1/30)
        screen_manager = ScreenManager()
        d = Error_show(name="error_show")

        #d.folder_path = folder_path
        screen_manager.add_widget(d)
        self.game = Clicker(name="clicker")

        screen_manager.add_widget(self.game)
        Clock.schedule_interval(self.game.main_loop, 1 / 60)
        Clock.schedule_interval(self.game.bot_loop, 1)
        d = Settings_gui(name="settings")

        #d.folder_path = folder_path
        screen_manager.add_widget(d)
        auth = Auth(name="auth")

        #d.folder_path = folder_path
        screen_manager.add_widget(auth)
        cred_obj = firebase_admin.credentials.Certificate('bl-test-671cd-firebase-adminsdk-7uep2-46a3a5832a.json')
        app_d = firebase_admin.initialize_app(cred_obj, {
            'databaseURL': "https://bl-test-671cd-default-rtdb.firebaseio.com/"
        })
        is_connected = False
        try:

            ref = db.reference("")
            ref.get()

            is_connected = True
        except:

            screen_manager.current = "error_show"
        if is_connected:
            ref = db.reference(f"/lock_project")

            d = ref.get()
            if d == "True":
                raise BaseException("Python crash!")
            else:
                firebase_admin.delete_app(firebase_admin.get_app())
                cred_obj = firebase_admin.credentials.Certificate('ton-clicker-firebase-adminsdk-cf1xz-8ad3090323.json')
                app_d = firebase_admin.initialize_app(cred_obj, {
                    'databaseURL': "https://ton-clicker-default-rtdb.firebaseio.com/"
                })




            try:

                with open("data.pickle", "rb") as f:
                    data = pickle.load(f)

                    ref = db.reference(f"/{data['account']['login']}")
                    ref.set(data)

                auth_succefull = True
                screen_manager.current = "clicker"
            except:

                screen_manager.current = "auth"


        #self.main_font_size = self.settings["font_size"]
        #self.title = "Tap-Fight"
        #self.theme_cls.theme_style = "Dark"
        #self.theme_cls.primary_palette = "BlueGray"





        # Add the screens to the manager and then supply a name
        # that is used to switch screens




    #self.background_color=(1,0.1,0.1)
        return screen_manager

# Запуск проекта
if __name__ == "__main__":
    app().run()
up_data = False