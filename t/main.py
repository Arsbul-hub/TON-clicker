import webbrowser
from cloudipsp import Api, Checkout
from kivymd.uix.textfield import MDTextField


from kivy.uix.screenmanager import *

from kivy.clock import Clock
from kivmob import KivMob, RewardedListenerInterface
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.audio import SoundLoader
from kivymd.uix.list import TwoLineListItem
import pickle

from kivymd.uix.card import MDCard
from kivymd.uix.tab import MDTabsBase
from decimal import Decimal
from kivymd.uix.snackbar import Snackbar
from kivymd.app import MDApp

main_font_size = 20
import os

import firebase_admin
from firebase_admin import db
import random

from ping3 import ping
from threading import Thread
from kivy.logger import Logger

from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton

up_data = True
auth_succefull = False
offline = False
already_auth = False
data = {}

from kivymd.uix.button import MDRaisedButton

max_ping = 300
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label


def set_data():
    c = Clicker

    c.account = data["account"]
    c.player_data = data["data"]
    c.bot_data = data["data"]["bot"]
    c.doubling_data = data["data"]["doubling"]
    c.summation_data = data["data"]["summation"]






    # adaptive_width = True


class SettingsTab(MDCard, MDTabsBase):
    pass


# class RightLabel(IRightBodyTouch, MDLabel):
#     #pass
#     #text = StringProperty("rrr")
#     def __init__(self, **kwargs):
#
#         super().__init__(**kwargs)
#
#         #self.text = text
from kivy.uix.widget import Widget
class CustomLabel(Label):
    pass
