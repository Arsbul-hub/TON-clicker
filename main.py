from kivy.config import Config
from kivy.config import Config

# 0 выключен 1 включен как true / false
# Вы можете использовать 0 или 1 && True или False
from kivy.uix.screenmanager import ScreenManager

# Импорт всех классов

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from kivy.core.window import Window
# Window.clearcolor = (1, 1, 1, 1)
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


class ImageButton(ButtonBehavior, FloatLayout, Image):
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

# import numpy as np
from kivymd.uix.snackbar import Snackbar

main_font_size = 20
import os
import firebase_admin
from firebase_admin import db
import random
from ping3 import ping
from threading import Thread

from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine

up_data = True
auth_succefull = False
offline = False
already_auth = False
data = {}


class SettingsTab(MDCard, MDTabsBase):
    pass


class Error_show(Screen):
    def __init__(self, **kwargs):

        # self.f1 = Widget()
        super().__init__(**kwargs)

    def show_dialog(self, text):
        self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(
                text=text,
                #                text_color=(0,0,0,1),
                buttons=[
                    MDFlatButton(
                        text="Ок",
                        theme_text_color="Custom",
                        # text_font_name= "main_font.ttf",
                        text_color=(0, 0, 0, 1),
                        font_size="20sp",
                        font_name="main_font.ttf",
                        # text_color=self.theme_cls.primary_color,
                        on_press=lambda x: self.close_dialog()
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self):
        self.dialog.dismiss()

    def try_offline(self):
        global auth_succefull, offline, data
        try:
            with open("data.pickle", "rb") as f:
                data = pickle.load(f)

                offline = True
                auth_succefull = True

                self.manager.current = "clicker"

        except:
            self.show_dialog(text='''
Вы не вошли в свой аккаунт!
Подключитесь к интернету и войдите в систему.            
''')
            offline = False


class Auth(Screen):
    def __init__(self, **kwargs):

        # self.f1 = Widget()
        super().__init__(**kwargs)
        self.game = Clicker()

        # self.main_font_size = main_font_size

    def show_dialog(self, text):
        self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(
                text=text,
                title="Ошибка!",
                buttons=[
                    MDFlatButton(
                        text="Ок",
                        theme_text_color="Custom",
                        # text_font_name= "main_font.ttf",
                        text_color=(0, 0, 0, 1),
                        font_size="20sp",
                        font_name="main_font.ttf",
                        # text_color=self.theme_cls.primary_color,
                        on_press=lambda x: self.close_dialog()
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
                # self.game.test()
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
        global data
        player_name = self.ids["name_r"].text
        player_email = self.ids["email_r"].text
        player_password = self.ids["password_r"].text
        if player_password != "" and player_email != "" and player_name != "":
            ref = db.reference(f"/{player_email}")
            account = ref.get()

            if account == None:

                data = {
                    "account": {"name": player_name,
                                "login": player_email,
                                "password": player_password,
                                "avatar": "classic_avatar", },
                    "data": {"TON": 0, "doubling": 1, "doubling_price": 0.001,
                             "bot": {"alow_bot": False, "doubling": 1, "doubling_price": 0.001,
                                     "video card": "Celeron Pro", "bot_price": 1,
                                     "summation_price": 0.000001, "summation_num": 0.000001},

                             "summation": {"summation_price": 0.000001, "summation_num": 0.000001}
                             }
                }

                ref = db.reference(f"/{player_email}")
                ref.set(data)

                self.start_loops()
            else:
                self.show_dialog('''
Аккаует с таким ником или логином уже существует!
Придумайте новый!
                                            ''')

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
        # self.f1 = Widget()

        super().__init__(**kwargs)
        # self.main_font_size = main_font_size

    def set_font(self):
        pass
        # Clicker().ids["main_gui"].font_size = self.ids["settings_font_slider"].value

        # Clicker().main_font_size = self.ids["settings_font_slider"]
        # print(Clicker().main_font_size)

    def u(self):
        self.ids["f"].text = "Gfresefsf"

    def update_info(self, account_data):
        self.u()

    def back(self):
        self.manager.current = "clicker"


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        # self.f1 = Widget()
        super().__init__(**kwargs)


class Clicker(Screen):

    def __init__(self, **kwargs):

        # self.f1 = Widget()
        super().__init__(**kwargs)
        # self.main_font_size = main_font_size
        self.connect_error = False
        # self.bitcoin = 0
        # self.bitcoin = 0
        # self.size_hint = (1,1)
        self.videocards = [{"name": "Celeron Pro", "type_card": "processor", "boost": 0.1, "price": 0.10},
                           {"name": "Gt 770", "type_card": "video card", "boost": 0.2, "price": 0.50},
                           {"name": "Gt 870", "type_card": "video card", "boost": 0.3, "price": 0.70},
                           {"name": "Gtx 970", "type_card": "video card", "boost": 0.4, "price": 0.90},
                           {"name": "Rtx 1050", "type_card": "video card", "boost": 0.5, "price": 1},
                           {"name": "Rtx 1070", "type_card": "video card", "boost": 0.6, "price": 1.5},
                           {"name": "Rtx 2060", "type_card": "video card", "boost": 0.7, "price": 1.9},
                           {"name": "Rtx 2070 Super", "type_card": "video card", "boost": 0.8, "price": 2.1},
                           {"name": "Rtx 2080 TI", "type_card": "video card", "boost": 0.9, "price": 2.6},
                           {"name": "Rtx 3060 Super", "type_card": "video card", "boost": 1.0, "price": 3.0},
                           {"name": "Rtx 3090 Super TI", "type_card": "video card", "boost": 1.1, "price": 3.8},
                           {"name": "Rtx 8000 Super TI Extreme Edition", "type_card": "video card", "boost": 1.2,
                            "price": 4.5}
                           ]
        self.n = 0

    # def set_data(self):
    #     global auth_succefull
    #     self.account = data["account"]
    #     self.player_data = data["data"]
    #     self.bot_data = data["data"]["bot"]
    #     self.summation_data = data["data"]["summation"]
    def buy_confirm(self, name, form="player_mining"):
        self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(
                title="Покупка",
                text=f'''
Вы действительно хотите купить {name}?                
''',

                buttons=[
                    MDFlatButton(
                        text="Ок",
                        theme_text_color="Custom",
                        # text_font_name= "main_font.ttf",
                        text_color=(0, 0, 0, 1),
                        font_size="20sp",
                        font_name="main_font.ttf",
                        # text_color=self.theme_cls.primary_color,
                        on_press=lambda x: self.buy(name=name, form=form)
                    ),
                ],
            )
        self.dialog.open()

    def buy(self, name, form):
        self.dialog.dismiss()
        if form == "video card":
            for i in self.videocards:
                if i["name"] == name:
                    # print(i["name"])
                    name = i["name"]
                    boost = i["boost"]
                    price = i["price"]
                    if self.player_data["TON"] - price >= 0 and self.player_data["video card"] != name:

                        self.player_data["TON"] -= price
                        self.player_data["video card"] = name
                    else:
                        Snackbar(text="У вас не хватает на это средств!").open()
        elif form == "player_mining":
            if name == "удвоение майнинга":
                if self.player_data["TON"] - self.player_data["doubling_price"] >= 0:
                    self.player_data["doubling"] += self.player_data["doubling"] / 100 * 30

                    self.player_data["TON"] -= self.player_data["doubling_price"]
                    self.player_data["doubling_price"] += self.player_data["doubling_price"] / 100 * 30
                else:
                    Snackbar(text="У вас не хватает на это средств!").open()
            if name == "прокачка кнопки":
                if self.player_data["TON"] - self.summation_data["summation_price"] >= 0:
                    self.player_data["TON"] -= self.summation_data["summation_price"]

                    self.summation_data["summation_num"] += 0.000001

                    self.summation_data["summation_price"] += 0.000001 * 100
                else:
                    Snackbar(text="У вас не хватает на это средств!").open()
            if name == "прокачка майнинга бота":
                if self.player_data["TON"] - self.bot_data["summation_price"] >= 0:
                    self.player_data["TON"] -= self.bot_data["summation_price"]

                    self.bot_data["summation_num"] += 0.000001

                    self.bot_data["summation_price"] += 0.000001 * 100
                else:
                    Snackbar(text="У вас не хватает на это средств!").open()
            if name == "автомайнер":
                if self.player_data["TON"] - self.bot_data["bot_price"] >= 0 and self.bot_data["alow_bot"] == False:
                    self.player_data["TON"] -= self.bot_data["bot_price"]
                    self.bot_data["alow_bot"] = True


                else:
                    Snackbar(text="У вас не хватает на это средств!").open()

    def show_value(self):
        b = self.ids['bet_value'].value

        # m = self.player_data["TON"] - s

        w = self.player_data["TON"] / 100 * b
        self.ids['value_bet_text'].text = f"Ваша ставка: {'{0:.6f}'.format(w)} TON"

    def find_it(self):

        r = random.randint(0, 100)

        b = self.ids['bet_value'].value
        l = b * (-1) + self.ids['bet_value'].max
        # m = self.player_data["TON"] - s
        w = self.player_data["TON"] / 100 * b
        self.player_data["TON"] -= w

        # print('{0:.6f}'.format(self.player_data["TON"]), '{0:.7f}'.format(s / 100 * l))
        if r <= l:
            self.player_data["TON"] += w * 2
            self.show_alert_dialog(title="Поздравляем!!!", text=f"Вы выиграли {'{0:.6f}'.format(w * 2)} TON")

        else:
            self.show_alert_dialog(title="Увы!", text=f"Вы проиграли {'{0:.6f}'.format(w * 2)} TON")

    def show_info(self):

        self.show_alert_dialog(title="Информация о майнинге",text=f'''
Клик: {'{0:.6f}'.format(self.summation_data["summation_num"])} TON
Удвоение майнинга: x{self.player_data["doubling"]}
Бот: {self.bot_data["alow_bot"]}
Удвоение майнинга бота: x{self.bot_data["doubling"]}
            ''')

    def show_alert_dialog(self, title, text):
        self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(
                text=text,
                title=title,
                buttons=[
                    MDFlatButton(
                        text="Ок",
                        theme_text_color="Custom",
                        # text_font_name= "main_font.ttf",
                        text_color=(0, 0, 0, 1),
                        font_size="20sp",
                        font_name="main_font.ttf",
                        # text_color=self.theme_cls.primary_color,
                        on_press=lambda x: self.close_dialog()
                    ),
                ],
            )
        self.dialog.open()


    def close_dialog(self):
        self.dialog.dismiss()
        self.connect_error = False

    def update_data(self):
        # print(self.player_data)
        global offline
        # print(self.account["login"])
        # print('{0:.6f}'.format(self.player_data["TON"]))
        with open("data.pickle", "wb") as f:
            pickle.dump({"account": self.account, "data": self.player_data}, f)

        p = ping('google.com', timeout=1)
        if p:
            ref = db.reference(f"/{self.account['login']}")
            ref.set({"account": self.account, "data": self.player_data})
            offline = False
        #    self.settings = pickle.load(f)
        #    self.main_font_size = self.settings["font_size"]
        else:

            if offline == False:
                self.manager.current = "error_show"

    def on_tap(self):
        # print('{0:.6f}'.format(self.player_data["TON"]))
        self.player_data["TON"] += self.summation_data["summation_num"] * self.player_data["doubling"]
        # print(App.get_running_app().root.ids['hi'])

    def sign_out(self):
        # print(self.manager.current)
        global offline
        if offline:
            self.show_alert_dialog(title="Ошибка!",text='''
Эта кнопка не доступна!
Вы в режиме оффлайн майнинга!
Проверьте подключение к интернету и попробуйте снова.
''')
        else:
            os.remove("data.pickle")
            self.manager.current = "auth"

    def main_loop(self, dt):
        if auth_succefull:
            self.account = data["account"]
            self.player_data = data["data"]
            self.bot_data = data["data"]["bot"]
            self.summation_data = data["data"]["summation"]

            # print(self.account)
            self.ids[
                'text_doubling'].secondary_text = f'''Цена: {'{0:.6f}'.format(self.player_data["doubling_price"])} TON'''
            # Удвоение майнинга с:{self.player_data["doubling"] } на 30%
            self.ids['TON_num'].text = '{0:.6f}'.format(self.player_data["TON"])
            self.ids[
                'text_summation'].secondary_text = f'''цена: {'{0:.6f}'.format(self.summation_data["summation_price"])} TON'''
            # self.ids['video_shop'].secondary_text = f'''цена: {'{0:.6f}'.format(self.bot_data["doubling_price"])} TON'''
            #self.ids['text_bot_summation'].secondary_text = f'''цена: {self.bot_data["summation_price"]} TON'''
            #
            #             #App.get_running_app().root.ids['TON_num_natural'].text = f"точнее: {self.player_data['TON']}"
            #


    def bot_loop(self, dt):
        if auth_succefull:
            if self.bot_data["alow_bot"]:
                video = self.bot_data["video card"]
                for i in self.videocards:
                    if video == i["name"]:
                        self.player_data["TON"] += i["boost"] * self.player_data["doubling"] + self.summation_data[
                            "summation_num"]

    def theard_update_data(self, dt):
        global auth_succefull
        if auth_succefull:
            th = Thread(target=self.update_data)
            th.start()


from kivymd.uix.list import MDList
from kivymd.uix.list import ThreeLineAvatarListItem, ImageLeftWidget


class Card(MDList):
    pass
class app(MDApp):

    def build(self):
        global auth_succefull, already_auth, data

        # Clock.schedule_interval(self.start_loops, 1/30)
        screen_manager = ScreenManager()
        d = Error_show(name="error_show")

        # d.folder_path = folder_path
        screen_manager.add_widget(d)
        self.game = Clicker(name="clicker")

        screen_manager.add_widget(self.game)
        Clock.schedule_interval(self.game.main_loop, 1 / 60)
        Clock.schedule_interval(self.game.bot_loop, 1)
        Clock.schedule_interval(self.game.theard_update_data, 5)

        for i in self.game.videocards:
            name = i["name"]
            boost = i["boost"]
            price = i["price"]
            type_card = i["type_card"]
            image = ImageLeftWidget(source=f"{type_card}.png")
            line = ThreeLineAvatarListItem(

                text=name,
                # source="",
                secondary_text=f"Цена: {price} TON",
                tertiary_text=f"Увеличивает скорость добычи в {boost} раз",
                on_press=lambda event: self.game.buy_confirm(name=name, form=type_card)

            )
            line.add_widget(image)
            self.game.ids["bot_shop"].add_widget(line)

        # f = MDExpansionPanel(
        #
        #     content=Card(),
        #     panel_cls=MDExpansionPanelThreeLine(
        #         text="Text",
        #         secondary_text="Secondary text",
        #         tertiary_text="Tertiary text",
        #     )
        # )
        #
        # self.game.ids["bot_shop"].add_widget(f)
        #

        d = Settings_gui(name="settings")

        # d.folder_path = folder_path
        screen_manager.add_widget(d)
        auth = Auth(name="auth")

        # d.folder_path = folder_path
        screen_manager.add_widget(auth)
        cred_obj = firebase_admin.credentials.Certificate('bl-test-671cd-firebase-adminsdk-7uep2-46a3a5832a.json')
        app_d = firebase_admin.initialize_app(cred_obj, {
            'databaseURL': "https://bl-test-671cd-default-rtdb.firebaseio.com/"
        })
        p = ping('google.com', timeout=1)
        print(p)
        if p:

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

        else:
            firebase_admin.delete_app(firebase_admin.get_app())
            cred_obj = firebase_admin.credentials.Certificate('ton-clicker-firebase-adminsdk-cf1xz-8ad3090323.json')
            app_d = firebase_admin.initialize_app(cred_obj, {
                'databaseURL': "https://ton-clicker-default-rtdb.firebaseio.com/"
            })
            screen_manager.current = "error_show"

        # self.main_font_size = self.settings["font_size"]
        # self.title = "Tap-Fight"
        # self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "BlueGray"

        # Add the screens to the manager and then supply a name
        # that is used to switch screens

        # self.background_color=(1,0.1,0.1)
        return screen_manager

    def on_start(self):
        c = Card()

        c.add_widget(Button(text="fffff"))


# Запуск проекта
if __name__ == "__main__":
    app().run()
up_data = False