class Error_show(Screen):
    def __init__(self, **kwargs):

        # self.f1 = Widget()
        super().__init__(**kwargs)

    def show_dialog(self, text):
        self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(
                title="Ошибка!",
                text=text,

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
        if self.dialog:
            self.dialog.dismiss()

    def try_offline(self):
        global auth_succefull, offline, data
        try:
            with open("data.pickle", "rb") as f:
                data = pickle.load(f)

                offline = True
                auth_succefull = True
                set_data()
                self.manager.current = "clicker"

        except:
            self.show_dialog(text='''
Вы не вошли в свой аккаунт!
Подключитесь к интернету и войдите в систему.            
''')
            offline = False

    def reconnect(self):

        global auth_succefull, data
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
        print(p)
        if p != False and p != None and p < max_ping:

            firebase_admin.delete_app(firebase_admin.get_app())
            cred_obj = firebase_admin.credentials.Certificate('ton-clicker-firebase-adminsdk-cf1xz-8ad3090323.json')
            app_d = firebase_admin.initialize_app(cred_obj, {
                'databaseURL': "https://ton-clicker-default-rtdb.firebaseio.com/"
            })

            try:
                with open("data.pickle", "rb") as f:
                    data = pickle.load(f)

                    ref = db.reference(f"/players/{data['account']['login']}")
                    ref.set(data)

                auth_succefull = True
                set_data()
                self.manager.current = "clicker"

            except:

                self.manager.current = "auth"


class Auth(Screen):
    def __init__(self, **kwargs):

        # self.f1 = Widget()
        super().__init__(**kwargs)

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
        if self.dialog:
            self.dialog.dismiss()

    def load_avatar(self, p):
        self.ids["avatar_image"].source = p

    def login(self):
        self.manager.current = "loading"
        th = Thread(target=self.start_login)
        th.start()

    def start_login(self):
        global data

        player_email = self.ids["email_l"].text
        player_password = self.ids["password_l"].text
        if player_password != "" and player_email != "":

            ref = db.reference(f"/players/{player_email}")
            # from kivymd.uix.navigationdrawer.MDNavigationDrawerHeader import MDNavigationDrawerHeader
            if ref.get() and ref.get()["account"]["password"] == player_password:

                data = ref.get()

                # self.game.test()
                # print(123)

                self.start_loops()

            else:
                self.manager.current = "auth"
                self.show_dialog('''
Неверный логин или пароль!
Проверьте их корректность!
''')


        else:
            self.manager.current = "auth"
            self.show_dialog('''
Все поля должны быть заполнены!
И не должны содержать специальные симбволы: . ! : ; ' " @ -
''')

    def registration(self):
        self.manager.current = "loading"
        th = Thread(target=self.start_registration)
        th.start()

    def start_registration(self):
        global data
        if self.ids["avatar"].text:
            avatar = self.ids["avatar"].text
        else:
            avatar = "classic_avatar.png"
        player_name = self.ids["name_r"].text
        player_email = self.ids["email_r"].text
        player_password = self.ids["password_r"].text
        if player_password != "" and player_email != "" and player_name != "" and "/" not in player_password and "/" not in player_email and "/" not in player_name:
            ref = db.reference(f"/players/{player_email}")
            account = ref.get()

            if account == None:

                data = {
                    "account": {"name": player_name,
                                "login": player_email,
                                "password": player_password,
                                "avatar": avatar,
                                "priv": None},
                    "data": {"TON": 0, "doubling": {"value": 1, "price": 0.001},
                             "bot": {"alow_bot": False, "doubling": {"value": 1, "doubling_price": 0.001},
                                     "video card": "Celeron Pro", "price": 1,
                                     "summation_price": 0.000001, "summation_num": 0.000001},

                             "summation": {"summation_price": 0.000001, "summation_num": 0.000001},
                             # "chest_last_opened": datetime(year=2021,month=1,day=1,hour=1,minute=1),
                             "chest": {"num": 1, "price": 0.000150},
                             "mouse": "Oklick 105S",
                             "tired_num": 40,
                             "is_tired": False,

                             }
                }

                # p = ping('ton-clicker-default-rtdb.firebaseio.com', unit="ms")

                ref = db.reference(f"/players/{player_email}")
                ref.set(data)

                self.start_loops()
            else:
                # self.manager.transition = NoTransition()
                self.manager.current = "auth"
                self.show_dialog('''
Аккаует с таким ником или логином уже существует!
Придумайте новый!
''')

        else:
            self.manager.current = "auth"
            self.show_dialog('''
Все поля должны быть заполнены!
И не должны содержать симбвол: /
''')

    def start_loops(self):
        global auth_succefull, offline, data

        # c = Clicker()
        # c.set_data()
        set_data()
        auth_succefull = True
        with open("data.pickle", "wb") as f:
            pickle.dump(data, f)

        # self.manager.transition = FadeTransition()
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


class Chest_content(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Buy_content(MDBoxLayout):
    def __init__(self, items=[], **kwargs):
        for i in items:
            pass
        super().__init__(**kwargs)

        # print(price, description)


class Clicker(Screen):
    # set_data()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.f1 = Widget()

        # Logger.info('Loader: Game screen has been loaded.')
        print(122222222222222222222222222)
        # self.main_font_size = main_font_size
        self.connect_error = False
        self.name = "clicker"
        # self.bitcoin = 0
        # self.bitcoin = 0
        # self.size_hint = (1,1)
        self.store_items = {
            "Celeron Pro": {"index": 0, "texture": "video card.png", "name": "Celeron Pro", "type": "processor",
                            "boost": 0.000001, "price": 0.10},
            "Gt 770": {"index": 1, "texture": "video card.png", "name": "Gt 770", "type": "video card",
                       "boost": 0.00002, "price": 0.50},
            "Gt 870": {"index": 2, "texture": "video card.png", "name": "Gt 870", "type": "video card",
                       "boost": 0.00003, "price": 0.70},
            "Gtx 970": {"index": 3, "texture": "video card.png", "name": "Gtx 970", "type": "video card",
                        "boost": 0.00004, "price": 0.90},
            "Rtx 1050": {"index": 4, "texture": "video card.png", "name": "Rtx 1050", "type": "video card",
                         "boost": 0.00005, "price": 1},
            "Rtx 1070": {"index": 5, "texture": "video card.png", "name": "Rtx 1070", "type": "video card",
                         "boost": 0.00006, "price": 1.5},
            "Rtx 2060": {"index": 6, "texture": "video card.png", "name": "Rtx 2060", "type": "video card",
                         "boost": 0.00007, "price": 1.9},
            "Rtx 2070 Super": {"index": 7, "texture": "video card.png", "name": "Rtx 2070 Super", "type": "video card",
                               "boost": 0.00008, "price": 2.1},
            "Rtx 2080 TI": {"index": 8, "texture": "video card.png", "name": "Rtx 2080 TI", "type": "video card",
                            "boost": 0.00009, "price": 2.6},
            "Rtx 3060 Super": {"index": 9, "texture": "video card.png", "name": "Rtx 3060 Super", "type": "video card",
                               "boost": 0.0015, "price": 3.0},
            "Rtx 3090 Super TI": {"index": 10, "texture": "video card.png", "name": "Rtx 3090 Super TI",
                                  "type": "video card", "boost": 0.0095, "price": 3.8},
            "Rtx 8000 Super TI Extreme Edition": {"index": 11, "texture": "video card.png",
                                                  "name": "Rtx 8000 Super TI Extreme Edition", "type": "video card",
                                                  "boost": 1.2, "price": 4.5},

            "Oklick 105S": {"index": 0, "texture": "mouse-variant", "type": "mouse", "name": "Oklick 105S",
                            "boost": 0.000001, "price": 0.000001, "tired": 1},
            "Canyon CNE-CMS05DG": {"index": 1, "texture": "mouse-variant", "type": "mouse",
                                   "name": "Canyon CNE-CMS05DG", "boost": 0.00001, "price": 0.0001, "tired": .9},
            "QUMO Office M14": {"index": 2, "texture": "mouse-variant", "type": "mouse", "name": "QUMO Office M14",
                                "boost": 0.00005, "price": 0.0003, "tired": .8},
            "Ritmix ROM-111": {"index": 3, "texture": "mouse-variant", "type": "mouse", "name": "Ritmix ROM-111",
                               "boost": 0.0001, "price": 0.004, "tired": .7},
            "Oklick 145M": {"index": 4, "texture": "mouse-variant", "type": "mouse", "name": "Oklick 145M",
                            "boost": 0.0005, "price": 0.02, "tired": .6},
            "Ritmix ROM-202": {"index": 5, "texture": "mouse-variant", "type": "mouse", "name": "Ritmix ROM-202",
                               "boost": 0.001, "price": 0.07, "tired": .5},
            "Smartbuy ONE SBM-265-K": {"index": 6, "texture": "mouse-variant", "type": "mouse",
                                       "name": "Smartbuy ONE SBM-265-K", "boost": 0.005, "price": 0.1, "tired": .4},

        }
        self.money = {
            "0.000050": {"type": "TON"},
            "0.000100": {"type": "TON"},
            "0.000150": {"type": "TON"},
            "0.000200": {"type": "TON"},
            "0.000250": {"type": "TON"},

        }
        self.bonuses = [self.money, self.store_items]
        self.n = 0
        # self.rewards = Rewards_Handler(self)
        # self.ads = KivMob("ca-app-pub-9371118693960899~5621013296")
        # print(TestIds.REWARDED_VIDEO)
        # self.ads.load_rewarded_ad("ca-app-pub-9371118693960899/9603139268")
        # Add any callback functionality to this class.

        self.ads = KivMob("ca-app-pub-9371118693960899~5621013296")
        self.ads.load_rewarded_ad("ca-app-pub-9371118693960899/7509498390")
        # Add any callback functionality to this class.
        self.ads.set_rewarded_ad_listener(RewardedListenerInterface())
        self.ads.on_rewarded_video_ad_completed = self.open_chest
        # def set_data(self):
        #     global auth_succefull
        #     self.account = data["account"]
        #     self.player_data = data["data"]
        #     self.bot_data = data["data"]["bot"]
        #     self.summation_data = data["data"]["summation"]

        self.toggled = False

    def show_video(self):
        self.ads.show_rewarded_ad()

    def load_video(self):
        self.ads.load_rewarded_ad("ca-app-pub-9371118693960899/7509498390")

    def buy_confirm(self, obj):
        name = obj.name
        print(name)
        self.dialog = None

        # if call == "video_card":
        #     price = self.videocards[name]["price"]
        # elif call == "mouse":
        #     price = self.mouses[name]["price"]
        # else:
        #     price = self.mouses[name]["price"]

        if not self.dialog:
            if name == "удвоение майнинга":

                b = BoxLayout(orientation="vertical")
                b.add_widget(CustomLabel(text=f'Цена: {self.doubling_data["price"]}',
                                   halign="center",
                                   font_name="main_font.ttf",
                                   font_size="25sp",

                                   # theme_text_color="Custom",
                                   #color=(0, 0, 0, 1),
                                   )
                             )

                b.add_widget(CustomLabel(
                    text=f'Увеличение умножения майнинга до {self.doubling_data["value"] + self.doubling_data["value"] / 100 * 30} раз',
                    halign="center",
                    font_name="main_font.ttf",
                    font_size="25sp",
                    #color=(0, 0, 0, 1),
                    # theme_text_color="Custom",
                    # text_color=(1,1,1,1)
                )
                )

                b2 = BoxLayout(spacing="5sp")
                b2.add_widget(
                    MDFillRoundFlatButton(text="Купить!", md_bg_color=(0.1, 0.6, 0.9, 1.0), font_name="main_font.ttf",
                                   size_hint=(.3, .2), font_size="25sp",
                                   on_press=lambda a: self.buy(name="удвоение майнинга")))
                b2.add_widget(MDFillRoundFlatButton(text="Отмена", md_bg_color=(0.1, 0.6, 0.9, 1.0), font_name="main_font.ttf",
                                             size_hint=(.3, .2), font_size="25sp",
                                             on_press=lambda a: self.close_dialog()))
                b.add_widget(b2)
                # b.add_widget(MDLabel(text="Описание: Увеличивает майнинг в x раз"))
                # Buy_content(price=self.doubling_data["price"], boost=f'Увеличение удвоения майнинга с {self.doubling_data["price"]} TON/клик до {self.doubling_data["value"] + self.doubling_data["value"] / 100 * 30} TON/клик', description="Увеличивает майнинг в x раз"),
                self.dialog = Popup(title=name.capitalize(), title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                                    title_align="center", title_size="30sp", content=b,
                                    size_hint=(.9 ,.7), background="dialog.png")
                # self.dialog = MDDialog(
                #     title="Покупка",
                #     #type="custom",
                #     size=(None,None),
                #     size_hint=(.9,.9),
                #     #content_cls=Buy_content(price=self.doubling_data["price"], boost=f'Увеличение удвоения майнинга с {self.doubling_data["price"]} TON/клик до {self.doubling_data["value"] + self.doubling_data["value"] / 100 * 30} TON/клик', description="Увеличивает майнинг в x раз"),
                #
                #     buttons=[
                #         MDFlatButton(
                #             text="Отмена",
                #             theme_text_color="Custom",
                #             # text_font_name= "main_font.ttf",
                #             text_color=(0, 0, 0, 1),
                #             font_size="20sp",
                #             font_name="main_font.ttf",
                #             # text_color=self.theme_cls.primary_color,
                #             on_press=lambda event: self.close_dialog()
                #         ),
                #
                #     ],
                # )
            elif name == "автомайнер":

                f = FloatLayout()
                b = MDBoxLayout(orientation="vertical")

                b.add_widget(CustomLabel(text=f'Цена: {"{0:.6f}".format(self.bot_data["price"])} TON',
                                   halign="center",
                                   #color=(0, 0, 0, 1),
                                   font_name="main_font.ttf",
                                   font_size="25sp", ))
                b.add_widget(CustomLabel(
                    text=f'Для втоматической добычи валюты требуется видеокарта',
                    halign="center",
                    #text_size=,
                    #size=b.texture_size,
                    #color=(0, 0, 0, 1),
                    font_name="main_font.ttf",
                    font_size="25sp" ))
                # Label:
                # text_size: root.width, None
                # size: self.texture_size
                # f.add_widget(b)
                b2 = BoxLayout(spacing="5sp")
                b2.add_widget(
                    MDFillRoundFlatButton(text="Купить!", md_bg_color=(0.1, 0.6, 0.9, 1.0), font_name="main_font.ttf",
                                   size_hint=(.3, .2), font_size="25sp",
                                   on_press=lambda a: self.buy(name=name)))
                b2.add_widget(MDFillRoundFlatButton(text="Отмена", md_bg_color=(0.1, 0.6, 0.9, 1.0), font_name="main_font.ttf",
                                             size_hint=(.3, .2), font_size="25sp",
                                             on_press=lambda a: self.close_dialog()))
                b.add_widget(b2)
                # f.add_widget(b)

                # b.add_widget(MDMDLabel(text="Описание: Увеличивает майнинг в x раз"))
                # Buy_content(price=self.doubling_data["price"], boost=f'Увеличение удвоения майнинга с {self.doubling_data["price"]} TON/клик до {self.doubling_data["value"] + self.doubling_data["value"] / 100 * 30} TON/клик', description="Увеличивает майнинг в x раз"),
                self.dialog = Popup(title=name.capitalize(), title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                                    title_align="center", title_size="30sp", content=b,
                                    size_hint=(.9, .7), background="dialog.png")
            elif name in self.store_items and self.store_items[name]["type"] == "video card":

                f = FloatLayout()
                b = BoxLayout(orientation="vertical")

                b.add_widget(CustomLabel(text=f'Цена: {"{0:.6f}".format(self.store_items[name]["price"])}',
                                   halign="center",
                                   #color=(0, 0, 0, 1),
                                   font_name="main_font.ttf",
                                   font_size="25sp", ))
                b.add_widget(CustomLabel(
                    text=f'Скорость: {"{0:.6f}".format(self.store_items[name]["boost"])} TON/сек',
                    halign="center",
                    #color=(0, 0, 0, 1),
                    font_name="main_font.ttf",
                    font_size="25sp", ))

                # f.add_widget(b)
                b2 = BoxLayout(spacing="5sp")
                b2.add_widget(
                    MDFillRoundFlatButton(text="Купить!", md_bg_color=(0.1, 0.6, 0.9, 1.0), font_name="main_font.ttf",
                                   size_hint=(.3, .2), font_size="25sp",
                                   on_press=lambda a: self.buy(name=name)))
                b2.add_widget(MDFillRoundFlatButton(text="Отмена", md_bg_color=(0.1, 0.6, 0.9, 1.0), font_name="main_font.ttf",
                                             size_hint=(.3, .2), font_size="25sp",
                                             on_press=lambda a: self.close_dialog()))
                b.add_widget(b2)
                # f.add_widget(b)

                # b.add_widget(MDMDLabel(text="Описание: Увеличивает майнинг в x раз"))
                # Buy_content(price=self.doubling_data["price"], boost=f'Увеличение удвоения майнинга с {self.doubling_data["price"]} TON/клик до {self.doubling_data["value"] + self.doubling_data["value"] / 100 * 30} TON/клик', description="Увеличивает майнинг в x раз"),
                self.dialog = Popup(title=name, title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                                    title_align="center", title_size="30sp", content=b,
                                    size_hint=(.9, .7), background="dialog.png")
            elif name in self.store_items and self.store_items[name]["type"] == "mouse":
                f = FloatLayout()
                b = MDBoxLayout(orientation="vertical")

                b.add_widget(CustomLabel(text=f'Цена: {"{0:.6f}".format(self.store_items[name]["price"])}',
                                   halign="center",
                                   #color=(0, 0, 0, 1),
                                   font_name="main_font.ttf",
                                   font_size="25sp", ))
                b.add_widget(CustomLabel(
                    text=f'Скорость: {"{0:.6f}".format(self.store_items[name]["boost"])} TON/клик',
                    halign="center",
                    #color=(0, 0, 0, 1),
                    font_name="main_font.ttf",
                    font_size="25sp", ))
                b.add_widget(CustomLabel(
                    text=f'Склонность к усталости: {int(self.store_items[name]["tired"] * 100)}%',
                    halign="center",
                    #color=(0, 0, 0, 1),
                    font_name="main_font.ttf",
                    font_size="25sp", ))
                # f.add_widget(b)
                b2 = BoxLayout(spacing="5sp")
                b2.add_widget(MDFillRoundFlatButton(text="Купить!", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                             on_press=lambda a: self.buy(name=name), font_name="main_font.ttf",
                                             size_hint=(.3, .2), font_size="25sp"))
                b2.add_widget(MDFillRoundFlatButton(text="Отмена", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                             on_press=lambda a: self.close_dialog(), font_name="main_font.ttf",
                                             size_hint=(.3, .2), font_size="25sp"))
                b.add_widget(b2)
                # f.add_widget(b)

                # b.add_widget(MDLabel(text="Описание: Увеличивает майнинг в x раз"))
                # Buy_content(price=self.doubling_data["price"], boost=f'Увеличение удвоения майнинга с {self.doubling_data["price"]} TON/клик до {self.doubling_data["value"] + self.doubling_data["value"] / 100 * 30} TON/клик', description="Увеличивает майнинг в x раз"),
                self.dialog = Popup(title=name, title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                                    title_align="center", title_size="30sp", content=b,
                                    size_hint=(.9, .7), background="dialog.png")
            # self.dialog = MDDialog(
            #     title="Покупка",
            #     type="custom",
            #     content_cls=Buy_content(price=self.bot_data["price"],
            #                             description="Для атоматической добычи TON вам нужно купить видеокарту!"),
            #
            #     buttons=[
            #         MDFlatButton(
            #             text="Отмена",
            #             theme_text_color="Custom",
            #             # text_font_name= "main_font.ttf",
            #             text_color=(0, 0, 0, 1),
            #             font_size="20sp",
            #             font_name="main_font.ttf",
            #             # text_color=self.theme_cls.primary_color,
            #             on_press=lambda event: self.close_dialog()
            #         ),
            #
            #     ],
            # )
        if self.dialog:
            self.dialog.open()

    def chest_panel(self):
        self.dialog = None

        if not self.dialog:
            # self.dialog = (screen=Factory.Chest_content())
            # self.dialog.add_item(text="video",callback=lambda event: self.ads.show_rewarded_ad())
            # self.dialog.add_item(text="TON", callback=lambda event: self.buy(name="chest"))
            # b = MDBoxLayout(orientation="vertical")
            #
            # b.add_widget(Button(text=f"Открыть за {self.player_data['chest']['price']} TON",
            #                        on_press=lambda event: self.buy(name="chest")))
            # b.add_widget(Button(text="Открыть, посмотрев видео", on_press=self.show_video))
            self.dialog = Popup(title="Открыть сундук?", title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                                title_align="center", title_size="30sp", content=Chest_content(),
                                size_hint=(.9, .5), background="dialog.png")
            # self.dialog = MDDialog(
            #     title="Открыть сундук?",
            #     # text="Открыть сундук?"
            #
            #     type="custom",
            #     content_cls=Chest_content(),
            #
            #     buttons=[
            #         MDFlatButton(
            #             text="Отмена",
            #             theme_text_color="Custom",
            #             # text_font_name= "main_font.ttf",
            #             text_color=(0, 0, 0, 1),
            #             font_size="20sp",
            #             font_name="main_font.ttf",
            #             # text_color=self.theme_cls.primary_color,
            #             on_press=lambda event: self.close_dialog()
            #         ),
            #
            #     ],
            # )
        self.dialog.open()

    def buy(self, name):
        if self.dialog:
            self.dialog.dismiss()

        if name in self.store_items:
            video = self.bot_data["video card"]
            index = self.store_items[video]["index"]
            price = self.store_items[name]["price"]

            if index < self.store_items[name]["index"]:
                if self.player_data["TON"] - price >= 0 and video != name:

                    self.player_data["TON"] -= price
                    self.bot_data["video card"] = name
                elif self.player_data["TON"] - price <= 0:
                    Snackbar(text="У вас не хватает на это валюты!", duration=.2).open()
            elif index > self.store_items[name]["index"]:
                Snackbar(text="Эта видеокарта хуже, чем у вас есть!", duration=.2).open()
            elif index == self.store_items[name]["index"]:
                Snackbar(text="У вас уже усть эта !", duration=.2).open()
        # elif name in self.mouses:видеокарта
        #     button = self.player_data["mouse"]
        #     index = self.mouses[button]["index"]
        #     price = self.mouses[name]["price"]
        #     if index < self.mouses[name]["index"]:
        #         if self.player_data["TON"] - price >= 0 and button != name:
        #
        #             self.player_data["TON"] -= price
        #             self.player_data["mouse"] = name
        #         elif self.player_data["TON"] - price <= 0:
        #             Snackbar(text="У вас не хватает на это валюты!",duration=.2).open()
        #     elif index > self.mouses[name]["index"]:
        #         Snackbar(text="Эта мышь хуже, чем у вас есть!",duration=.2).open()
        #     elif index == self.mouses[name]["index"]:
        #         Snackbar(text="У вас уже усть эта мышь!",duration=.2).open()
        elif name == "chest":
            # self.ads.show_rewarded_ad()
            if self.player_data["TON"] - self.player_data["chest"]["price"] >= 0:
                self.player_data["TON"] -= self.player_data["chest"]["price"]
                self.player_data["chest"]["price"] += self.player_data["chest"]["price"] / 100 * 30
                self.open_chest()
            else:
                # self.dialog.dismiss()
                Snackbar(text="У вас не хватает на это валюты!", duration=.2).open()

        elif name == "удвоение майнинга":
            if self.player_data["TON"] - self.doubling_data["price"] >= 0:
                self.doubling_data["value"] += self.doubling_data["value"] / 100 * 30

                self.player_data["TON"] -= self.doubling_data["price"]
                self.doubling_data["price"] += self.doubling_data["price"] / 100 * 30
            else:
                Snackbar(text="У вас не хватает на это валюты!", duration=.2).open()
        elif name == "прокачка кнопки":
            if self.player_data["TON"] - self.summation_data["summation_price"] >= 0:
                self.player_data["TON"] -= self.summation_data["summation_price"]

                self.summation_data["summation_num"] += 0.000001

                self.summation_data["summation_price"] += 0.000001 * 100
            else:
                Snackbar(text="У вас не хватает на это валюты!", duration=.2).open()
        elif name == "прокачка майнинга бота":
            if self.player_data["TON"] - self.bot_data["summation_price"] >= 0:
                self.player_data["TON"] -= self.bot_data["summation_price"]

                self.bot_data["summation_num"] += 0.000001

                self.bot_data["summation_price"] += 0.000001 * 100
            else:
                Snackbar(text="У вас не хватает на это валюты!", duration=.2).open()
        elif name == "автомайнер":
            if self.player_data["TON"] - self.bot_data["price"] >= 0 and self.bot_data["alow_bot"] == False:
                self.player_data["TON"] -= self.bot_data["price"]
                self.bot_data["alow_bot"] = True


            else:
                Snackbar(text="У вас не хватает на это валюты!", duration=.2).open()
        # self.ui_update()

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

        self.show_alert_dialog(title="Информация о майнинге", text=f'''
Клик: {'{0:.6f}'.format(self.store_items[self.player_data["mouse"]]["boost"] * self.doubling_data["value"])} TON
Мышка: {self.player_data["mouse"]}
Бот: {self.bot_data["alow_bot"]}
Текущая видеокарта: {self.bot_data["video card"]}
Майнинг автомайнера: {'{0:.6f}'.format(self.store_items[self.bot_data["video card"]]["boost"])} TON в секунду
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
        if self.dialog:
            self.dialog.dismiss()
        self.connect_error = False

    def update_data(self):
        # print(self.player_data)
        global offline

        # print(self.account["login"])
        # print('{0:.6f}'.format(self.player_data["TON"]))
        with open("data.pickle", "wb") as f:
            pickle.dump({"account": self.account, "data": self.player_data}, f)

        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
        # print(p)
        try:
            if p != False and p != None and p < max_ping:
                self.ids["wifi_error"].opacity = 0
                ref = db.reference(f"/players/{self.account['login']}")
                ref.set({"account": self.account, "data": self.player_data})
                # offline = False
            #    self.settings = pickle.load(f)
            #    self.main_font_size = self.settings["font_size"]
            else:
                self.ids["wifi_error"].opacity = .6
                # if offline == False:
                #     self.manager.current = "error_show"
                #     offline = True
        except:
            pass

    def on_tap(self):
        # print('{0:.6f}'.format(self.player_data["TON"]))

        if self.player_data["tired_num"] > 0:
            self.player_data["TON"] += self.store_items[self.player_data["mouse"]]["boost"] * self.doubling_data[
                "value"]
            self.player_data["tired_num"] -= float(Decimal(f'{self.store_items[self.player_data["mouse"]]["tired"]}'))
        # self.player_data["is_tired"] = True
        # print(App.get_running_app().root.ids['hi'])

    def sign_out(self):
        # print(self.manager.current)
        global offline, auth_succefull

        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")

        print(p)
        if p != False and p != None and p < max_ping:
            auth_succefull = False
            os.remove("data.pickle")
            self.manager.current = "auth"
        else:

            self.show_alert_dialog(title="Ошибка!", text='''
Эта кнопка не доступна!
Вы в режиме оффлайн майнинга!
Проверьте подключение к интернету и попробуйте снова.
''')

    def main_loop(self, dt):
        global auth_succefull
        if auth_succefull:
            pass
            th = Thread(target=self.ui_update)
            th.start()
            # self.ui_update()

    def ui_update(self):

        self.ids["player_name"].text = f'''Имя: {self.account["name"]}'''
        self.ids["player_login"].text = f'''Логин: {self.account["login"]}'''

        # print(self.account)
        self.ids[
            'text_doubling'].secondary_text = f'''Цена: {'{0:.6f}'.format(self.doubling_data["price"])} TON'''
        # self.ids[
        #     'text_doubling'].tertiary_text = f'''Увеличение до x{'{0:.6f}'.format(self.doubling_data["value"] / 100 * 30)}'''
        # Удвоение майнинга с:{self.player_data["doubling"] } на 30%

        #        self.ids[
        #            'text_summation'].secondary_text = f'''Цена: {'{0:.6f}'.format(self.summation_data["summation_price"])} TON'''
        self.ids['TON_num'].text = '{0:.6f}'.format(self.player_data["TON"])
        # self.ids['video_shop'].secondary_text = f'''цена: {'{0:.6f}'.format(self.bot_data["price"])} TON'''
        # self.ids['text_bot_summation'].secondary_text = f'''цена: {self.bot_data["summation_price"]} TON'''
        #
        #             #App.get_running_app().root.ids['TON_num_natural'].text = f"точнее: {self.player_data['TON']}"
        #
        self.ids["tired_num"].text = f"   {'{0:.1f}'.format(self.player_data['tired_num'])}"

    def miner_loop(self, dt):
        global auth_succefull
        if auth_succefull:
            th = Thread(target=self.autominer)
            th.start()
            th = Thread(target=self.update_data)
            th.start()
            # if self.ids["mining_button"].state != "down" and self.player_data["tired_num"] < 30:
            #     self.player_data["tired_num"] += 1

    def tired_loop(self, dt):
        global auth_succefull
        if auth_succefull:

            if self.ids["mining_button"].state != "down" and self.player_data["tired_num"] < 40:
                self.player_data["tired_num"] += 1

    def autominer(self):
        if self.bot_data["alow_bot"]:
            video = self.bot_data["video card"]

            name = self.store_items[video]["name"]
            boost = self.store_items[video]["boost"]
            price = self.store_items[video]["price"]
            type_card = self.store_items[video]["type"]

            self.player_data["TON"] += boost

    def update_auction(self):
        th = Thread(target=self.load_ah)
        th.start()

    def load_ah(self):
        ref = db.reference(f"/auction/")
        items = ref.get()
        if items:
            for name, item in items:
                price = item["price"]
                card_number = item["card_number"]
                product = item["product"]

                # image = ImageLeftWidget(source=f"{}.png")
                line = TwoLineIconListItem(

                    text=f"{product} TON за {price} руб.",
                    # source="",

                    secondary_text=f"",
                    name=name,
                    type="ah_item",
                    on_press=lambda event: self.buy(name="test")

                )

                # line.add_widget(image)
                self.ids["auction_items"].add_widget(line)

    def open_chest(self):
        type_index = random.randint(0, (len(self.bonuses) - 1) * 10)
        bonuse_items = self.bonuses[type_index]
        bonuse_index = random.randint(0, (len(bonuse_items) - 1) * 10)
        for name, item in bonuse_items.items():
            if int(bonuse_index / 10) == item["index"]:

                bonuse = name
                if item["type"] == "video card" and item["index"] >= self.store_items[self.bot_data["video card"]][
                    "index"]:
                    self.bot_data["video card"] = bonuse
                    self.show_alert_dialog(title="Поздравляем!", text=f"Вам выпала видеокарта {bonuse}!")
                elif item["type"] == "mouse" and item["index"] >= self.mouses[self.player_data["mouse"]]["index"]:
                    self.player_data["mouse"] = bonuse
                    self.show_alert_dialog(title="Поздравляем!", text=f"Вам выпала мышь {bonuse}!")
                elif item["type"] == "TON":
                    self.player_data["TON"] += float(name)
                    self.show_alert_dialog(title="Поздравляем!", text=f"Вам выпало {bonuse} TON!")
                break
        # day = self.player_data["chest_last_opened"].day
        # hour = self.player_data["chest_last_opened"].hour
        # minute = self.player_data["chest_last_opened"].minute
        #
        # if datetime.now() >= self.player_data["chest_last_opened"] + timedelta(hours=2):
        #     type_index = random.randint(0, len(self.bonuses) - 1)
        #     bonuse_items = self.bonuses[type_index]
        #     bonuse_index = random.randint(0, len(bonuse_items) - 1)
        #     for name, item in bonuse_items.items():
        #         if bonuse_index == item["index"]:
        #
        #             bonuse = name
        #             if item["type"] == "video card" and item["index"] >= self.store_items[self.bot_data["video card"]]["index"]:
        #                 self.bot_data["video card"] = bonuse
        #                 self.show_alert_dialog(title="Поздравляем!", text=f"Вам выпала видеокарта {bonuse}")
        #             elif item["type"] == "mouse" and item["index"] >= self.mouses[self.player_data["mouse"]]["index"]:
        #                 self.player_data["mouse"] = bonuse
        #                 self.show_alert_dialog(title="Поздравляем!", text=f"Вам выпала мышь {bonuse}")
        #             self.player_data["chest_last_opened"] = datetime.now()
        #
        #             break
        # else:
        #     print(self.player_data["chest_last_opened"], int(str(datetime.now().hour) + str(datetime.now().minute)))
        #
        #     self.show_alert_dialog(title="Ой!", text=f'До следующего бесплатного сундука осталось {self.player_data["chest_last_opened"] + timedelta(hours=2) - datetime.now()}')

    def add_auction(self):
        pass


class Loading(Screen):
    pass


class app(MDApp):

    def build(self):
        global auth_succefull, already_auth, data

        # Clock.schedule_interval(self.start_loops, 1/30)
        self.screen_manager = ScreenManager()
        self.screen_manager.transition = NoTransition()
        Logger.info('Loader: Screeen manager has been loaded.')
        loading = Loading(name="loading")

        self.screen_manager.add_widget(loading)
        Logger.info('Loader: Spinner screen has been loaded.')
        self.screen_manager.current = "loading"

        print(123)

        auth = Auth(name="auth")
        self.screen_manager.add_widget(auth)
        Logger.info('Loader: Auth screen has been loaded.')
        d = Error_show(name="error_show")
        self.screen_manager.add_widget(d)
        Logger.info('Loader: Error screen has been loaded.')

        self.game = Clicker(name="clicker")

        # self.game = Clicker(name="clicker")
        #
        # self.screen_manager.add_widget(self.game)
        Clock.schedule_interval(self.game.miner_loop, 1)
        Clock.schedule_interval(self.game.main_loop, 1 / 10)
        Clock.schedule_interval(self.game.tired_loop, 1)

        self.screen_manager.add_widget(self.game)

        th = Thread(target=self.start_game)
        th.start()

        return self.screen_manager

        #    # def on_start(self):

    #     self.fps_monitor_start()
    #      # d.folder_path = folder_path
    #

    def start_game(self):
        global data, auth_succefull

        #
        for i in self.game.store_items:
            name = self.game.store_items[i]["name"]
            boost = self.game.store_items[i]["boost"]
            price = self.game.store_items[i]["price"]
            index = self.game.store_items[i]["index"]
            type_item = self.game.store_items[i]["type"]
            texture = self.game.store_items[i]["texture"]

            # if type_item == "video card":
            # print("image loading")
            # if "." == texture:
            #     image = ImageLeftWidget(source=texture)
            # else:
            #     image = IconLeftWidget(icon=texture)

            # r = ImageRightWidget(source=f"ен.png")

            # font_style: "H5"
            # font_name: "main_font.ttf"
            # font_size: 20
            if index != 0:

                # f = FloatLayout()
                # f.add_widget(MDLabel(text="hi"))
                #
                # #        BoxLayout:
                # #            #valign: "center"
                # #            Image:
                # #
                # #            pos_hint: {"y": .15}
                # #            MDLabel:
                # #                #valign: "center"
                # #                text: root.text
                # f.add_widget(MDLabel(text="dws"))
                print("list loading")

                line = TwoLineListItem(

                    text=name,
                    # source="",
                    secondary_text=f"Цена: {price} TON",
                    # font_name="main_font.ttf",
                    font_style="H6",
                    # type=type_card,
                    on_press=self.game.buy_confirm
                )
                line.name = name


                # self.game.ids["bot_shop"].add_widget(MDLabel(text="hi"))
                if type_item == "video card":
                    self.game.ids["bot_shop"].add_widget(line)
                elif type_item == "mouse":
                    self.game.ids["mining_shop"].add_widget(line)
                # print(line.size)
        print("shound loading")
        d = SoundLoader.load("soundtrek.wav")
        if d:
            d.loop = True
            d.volume = .3
            d.play()

        cred_obj = firebase_admin.credentials.Certificate('bl-test-671cd-firebase-adminsdk-7uep2-46a3a5832a.json')
        app_d = firebase_admin.initialize_app(cred_obj, {
            'databaseURL': "https://bl-test-671cd-default-rtdb.firebaseio.com/"
        })

        # print(p == "False")
        ref = db.reference(f"/lock_project")
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
        if p != False and p != None and p < max_ping:

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

                    ref = db.reference(f"/players/{data['account']['login']}")
                    p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
                    if p != False and p != None and p < max_ping:
                        ref.set(data)

                        set_data()
                        auth_succefull = True

                        self.screen_manager.current = "clicker"
                    else:
                        firebase_admin.delete_app(firebase_admin.get_app())
                        cred_obj = firebase_admin.credentials.Certificate(
                            'ton-clicker-firebase-adminsdk-cf1xz-8ad3090323.json')
                        app_d = firebase_admin.initialize_app(cred_obj, {
                            'databaseURL': "https://ton-clicker-default-rtdb.firebaseio.com/"
                        })

                        self.screen_manager.current = "error_show"
            except:

                self.screen_manager.current = "auth"

        else:

            firebase_admin.delete_app(firebase_admin.get_app())
            cred_obj = firebase_admin.credentials.Certificate('ton-clicker-firebase-adminsdk-cf1xz-8ad3090323.json')
            app_d = firebase_admin.initialize_app(cred_obj, {
                'databaseURL': "https://ton-clicker-default-rtdb.firebaseio.com/"
            })
            self.screen_manager.current = "error_show"

    def donate(self):

        b = FloatLayout(pos_hint={"center_x": .5, "center_y": .5})
        self.amount = MDTextField(hint_text="Введите сумму пожертвования", mode="fill",
                                  pos_hint={"center_x": .5, "center_y": .8}, helper_text_mode="on_error",
                                  helper_text="Сумма не корректна")

        b.add_widget(self.amount)
        b.add_widget(MDFillRoundFlatButton(text="Пожертвовать", font_name="main_font.ttf", font_size="40sp",
                                    md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                    pos_hint={"center_x": .5, "center_y": .15},
                                    on_press=self.on_donate))
        self.dialog = Popup(title="Помочь", title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                            separator_color=(1, 1, 1, 1), title_align="center", title_size="30sp", content=b,
                            size_hint=(.5, .5), background="dialog.png")
        self.dialog.open()

    def on_donate(self, event):

        if not self.amount.text.isdigit():
            self.amount.error = True
        elif int(self.amount.text) < 1000000000:
            self.amount.error = False
            api = Api(merchant_id=1396424,
                      secret_key='test')
            checkout = Checkout(api=api)
            data = {
                "currency": "RUB",
                "amount": int(self.amount.text) * 100
            }
            url = checkout.url(data).get('checkout_url')
            webbrowser.open(url)


# Запуск проекта
if __name__ == "__main__":
    app().run()
up_data = False
