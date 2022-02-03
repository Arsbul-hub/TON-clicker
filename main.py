import webbrowser

import webbrowser

from kivymd.uix.list import IconLeftWidget
from kivy.uix.screenmanager import *

from kivmob import KivMob, RewardedListenerInterface
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.audio import SoundLoader

import pickle
from kivymd.uix.textfield import MDTextFieldRound
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
import datetime
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton

from kivy.lang.builder import Builder

up_data = True
auth_succefull = False
offline = False
already_auth = False
data = {}
cur_nav = "nav_drawer2"
max_ping = 300
version = 1.0
no_data = {
    "account": {"name": None,
                "login": None,
                "password": None,
                "avatar": None,
                "privilege": "Игрок",

                },
    "data": {"TON": 0,
             "inventory": {"Oklick 105S": {"index": 0, "texture": "mouse-variant", "type": "mouse",
                                           "name": "Oklick 105S",
                                           "boost": 0.000001, "price": 0.000001, "tired": 1},
                           "Celeron Pro": {"index": 0, "texture": "video card.png",
                                           "name": "Celeron Pro", "type": "processor",
                                           "boost": 0.000001, "price": 0.10}
                           },

             "doubling": {"value": 1, "price": 0.001},
             "bot": {"alow_bot": False, "doubling": {"value": 1, "doubling_price": 0.001},
                     "video card": "Celeron Pro", "price": 1,
                     "summation_price": 0.000001, "summation_num": 0},
             "token": {"price": 0.000100, "value": 5},
             "summation": {"price": 0.000001, "value": 0.000001},
             # "chest_last_opened": datetime(year=2021,month=1,day=1,hour=1,minute=1),
             "chest": {"num": 1, "price": 0.000150, "last_opened": datetime.datetime.now().isoformat()},
             "mouse": "Oklick 105S",
             "tired_num": 40,
             "is_tired": False,

             }
}
from kivymd.uix.list import TwoLineAvatarIconListItem, OneLineIconListItem
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

from kivy.clock import Clock

from kivymd.uix.list import IRightBodyTouch, IRightBody, ILeftBody, ImageLeftWidget
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout


class ButImage(ButtonBehavior, AsyncImage):
    pass


# class ImageLeftWidget(ILeftBody, AsyncImage):
#    pass

class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    # Here specify the required parameters for MDTextFieldRound:
    # [...]


class Navigate_with_account(Screen):

    def __init__(self, **kwargs):
        self.game = Clicker
        super().__init__(**kwargs)

    def sign_out(self):
        global offline, auth_succefull

        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")

        print(p)
        if p != False and p != None and p < max_ping:
            auth_succefull = False
            os.remove("data.pickle")
            self.game.manager.current = "auth"
        else:

            self.show_alert_dialog(title="Ошибка!", text='''
Проверьте подключение к интернету и попробуйте снова.
        ''')

    def show_alert_dialog(self, title, text, command=lambda: print("Hello!")):
        # lambda
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
                        on_press=lambda a: [self.close_dialog(), command()]
                    ),
                ],
            )
        self.dialog.open()


class Navigate_without_account(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.game = Clicker

    def to_auth(self):
        self.manager.current = "auth"

    def sign_out(self):
        global offline, auth_succefull

        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")

        print(p)
        if p != False and p != None and p < max_ping:
            auth_succefull = False
            os.remove("data.pickle")
            self.manager.current = "auth"
        else:

            self.show_alert_dialog(title="Ошибка!", text='''
        Проверьте подключение к интернету и попробуйте снова.
        ''')


def set_data():
    c = Clicker

    c.account = data["account"]
    c.player_data = data["data"]
    c.bot_data = data["data"]["bot"]
    c.doubling_data = data["data"]["doubling"]
    c.summation_data = data["data"]["summation"]

    # adaptive_width = True


class Edit_profile(MDBoxLayout):
    def __init__(self, dialog, **kwargs):
        super().__init__(**kwargs)
        self.main_dialog = dialog

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

    def edit(self):
        global data, auth_succefull
        if self.ids["avatar"].text:
            avatar = self.ids["avatar"].text
        else:
            avatar = "classic_avatar.png"
        player_name = self.ids["name_r"].text
        # player_email = self.ids["email_r"].text
        player_password = self.ids["password_r"].ids["text_field"].text
        # print(, player_name)
        import re
        string_check = re.match('''[#$. /?]''', player_name)
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
        if p != False and p != None and p < max_ping:

            if player_password != "" and player_name != "" and string_check == None:
                # print(string_check)
                try:
                    ref = db.reference(f"/players/{player_name}")
                    account = ref.get()

                    if account == None:
                        # account = data["account"]
                        ref = db.reference(f'/players/{data["account"]["name"]}')
                        ref.delete()

                        data["account"]["name"] = player_name
                        data["account"]["login"] = player_name
                        data["account"]["password"] = player_password
                        data["account"]["avatar"] = avatar


                        #print(data["account"]["privilege"])
                        #print(data["account"])
                        self.main_dialog.dismiss()
                        # set_data()

                        # p = ping('ton-clicker-default-rtdb.firebaseio.com', unit="ms")

                        ref = db.reference(f"/players/{player_name}")
                        ref.set(data)
                        auth_succefull = True
                        # self.start_loops()
                    else:
                        # self.manager.transition = NoTransition()
                        # self.manager.current = "auth"
                        self.show_dialog('''
Аккаует с таким ником уже существует!
Придумайте новый!
            ''')
                except:
                    # self.manager.current = "auth"
                    self.show_dialog('''
Ошибка подключения!
Повторите попытку!
                                            ''')

            elif string_check:
                # self.manager.current = "auth"
                self.show_dialog('''
Все поля должны быть заполнены!
И не должны содержать специальные симбволы: пробела и '[_!#$%^&*()<>?/\|}{~:]'
            ''')
        else:
            # self.manager.current = "auth"
            self.show_dialog('''
Ошибка подключения!
Повторите попытку!
                        ''')


class RightText(IRightBody, Label):
    pass


class Check(MDCheckbox, IRightBodyTouch):
    pass


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


class Dino(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class CustomLabel(Label):
    pass


class Error_show(Screen):
    def __init__(self, **kwargs):
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
        try:
            self.dialog.dismiss()
        except:
            pass

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

            # firebase_admin.delete_app(firebase_admin.get_app())
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
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
        if p != False and p != None and p < max_ping:
            player_name = self.ids["name_l"].text
            player_password = self.ids["password_l"].ids["text_field"].text
            import re
            string_check = re.match('''[#$. /?]''', player_name)
            if player_password != "" and player_name != "" and string_check == None:
                try:
                    ref = db.reference(f"/players/{player_name}")
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
                except:
                    self.manager.current = "auth"
                    self.show_dialog('''
Ошибка подключения!
Повторите попытку!
                                    ''')



            elif string_check:
                self.manager.current = "auth"
                self.show_dialog('''
Все поля должны быть заполнены!
И не должны содержать специальные симбволы пробела и #$./?
    ''')
        else:
            self.manager.current = "auth"
            self.show_dialog('''
Ошибка подключения!
Повторите попытку!
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
        # player_email = self.ids["email_r"].text
        player_password = self.ids["password_r"].ids["text_field"].text
        import re
        string_check = re.match('''[#$. /?]''', player_name)
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
        if p != False and p != None and p < max_ping:
            if player_password != "" and player_name != "" and string_check == None:

                try:
                    ref = db.reference(f"/players/{player_name}")
                    account = ref.get()

                    if account == None:
                        # account = data["account"]
                        data["account"]["name"] = player_name
                        data["account"]["login"] = player_name
                        data["account"]["password"] = player_password
                        data["account"]["avatar"] = avatar
                        data["account"]["privilege"] = "Игрок"
                        # p = ping('ton-clicker-default-rtdb.firebaseio.com', unit="ms")

                        ref = db.reference(f"/players/{player_name}")
                        ref.set(data)

                        self.start_loops()
                    else:
                        # self.manager.transition = NoTransition()
                        self.manager.current = "auth"
                        self.show_dialog('''
Аккаует с таким ником уже существует!
Придумайте новый!
    ''')
                except:
                    self.manager.current = "auth"
                    self.show_dialog('''
Ошибка подключения!
Повторите попытку!
                                    ''')

            elif string_check:
                self.manager.current = "auth"
                self.show_dialog('''
Все поля должны быть заполнены!
И не должны содержать специальные симбволы пробела и #$./?
    ''')
        else:
            self.manager.current = "auth"
            self.show_dialog('''
Ошибка подключения!
Повторите попытку!
                ''')

    def sign_out(self):
        global offline, auth_succefull

        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")

        # print(p)
        if p != False and p != None and p < max_ping:
            auth_succefull = False
            os.remove("data.pickle")
            self.manager.current = "auth"
        else:

            self.show_alert_dialog(title="Ошибка!", text='''
        Проверьте подключение к интернету и попробуйте снова.
        ''')

    def start_loops(self):
        global auth_succefull, offline, data, cur_nav

        # c = Clicker()
        # c.set_data()
        set_data()
        auth_succefull = True
        self.game = Clicker
        cur_nav = "nav_drawer1"
        self.ids["name_l"].text = ""
        self.ids["password_l"].ids["text_field"].text = ""
        self.ids["avatar"].text = ""
        self.ids["name_r"].text = ""
        self.ids["password_r"].ids["text_field"].text = ""
        # print(self.game.cur_nav)
        #
        # self.game.ids["nav_drawer_scroll"].opacity = 1
        # self.game.ids["nav_drawer_player"].opacity = 1
        # self.game.ids["nav_drawer_button"].opacity = 0
        with open("data.pickle", "wb") as f:
            pickle.dump(data, f)

        # self.game.ids["nav_drawer"].add_widget(Navigate_with_account())
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
    def __init__(self, dialog, **kwargs):
        self.dialog = dialog
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
        # print(122222222222222222222222222)
        # self.main_font_size = main_font_size
        self.connect_error = False
        self.name = "clicker"
        # self.bitcoin = 0
        # self.bitcoin = 0
        # self.size_hint = (1,1)
        self.store_items = {
            "Celeron Pro": {"index": 0, "texture": "video card.png", "name": "Celeron Pro", "type": "processor",
                            "boost": 0.000001, "price": 0.000600},
            "Gt 770": {"index": 1, "texture": "video card.png", "name": "Gt 770", "type": "video card",
                       "boost": 0.000020, "price": 0.004000},
            "Gt 870": {"index": 2, "texture": "video card.png", "name": "Gt 870", "type": "video card",
                       "boost": 0.000020, "price": 0.006000},
            "Gtx 970": {"index": 3, "texture": "video card.png", "name": "Gtx 970", "type": "video card",
                        "boost": 0.000030, "price": 0.008000},
            "Rtx 1050": {"index": 4, "texture": "video card.png", "name": "Rtx 1050", "type": "video card",
                         "boost": 0.000040, "price": 0.010000},
            "Rtx 1070": {"index": 5, "texture": "video card.png", "name": "Rtx 1070", "type": "video card",
                         "boost": 0.000050, "price": 0.015200},
            "Rtx 2060": {"index": 6, "texture": "video card.png", "name": "Rtx 2060", "type": "video card",
                         "boost": 0.000060, "price": 0.018510},
            "Rtx 2070 Super": {"index": 7, "texture": "video card.png", "name": "Rtx 2070 Super", "type": "video card",
                               "boost": 0.000070, "price": 0.020000},
            "Rtx 2080 TI": {"index": 8, "texture": "video card.png", "name": "Rtx 2080 TI", "type": "video card",
                            "boost": 0.000080, "price": 0.022500},
            "Rtx 3060 Super": {"index": 9, "texture": "video card.png", "name": "Rtx 3060 Super", "type": "video card",
                               "boost": 0.000090, "price": 0.026700},
            # "Rtx 3090 Super TI": {"index": 10, "texture": "video card.png", "name": "Rtx 3090 Super TI",
            #                      "type": "video card", "boost": 0.000100, "price": 0.029541},
            # "Rtx 8000 Super TI Extreme Edition": {"index": 11, "texture": "video card.png",
            #                                      "name": "Rtx 8000 Super TI Extreme Edition", "type": "video card",
            #                                      "boost": 0.0003, "price": 0.035000},

            "Oklick 105S": {"index": 0, "texture": "mouse-variant", "type": "mouse", "name": "Oklick 105S",
                            "boost": 0.000001, "price": 0.000100, "tired": 1},
            "Canyon CNE-CMS05DG": {"index": 1, "texture": "mouse-variant", "type": "mouse",
                                   "name": "Canyon CNE-CMS05DG", "boost": 0.00001, "price": 0.004000, "tired": .9},
            "QUMO Office M14": {"index": 2, "texture": "mouse-variant", "type": "mouse", "name": "QUMO Office M14",
                                "boost": 0.00005, "price": 0.004547, "tired": .8},
            "Ritmix ROM-111": {"index": 3, "texture": "mouse-variant", "type": "mouse", "name": "Ritmix ROM-111",
                               "boost": 0.0001, "price": 0.007000, "tired": .7},
            "Oklick 145M": {"index": 4, "texture": "mouse-variant", "type": "mouse", "name": "Oklick 145M",
                            "boost": 0.0005, "price": 0.008500, "tired": .6},
            "Ritmix ROM-202": {"index": 5, "texture": "mouse-variant", "type": "mouse", "name": "Ritmix ROM-202",
                               "boost": 0.001, "price": 0.009500, "tired": .9},
            "Smartbuy ONE SBM-265-K": {"index": 6, "texture": "mouse-variant", "type": "mouse",
                                       "name": "Smartbuy ONE SBM-265-K", "boost": 0.005, "price": 0.040000,
                                       "tired": .4},

        }
        self.money = {
            "0.000050": {"type": "TON", "index": 0},
            "0.000100": {"type": "TON", "index": 1},
            "0.000150": {"type": "TON", "index": 2},
            "0.000200": {"type": "TON", "index": 3},
            "0.000250": {"type": "TON", "index": 4},

        }
        # import sys
        # print(sys.getsizeof(self.store_items))
        self.bonuses = [self.money, self.store_items]
        self.n = 0
        self.update_nav_drawer = False
        # self.cur_nav = "nav_drawer2"
        # self.rewards = Rewards_Handler(self)
        # self.ads = KivMob("ca-app-pub-9371118693960899~5621013296")
        # print(TestIds.REWARDED_VIDEO)
        # self.ads.load_rewarded_ad("ca-app-pub-9371118693960899/9603139268")
        # Add any callback functionality to this class.

        self.ads = KivMob("ca-app-pub-9371118693960899~5621013296")
        self.ads.load_rewarded_ad("ca-app-pub-9371118693960899/7509498390")
        self.ads.new_interstitial("ca-app-pub-9371118693960899/5940984013")

        # Add any callback functionality to this class.
        self.ads.set_rewarded_ad_listener(RewardedListenerInterface())

        # def set_data(self):
        #     global auth_succefull
        #     self.account = data["account"]
        #     self.player_data = data["data"]
        #     self.bot_data = data["data"]["bot"]
        #     self.summation_data = data["data"]["summation"]
        self.finded_numbers = []
        self.toggled = False

    def open_link(self, link):
        webbrowser.open(link)

    def current_item(self, obj):
        # print(222)
        name = obj.name

        # print(self.player_data["inventory"][name]["type"])
        if data["data"]["inventory"][name]["type"] == "video card" or data["data"]["inventory"][name][
            "type"] == "processor":
            data["data"]["bot"]["video card"] = name
            # print(data["data"]["bot"]["video card"])
        if data["data"]["inventory"][name]["type"] == "mouse":
            data["data"]["mouse"] = name

    def load_top(self):
        self.ids["error_load_top"].text = ""
        # self.ids["fl"].opacity = 0

        # self.ids["retry_load_top"].opacity = 0
        # self.ids["top_loading"].active = False
        self.ids["players_top"].clear_widgets()
        # self.ids["top_loading"].active = True
        self.ads.show_interstitial()
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
        # print(p)
        if p != False and p != None and p < max_ping:
            # try:
            # self.ids["fl"].disabled = True
            # Clock.schedule_once(ld)

            # self.ids["top_loading"].active = False
            th = Thread(target=self.loading_top)
            th.start()
            # self.loading_top()
        # th.join()

        # except:
        # self.ids["players_top"].add_widget(CustomLabel(text="Произошла ошибка подключения!\nОбновите список заново", font_name="main_font.ttf", font_size="25sp"))
        # self.ids["fl"].disabled = False
        #    self.ids["error_load_top"].text = "Произошла ошибка подключения!\nОбновите список"
        # self.ids["retry_load_top"].opacity = 1
        # self.ids["top_loading"].active = False
        else:
            self.ids["error_load_top"].text = "Произошла ошибка подключения!\nОбновите список"
            # self.ids["players_top"].add_widget(
        #     CustomLabel(text="Произошла ошибка подключения!\nОбновите список заново", font_name="main_font.ttf",
        #                 font_size="25sp"))
        # self.ids["fl"].disabled = False
        # self.ids["error_load_top"].opacity = 1
        # self.ids["retry_load_top"].opacity = 1
        # self.ids["top_loading"].active = False

    def loading_top(self):
        ref = db.reference(f'/players/')
        sorted_data = ref.order_by_child(f'data/TON').limit_to_last(15).get()
        results = list(sorted_data)
        # print(results)
        stage = 0
        for i in range(len(results) - 1, -1, -1):
            stage += 1
            # print(sorted_data[results[i]]["data"]["TON"])
            ton = sorted_data[results[i]]["data"]["TON"]
            name = sorted_data[results[i]]["account"]["name"]

            avatar = sorted_data[results[i]]["account"]["avatar"]
            # print(name)
            privilege = sorted_data[results[i]]["account"]["privilege"]

            line = TwoLineAvatarIconListItem(

                text=f"{stage}: {name}",
                # source="",
                secondary_text=f"TON: {'{0:.6f}'.format(ton)}",
                # font_name="main_font.ttf",
                # font_style="H6",
                # type=type_card,
                on_press=lambda a: print("Hello")

            )
            if privilege and privilege == "Admin":
                line.text = f"{stage}:  {name} - Админ"
                line.theme_text_color = "Custom"
                line.text_color = (1, .1, .1, 1)

            try:
                image = ImageLeftWidget(source=avatar)

                line.add_widget(image)
            except:
                pass
            if name == data["account"]["name"]:
                text = RightText(text="Вы")
                line.add_widget(text)
            # ak.and_()
            self.ids["players_top"].add_widget(line)

    def start_game(self, name):
        if name == "roulette":
            r = random.randint(0, 100)

            b = self.ids['bet_value'].value
            l = b * (-1) + self.ids['bet_value'].max
            # m = data["data"]["TON"] - s
            w = data["data"]["TON"] / 100 * b
            data["data"]["TON"] -= w

            # print('{0:.6f}'.format(data["data"]["TON"]), '{0:.7f}'.format(s / 100 * l))
            if r < 40:
                data["data"]["TON"] += w * 2
                self.show_alert_dialog(title="Поздравляем!!!", text=f"Вы выиграли {'{0:.6f}'.format(w * 2)} TON")

            else:
                self.show_alert_dialog(title="Увы!", text=f"Вы проиграли {'{0:.6f}'.format(w * 2)} TON")
        elif name == "find_it":
            if data["data"]["token"]["value"] - 1 >= 0:
                data["data"]["token"]["value"] -= 1
                self.find_li = [[0, 0, 0],
                                [0, 0, 0],
                                [0, 0, 0]]
                for i in range(3):
                    x = random.randint(0, 2)
                    y = random.randint(0, 2)
                    self.find_li[y][x] = 1
                for y in range(3):
                    for x in range(3):
                        b = ButImage(size=(.1, .1), source="card_normal.jpg", pos_hint={"x": x * .1, "y": y * .1},
                                     on_press=self.find_it)
                        if self.find_li[y][x] == 1:
                            b.name = 1
                        else:
                            b.name = 0
                        # b.background_normal = "card_normal.jpg"
                        self.ids["find_it_start_button"].opacity = 0
                        self.ids["text_find_it"].opacity = 0
                        self.ids["find_it"].add_widget(b)
                self.ids["find_it"].opacity = 1
            else:
                Snackbar(text="Увас нет жетонов!", duration=.2).open()

    def find_it(self, obj):
        # self.ids["find_it"].opacity = 1
        # print(obj.name)

        if len(self.finded_numbers) >= 3:
            # print(">3")
            n = 0
            for i in self.finded_numbers:
                if i.name == 1:
                    n += 0.000100

            data["data"]["TON"] += n

            self.finded_numbers = []
            # time.sleep(1)

            self.show_alert_dialog(title="Поздравляем!",
                                   text=f"Вы нашли {int(n / 0.000100)} карточки\nВы выиграли {'{0:.6f}'.format(n)} TON",
                                   command=self.undo_find_it)
        else:
            self.finded_numbers.append(obj)
            if obj.name == 1:
                obj.source = "card_win.jpg"
            if obj.name == 0:
                obj.source = "card_loose.jpg"
            obj.disabled = True
    def undo_find_it(self):
        self.ids["find_it"].clear_widgets()
        self.ids["find_it_start_button"].opacity = 1
        self.ids["text_find_it"].opacity = 1
        self.ids["find_it"].opacity = 0

    def show_rewarded_ad(self, command=None):
        self.ads.show_rewarded_ad()
        self.ads.on_rewarded_video_ad_completed = self.open_chest(is_bought=False)

    def load_video(self):
        self.ads.load_rewarded_ad("ca-app-pub-9371118693960899/7509498390")

    def buy_confirm(self, obj):
        name = obj.name
        # print(name)
        self.dialog = None

        # if call == "video_card":
        #     price = self.videocards[name]["price"]
        # elif call == "mouse":
        #     price = self.mouses[name]["price"]
        # else:
        #     price = self.mouses[name]["price"]

        if not self.dialog:
            if name == "суммирование майнинга":
                b = BoxLayout(orientation="vertical")
                b.add_widget(CustomLabel(text=f'Цена: {"{0:.6f}".format(data["data"]["summation"]["price"])}',
                                         halign="center",
                                         font_name="main_font.ttf",
                                         font_size="25sp",

                                         # theme_text_color="Custom",
                                         # color=(0, 0, 0, 1),
                                         )
                             )

                b.add_widget(CustomLabel(
                    text=f'Увеличение прибавления к майнингу до +{"{0:.6f}".format(data["data"]["summation"]["value"] + data["data"]["summation"]["value"] * 10)} TON',
                    halign="center",
                    font_name="main_font.ttf",
                    font_size="25sp",
                    # color=(0, 0, 0, 1),
                    # theme_text_color="Custom",
                    # text_color=(1,1,1,1)
                )
                )

                b2 = BoxLayout(spacing="5sp")
                b2.add_widget(
                    MDFillRoundFlatButton(text="Купить!", md_bg_color=(0.1, 0.6, 0.9, 1.0), font_name="main_font.ttf",
                                          size_hint=(.3, None), font_size="25sp",
                                          on_press=lambda a: self.buy(obj=obj)))
                b2.add_widget(
                    MDFillRoundFlatButton(text="Отмена", md_bg_color=(0.1, 0.6, 0.9, 1.0), font_name="main_font.ttf",
                                          size_hint=(.3, None), font_size="25sp",
                                          on_press=lambda a: self.close_dialog()))
                b.add_widget(b2)
                # b.add_widget(MDLabel(text="Описание: Увеличивает майнинг в x раз"))
                # Buy_content(price=self.doubling_data["price"], boost=f'Увеличение удвоения майнинга с {self.doubling_data["price"]} TON/клик до {self.doubling_data["value"] + self.doubling_data["value"] / 100 * 30} TON/клик', description="Увеличивает майнинг в x раз"),
                self.dialog = Popup(title=name.capitalize(), title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                                    title_align="center", title_size="30sp", content=b,
                                    size_hint=(.9, .7), background="dialog.png")
            if name == "удвоение майнинга":
                b = BoxLayout(orientation="vertical")
                b.add_widget(CustomLabel(text=f'Цена: {self.doubling_data["price"]}',
                                         halign="center",
                                         font_name="main_font.ttf",
                                         font_size="25sp",

                                         # theme_text_color="Custom",
                                         # color=(0, 0, 0, 1),
                                         )
                             )

                b.add_widget(CustomLabel(
                    text=f'Увеличение умножения майнинга до {self.doubling_data["value"] + self.doubling_data["value"] / 100 * 30} раз',
                    halign="center",
                    font_name="main_font.ttf",
                    font_size="25sp",
                    # color=(0, 0, 0, 1),
                    # theme_text_color="Custom",
                    # text_color=(1,1,1,1)
                )
                )

                b2 = BoxLayout(spacing="5sp")
                b2.add_widget(
                    MDFillRoundFlatButton(text="Купить!", md_bg_color=(0.1, 0.6, 0.9, 1.0), font_name="main_font.ttf",
                                          size_hint=(.3, None), font_size="25sp",
                                          on_press=lambda a: self.buy(obj=obj)))
                b2.add_widget(
                    MDFillRoundFlatButton(text="Отмена", md_bg_color=(0.1, 0.6, 0.9, 1.0), font_name="main_font.ttf",
                                          size_hint=(.3, None), font_size="25sp",
                                          on_press=lambda a: self.close_dialog()))
                b.add_widget(b2)
                # b.add_widget(MDLabel(text="Описание: Увеличивает майнинг в x раз"))
                # Buy_content(price=self.doubling_data["price"], boost=f'Увеличение удвоения майнинга с {self.doubling_data["price"]} TON/клик до {self.doubling_data["value"] + self.doubling_data["value"] / 100 * 30} TON/клик', description="Увеличивает майнинг в x раз"),
                self.dialog = Popup(title=name.capitalize(), title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                                    title_align="center", title_size="30sp", content=b,
                                    size_hint=(.9, .7), background="dialog.png")
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
            # print(data["data"]["bot"]["alow_bot"])
            if name == "автомайнер":
                if not data["data"]["bot"]["alow_bot"]:
                    f = FloatLayout()
                    b = MDBoxLayout(orientation="vertical")

                    b.add_widget(CustomLabel(text=f'Цена: {"{0:.6f}".format(data["data"]["bot"]["price"])} TON',
                                             halign="center",
                                             # color=(0, 0, 0, 1),
                                             font_name="main_font.ttf",
                                             font_size="25sp", ))
                    b.add_widget(CustomLabel(
                        text=f'Для втоматической добычи валюты требуется видеокарта',
                        halign="center",
                        # text_size=,
                        # size=b.texture_size,
                        # color=(0, 0, 0, 1),
                        font_name="main_font.ttf",
                        font_size="25sp"))
                    # Label:
                    # text_size: root.width, None
                    # size: self.texture_size
                    # f.add_widget(b)
                    b2 = BoxLayout(spacing="5sp")
                    b2.add_widget(
                        MDFillRoundFlatButton(text="Купить!", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                              font_name="main_font.ttf",
                                              size_hint=(.3, None), font_size="25sp",
                                              on_press=lambda a: self.buy(obj=obj, disabled=True)))
                    b2.add_widget(
                        MDFillRoundFlatButton(text="Отмена", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                              font_name="main_font.ttf",
                                              size_hint=(.3, None), font_size="25sp",
                                              on_press=lambda a: self.close_dialog()))
                    b.add_widget(b2)
                    # f.add_widget(b)

                    # b.add_widget(MDMDLabel(text="Описание: Увеличивает майнинг в x раз"))
                    # Buy_content(price=self.doubling_data["price"], boost=f'Увеличение удвоения майнинга с {self.doubling_data["price"]} TON/клик до {self.doubling_data["value"] + self.doubling_data["value"] / 100 * 30} TON/клик', description="Увеличивает майнинг в x раз"),
                    self.dialog = Popup(title=name.capitalize(), title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                                        title_align="center", title_size="30sp", content=b,
                                        size_hint=(.9, .7), background="dialog.png")

            elif name in self.store_items and self.store_items[name]["type"] == "video card" or self.store_items[name][
                "type"] == "processor":
                if name in data["data"]["inventory"]:
                    f = FloatLayout()
                    b = BoxLayout(orientation="vertical")
                    self.video_card_price = CustomLabel(
                        text=f'Цена: {"{0:.7f}".format(data["data"]["inventory"][name]["price"])} TON',
                        halign="center",
                        # color=(0, 0, 0, 1),
                        font_name="main_font.ttf",
                        font_size="25sp", )
                    b.add_widget(self.video_card_price)
                    self.video_card_speed = CustomLabel(
                        text=f'Скорость: {"{0:.7f}".format(data["data"]["inventory"][name]["boost"])} + {"{0:.7f}".format(data["data"]["inventory"][name]["boost"] * .3)} TON/сек',
                        halign="center",
                        # color=(0, 0, 0, 1),
                        font_name="main_font.ttf",
                        font_size="25sp", )
                    b.add_widget(self.video_card_speed)

                    # f.add_widget(b)
                    b2 = BoxLayout(spacing="5sp")
                    b2.add_widget(
                        MDFillRoundFlatButton(text="Прокачать!", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                              font_name="main_font.ttf",
                                              size_hint=(.3, None), font_size="25sp",
                                              on_press=lambda a: self.boosting(obj=obj)))
                    b2.add_widget(
                        MDFillRoundFlatButton(text="Отмена", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                              font_name="main_font.ttf",
                                              size_hint=(.3, None), font_size="25sp",
                                              on_press=lambda a: self.close_dialog()))
                    b.add_widget(b2)
                    # f.add_widget(b)

                    # b.add_widget(MDMDLabel(text="Описание: Увеличивает майнинг в x раз"))
                    # Buy_content(price=self.doubling_data["price"], boost=f'Увеличение удвоения майнинга с {self.doubling_data["price"]} TON/клик до {self.doubling_data["value"] + self.doubling_data["value"] / 100 * 30} TON/клик', description="Увеличивает майнинг в x раз"),
                    self.dialog = Popup(title=name, title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                                        title_align="center", title_size="30sp", content=b,
                                        size_hint=(.9, .7), background="dialog.png")
                else:
                    f = FloatLayout()
                    b = BoxLayout(orientation="vertical")

                    b.add_widget(CustomLabel(text=f'Цена: {"{0:.6f}".format(self.store_items[name]["price"])}',
                                             halign="center",
                                             # color=(0, 0, 0, 1),
                                             font_name="main_font.ttf",
                                             font_size="25sp", ))
                    b.add_widget(CustomLabel(
                        text=f'Скорость: {"{0:.6f}".format(self.store_items[name]["boost"])} TON/сек',
                        halign="center",
                        # color=(0, 0, 0, 1),
                        font_name="main_font.ttf",
                        font_size="25sp", ))

                    # f.add_widget(b)
                    b2 = BoxLayout(spacing="5sp")
                    b2.add_widget(
                        MDFillRoundFlatButton(text="Купить!", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                              font_name="main_font.ttf",
                                              size_hint=(.3, None), font_size="25sp",
                                              on_press=lambda a: self.buy(obj=obj, disabled=True)))
                    b2.add_widget(
                        MDFillRoundFlatButton(text="Отмена", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                              font_name="main_font.ttf",
                                              size_hint=(.3, None), font_size="25sp",
                                              on_press=lambda a: self.close_dialog()))
                    b.add_widget(b2)
                    # f.add_widget(b)

                    # b.add_widget(MDMDLabel(text="Описание: Увеличивает майнинг в x раз"))
                    # Buy_content(price=self.doubling_data["price"], boost=f'Увеличение удвоения майнинга с {self.doubling_data["price"]} TON/клик до {self.doubling_data["value"] + self.doubling_data["value"] / 100 * 30} TON/клик', description="Увеличивает майнинг в x раз"),
                    self.dialog = Popup(title=name, title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                                        title_align="center", title_size="30sp", content=b,
                                        size_hint=(.9, .7), background="dialog.png")
            elif name in self.store_items and self.store_items[name]["type"] == "mouse":
                print(name)
                if name in data["data"]["inventory"]:
                    f = FloatLayout()
                    b = MDBoxLayout(orientation="vertical")
                    self.mouse_price = CustomLabel(
                        text=f'Цена: {"{0:.6f}".format(data["data"]["inventory"][name]["price"])}',
                        halign="center",
                        # color=(0, 0, 0, 1),
                        font_name="main_font.ttf",
                        font_size="25sp", )
                    b.add_widget(self.mouse_price)
                    self.mouse_speed = CustomLabel(
                        text=f'Скорость: {"{0:.7f}".format(data["data"]["inventory"][name]["boost"])} + {"{0:.7f}".format(data["data"]["inventory"][name]["boost"] * .3)} TON/клик',
                        halign="center",
                        # color=(0, 0, 0, 1),
                        font_name="main_font.ttf",
                        font_size="25sp", )
                    b.add_widget(self.mouse_speed)
                    self.mouse_tired = CustomLabel(
                        text=f'Склонность к усталости: {int(data["data"]["inventory"][name]["tired"] * 100)}% - 2%',
                        halign="center",
                        # color=(0, 0, 0, 1),
                        font_name="main_font.ttf",
                        font_size="25sp", )
                    b.add_widget(self.mouse_tired)
                    # f.add_widget(b)
                    b2 = BoxLayout(spacing="5sp")
                    b2.add_widget(MDFillRoundFlatButton(text="Прокачать!", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                                        on_press=lambda a: self.boosting(obj=obj),
                                                        font_name="main_font.ttf",
                                                        size_hint=(.3, None), font_size="25sp"))
                    b2.add_widget(MDFillRoundFlatButton(text="Отмена", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                                        on_press=lambda a: self.close_dialog(),
                                                        font_name="main_font.ttf",
                                                        size_hint=(.3, None), font_size="25sp"))
                    b.add_widget(b2)
                    # f.add_widget(b)

                    # b.add_widget(MDLabel(text="Описание: Увеличивает майнинг в x раз"))
                    # Buy_content(price=self.doubling_data["price"], boost=f'Увеличение удвоения майнинга с {self.doubling_data["price"]} TON/клик до {self.doubling_data["value"] + self.doubling_data["value"] / 100 * 30} TON/клик', description="Увеличивает майнинг в x раз"),
                    self.dialog = Popup(title=name, title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                                        title_align="center", title_size="30sp", content=b,
                                        size_hint=(.9, .7), background="dialog.png")
                else:
                    f = FloatLayout()
                    b = MDBoxLayout(orientation="vertical")

                    b.add_widget(CustomLabel(text=f'Цена: {"{0:.6f}".format(self.store_items[name]["price"])}',
                                             halign="center",
                                             # color=(0, 0, 0, 1),
                                             font_name="main_font.ttf",
                                             font_size="25sp", ))
                    b.add_widget(CustomLabel(
                        text=f'Скорость: {"{0:.6f}".format(self.store_items[name]["boost"])} TON/клик',
                        halign="center",
                        # color=(0, 0, 0, 1),
                        font_name="main_font.ttf",
                        font_size="25sp", ))
                    b.add_widget(CustomLabel(
                        text=f'Склонность к усталости: {int(self.store_items[name]["tired"] * 100)}%',
                        halign="center",
                        # color=(0, 0, 0, 1),
                        font_name="main_font.ttf",
                        font_size="25sp", ))
                    # f.add_widget(b)
                    b2 = BoxLayout(spacing="5sp")
                    b2.add_widget(MDFillRoundFlatButton(text="Купить!", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                                        on_press=lambda a: self.buy(obj=obj, disabled=True),
                                                        font_name="main_font.ttf",
                                                        size_hint=(.3, None), font_size="25sp"))
                    b2.add_widget(MDFillRoundFlatButton(text="Отмена", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                                        on_press=lambda a: self.close_dialog(),
                                                        font_name="main_font.ttf",
                                                        size_hint=(.3, None), font_size="25sp"))
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
            #     content_cls=Buy_content(price=data["data"]["bot"]["price"],
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
            # b.add_widget(Button(text=f"Открыть за {data["data"]['chest']['price']} TON",
            #                        on_press=lambda event: self.buy(name="chest")))
            # b.add_widget(Button(text="Открыть, посмотрев видео", on_press=self.show_video))
            now = datetime.datetime.now()
            last_opened = datetime.datetime.fromisoformat(
                data["data"]["chest"].setdefault("last_opened", datetime.datetime.now().isoformat()))
            if now - last_opened > datetime.timedelta(hours=12):

                b2 = BoxLayout(orientation="vertical", spacing="5sp")
                b2.add_widget(CustomLabel(text=f'У вас есть 1 бесплатный сундук',
                                          halign="center",
                                          pos_hint={"center_x": .5},
                                          font_name="main_font.ttf",
                                          font_size="25sp",

                                          # theme_text_color="Custom",
                                          # color=(0, 0, 0, 1),
                                          )
                              )
                b2.add_widget(
                    MDFillRoundFlatButton(text="Открыть!", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                          pos_hint={"center_x": .5},
                                          font_name="main_font.ttf",
                                          size_hint=(.3, None),
                                          font_size="25sp",
                                          on_press=lambda a: self.open_chest(is_bought=False)))
                b = MDFlatButton(
                    text="Отмена",
                    font_size="20sp",
                    font_name="main_font.ttf",
                    pos_hint={"right": 1, "center_y": .1},
                    )
                b2.add_widget(b)
                self.chest_dialog = Popup(title="Открыть сундук?", title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                                          title_align="center", title_size="30sp", content=b2,
                                          size_hint=(.9, .5), background="dialog.png")
                b.bind(on_release=lambda a: self.chest_dialog.dismiss())
            else:
                self.chest_dialog = Popup(title="Открыть сундук?", title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                                          title_align="center", title_size="30sp",
                                          size_hint=(.9, .5), background="dialog.png")
                self.chest_dialog.content = Chest_content(dialog=self.chest_dialog)
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
            self.chest_dialog.open()

    def boosting(self, obj):
        name = obj.name

        video = data["data"]["bot"]["video card"]
        index = data["data"]["inventory"][name]["index"]
        price = data["data"]["inventory"][name]["price"]
        type_item = data["data"]["inventory"][name]["type"]

        # if index < self.store_items[name]["index"]:
        if data["data"]["TON"] - price >= 0:
            # print(type_item)
            data["data"]["TON"] -= price

            if type_item == "mouse":
                data["data"]["inventory"][name]["price"] += data["data"]["inventory"][name]["price"] * 5
                data["data"]["inventory"][name]["boost"] += data["data"]["inventory"][name]["boost"] * .3
                data["data"]["inventory"][name]["tired"] -= data["data"]["inventory"][name]["tired"] * .02
                data["data"]["mouse"] = name
                self.mouse_price.text = f'Цена: {"{0:.6f}".format(data["data"]["inventory"][name]["price"])}'
                self.mouse_tired.text = f'Склонность к усталости: {int(data["data"]["inventory"][name]["tired"] * 300)}% - 2%'
                self.mouse_speed.text = f'Скорость: {"{0:.6f}".format(data["data"]["inventory"][name]["boost"])} + {"{0:.6f}".format(data["data"]["inventory"][name]["boost"] * .3)} TON/клик'
            elif type_item == "video card":
                # print("23456")
                data["data"]["inventory"][name]["price"] += data["data"]["inventory"][name]["price"] * 5
                data["data"]["inventory"][name]["boost"] += data["data"]["inventory"][name]["boost"] * .3

                data["data"]["bot"]["video card"] = name
                self.video_card_price.text = f'Цена: {"{0:.6f}".format(data["data"]["inventory"][name]["price"])} TON'
                self.video_card_speed.text = f'Скорость: {"{0:.6f}".format(data["data"]["inventory"][name]["boost"])} + {"{0:.8f}".format(data["data"]["inventory"][name]["boost"] * .3)} TON/сек'
            # data["data"]["inventory"][name]["price"] += data["data"]["inventory"][name]["price"] * 300
            # obj.secondary_text = f'Цена: {"{0:.6f}".format(data["data"]["inventory"][name]["price"])} TON'
            obj.secondary_text = f'''Цена: {'{0:.6f}'.format(data["data"]["inventory"][name]["price"])} TON'''
        elif data["data"]["TON"] - price <= 0:
            Snackbar(text="У вас не хватает на это TON!", duration=.2).open()

    def buy(self, obj, disabled=False):

        name = obj.name
        self.close_dialog()
        # obj.disabled = disabled
        # obj.children.disabled = False
        if name in self.store_items:
            video = data["data"]["bot"]["video card"]
            index = self.store_items[video]["index"]
            price = self.store_items[name]["price"]
            type_item = self.store_items[name]["type"]

            if data["data"]["TON"] - price >= 0 and video != name:

                data["data"]["TON"] -= price
                if type_item == "mouse":

                    data["data"]["mouse"] = name
                elif type_item == "video card":
                    data["data"]["bot"]["video card"] = name
                data["data"]["inventory"][name] = self.store_items[name]
                data["data"]["inventory"][name]["price"] += data["data"]["inventory"][name]["price"] * 5
                obj.secondary_text = f'Цена: {"{0:.6f}".format(data["data"]["inventory"][name]["price"])} TON'
            elif data["data"]["TON"] - price <= 0:
                Snackbar(text="У вас не хватает на это TON!", duration=.2).open()

        # elif name in self.mouses:видеокарта
        #     button = data["data"]["mouse"]
        #     index = self.mouses[button]["index"]
        #     price = self.mouses[name]["price"]
        #     if index < self.mouses[name]["index"]:
        #         if data["data"]["TON"] - price >= 0 and button != name:
        #
        #             data["data"]["TON"] -= price
        #             data["data"]["mouse"] = name
        #         elif data["data"]["TON"] - price <= 0:
        #             Snackbar(text="У вас не хватает на это валюты!",duration=.2).open()
        #     elif index > self.mouses[name]["index"]:
        #         Snackbar(text="Эта мышь хуже, чем у вас есть!",duration=.2).open()
        #     elif index == self.mouses[name]["index"]:
        #         Snackbar(text="У вас уже усть эта мышь!",duration=.2).open()
        elif name == "token":
            if data["data"]["TON"] - data["data"]["token"]["price"] >= 0:
                data["data"]["TON"] -= data["data"]["token"]["price"]
                # data["data"]["token"]["price"] += data["data"]["token"]["price"] / 100 * 20
                data["data"]["token"]["value"] += 1

            else:
                # self.dialog.dismiss()
                Snackbar(text="У вас не хватает на это TON!", duration=.2).open()

        elif name == "chest":
            # self.ads.show_rewarded_ad()
            if data["data"]["TON"] - data["data"]["chest"]["price"] >= 0:

                # data["data"]["chest"]["price"] += data["data"]["chest"]["price"] / 100 * 20

                # else:
                self.open_chest(is_bought=True)

            else:
                # self.dialog.dismiss()
                Snackbar(text="У вас не хватает на это TON!", duration=.2).open()

        elif name == "удвоение майнинга":
            if data["data"]["TON"] - self.doubling_data["price"] >= 0:
                self.doubling_data["value"] += self.doubling_data["value"] / 100 * 50

                data["data"]["TON"] -= self.doubling_data["price"]
                self.doubling_data["price"] += self.doubling_data["price"] / 100 * 50

            else:
                Snackbar(text="У вас не хватает на это TON!", duration=.2).open()
        elif name == "суммирование майнинга":
            if data["data"]["TON"] - self.summation_data["price"] >= 0:
                data["data"]["TON"] -= self.summation_data["price"]

                self.summation_data["value"] += 0.000001

                self.summation_data["price"] += 0.000001 * 100
            else:
                Snackbar(text="У вас не хватает на это TON!", duration=.2).open()
        elif name == "прокачка майнинга бота":
            if data["data"]["TON"] - data["data"]["bot"]["summation_price"] >= 0:
                data["data"]["TON"] -= data["data"]["bot"]["summation_price"]

                data["data"]["bot"]["summation_num"] += 0.000001

                data["data"]["bot"]["summation_price"] += 0.000001 * 100
            else:
                Snackbar(text="У вас не хватает на это TON!", duration=.2).open()
        elif name == "автомайнер":
            if data["data"]["TON"] - data["data"]["bot"]["price"] >= 0:
                data["data"]["TON"] -= data["data"]["bot"]["price"]
                data["data"]["bot"]["alow_bot"] = True
                obj.secondary_text = "Активен"



            else:
                Snackbar(text="У вас не хватает на это TON!", duration=.2).open()
        # self.ui_update()

    def show_value(self):
        b = self.ids['bet_value'].value

        # m = data["data"]["TON"] - s

        w = data["data"]["TON"] / 100 * b
        self.ids['value_bet_text'].text = f"Ваша ставка: {'{0:.6f}'.format(w)} TON"

    def show_info(self):
        if data["data"]["bot"]["alow_bot"]:
            alow_bot = "Активен"
        else:
            alow_bot = "Неактивен"
        self.show_alert_dialog(title="Информация", text=f'''
Клик: {'{0:.6f}'.format(data["data"]["inventory"][data["data"]["mouse"]]["boost"])} TON
Мышка: {data["data"]["mouse"]}
Жетоны: {data["data"]["token"]["value"]}
Бот: {alow_bot}
Текущая видеокарта: {data["data"]["bot"]["video card"]}
Майнинг автомайнера: {'{0:.6f}'.format(data["data"]["inventory"][data["data"]["bot"]["video card"]]["boost"])} TON в секунду
''')

    def show_alert_dialog(self, title, text, command=lambda: print("Hello!")):
        # lambda
        self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(
                text=text,
                title=title,
                auto_dismiss=False,
                # title_font = "main_font.ttf",
                # title_align = "center",
                # title_size = "30sp",
                buttons=[
                    MDFlatButton(
                        text="Ок",
                        theme_text_color="Custom",
                        # text_font_name= "main_font.ttf",
                        text_color=(0, 0, 0, 1),
                        font_size="20sp",
                        font_name="main_font.ttf",
                        # text_color=self.theme_cls.primary_color,
                        on_press=lambda a: [self.close_dialog(), command()]
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self):
        try:
            self.dialog.dismiss()
        except:
            pass
        self.connect_error = False

    def update_data(self):
        # print(data["data"])
        global offline, data, version
        # print(self.cur_nav)
        # print(data["account"]["login"])
        # print('{0:.6f}'.format(data["data"]["TON"]))
        with open("data.pickle", "wb") as f:
            pickle.dump({"account": data["account"], "data": data["data"]}, f)

            p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
            # print(p)
        try:
            if p != False and p != None and p < max_ping:
                # self.ids["wifi_error"].opacity = 0
                ref = db.reference(f"/version")
                if ref.get() > version:
                    # print(ref.get())
                    self.dialog = MDDialog(
                        text="Доступна новая версия TON clicker!\nЗагрузите её сейчас.",
                        radius=[20, 7, 20, 7],
                        auto_dismiss=False)
                    self.dialog.open()
                    version = 2

                if data["account"]["name"] and auth_succefull:
                    ref = db.reference(f"/players/{data['account']['name']}")
                    ref.set(data)
                    ref = db.reference(f"/players/{data['account']['name']}/account/ban/is_banned")

                    if ref.get() == "True":
                        data = no_data
                        self.game.show_alert_dialog(title="Вы забанены!", text=f'''
Вы забанены по пречине: {ref.get("cause")}.
Обратитесь за помошью в дискорд сервер.
Приятной игры!
                                        ''')
                    ref = db.reference(f"/players/{data['account']['name']}/account/privilege")
                    priv = ref.get()
                    if priv:
                        data["account"]["privilege"] = priv
                    # print(2222)

                # print(ref.get())

        except:
            pass

    def on_tap(self):
        # print('{0:.6f}'.format(data["data"]["TON"]))
        mouse = data["data"]["mouse"]
        if data["data"]["tired_num"] - float(Decimal(f'{data["data"]["inventory"][mouse]["tired"]}')) > 0:

            data["data"]["TON"] += data["data"]["inventory"][mouse]["boost"]
            data["data"]["tired_num"] -= float(Decimal(f'{data["data"]["inventory"][mouse]["tired"]}'))
        else:
            self.ads.show_interstitial()
        # data["data"]["is_tired"] = True
        # print(App.get_running_app().root.ids['hi'])

    def send_rasban(self):
        b = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=30
        )
        self.ban_name = MDTextFieldRound(
            hint_text="Ник игрока",
            font_name="main_font.ttf",
            icon_right="account",
            font_size=25,
            pos_hint={"center_x": .5},

            color_active=[1, 1, 1, 1]
        )
        c = MDFillRoundFlatButton(
            text="Разбанить",
            font_size="20sp",
            on_release=lambda a: self.rasban()
        )
        self.dialog = Popup(title="Разбанить", title_color=(0, 0, 0, 1), content=b, title_font="main_font.ttf",
                            title_align="center", title_size="30sp",
                            size_hint=(.9, .7), background="dialog_reg.png")

    def send_ban(self):
        b = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=30
        )
        self.ban_name = MDTextFieldRound(
            # hint_text="Ник игрока",
            # font_name="main_font.ttf",
            # icon_right="account",
            # font_size=25,
            # pos_hint={"center_x": .5},

            # color_active=(1, 1, 1, 1)
        )
        self.ban_cause = MDTextFieldRound(
            hint_text="Причина",
            font_name="main_font.ttf",
            icon_right="account",
            font_size=25,
            pos_hint={"center_x": .5},

            color_active=[1, 1, 1, 1]
        )
        c = MDFillRoundFlatButton(
            text="Забанить",
            font_size="20sp",
            on_release=lambda a: self.ban()
        )
        self.dialog = Popup(title="Забанить", title_color=(0, 0, 0, 1), content=b, title_font="main_font.ttf",
                            title_align="center", title_size="30sp",
                            size_hint=(.9, .7), background="dialog_reg.png")

    def rasban(self):
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
        # print(p)
        try:
            if p != False and p != None and p < max_ping:
                # self.ids["wifi_error"].opacity = 0
                ref = db.reference(f"/{self.ban_name.text}/ban")
                ref.set({"is_banned": False, "cause": None})
        except:
            pass

    def ban(self):
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
        # print(p)
        try:
            if p != False and p != None and p < max_ping:
                # self.ids["wifi_error"].opacity = 0
                ref = db.reference(f"/{self.ban_name.text}/ban")
                ref.set({"is_banned": True, "cause": self.ban_cause.text})
        except:
            pass

    def sign_out(self):
        # print(self.manager.current)
        global offline, data, cur_nav

        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")

        print(p)

        # if p != False and p != None and p < max_ping:
        # auth_succefull = False
        data = no_data
        set_data()
        self.ids[cur_nav].set_state()
        cur_nav = "nav_drawer2"
        self.ads.show_interstitial()
        auth_succefull = False
        # print(self.ids[cur_nav].state)
        # os.remove("data.pickle")
        # self.manager.current = "auth"
        # else:

    #             self.show_alert_dialog(title="Ошибка!", text='''
    # Проверьте подключение к интернету и попробуйте снова.
    # ''')
    def edit_profile(self):
        global auth_succefull
        # on_text_validate: root.load_avatar(self.text)
        # b.ids["b"].add_widget('''''')
        self.dialog = Popup(title="Редактировать профиль", title_color=(1, 1, 1, 1), title_font="main_font.ttf",
                            title_align="center", title_size="30sp",
                            size_hint=(.9, .7), background="dialog_reg.png")
        self.dialog.content = Edit_profile(dialog=self.dialog)
        self.dialog.open()
        auth_succefull = False
    def open_account_info(self):
        # print(33333)
        self.ids[cur_nav].set_state("open")

    def main_loop(self, dt):
        global auth_succefull
        # if auth_succefull:
        #     pass
        th = Thread(target=self.ui_update)
        th.start()
        # self.ui_update()

    def ui_update(self):

        self.ids["tokens_num_games"].text = f'''Жетоны: {data["data"]["token"]["value"]}'''
        self.ids["ton_num_shop"].text = f'''TON: {'{0:.6f}'.format(data["data"]["TON"])}'''
        # self.ids[
        #     "summation_text"].secondary_text = f'''Цена: {'{0:.6f}'.format(data["data"]["summation"]["price"])} TON'''
        # print(data["account"])
        if data["account"]["name"]:
            self.ids["player_name"].text = f'''Имя: {data["account"]["name"]}'''
            self.ids["privilege"].text = f'''{data["account"]["privilege"]}'''

            if data["account"]["privilege"] == "Админ":
                self.ids["privilege"].color = (1, 0, 0, 1)
            else:
                self.ids["privilege"].color = (0, 0, 0, 1)
            self.ids["player_password"].text = f'''Пароль: {data["account"]["password"]}'''
            self.ids["avatar"].source = data["account"]["avatar"]
        self.ids["token_price"].text = f'''Цена: {'{0:.6f}'.format(data["data"]["token"]["price"])} TON'''

        # print(data["account"])
        # self.ids[
        #     'text_doubling'].secondary_text = f'''Цена: {'{0:.6f}'.format(self.doubling_data["price"])} TON'''
        # self.ids[
        #     'text_doubling'].tertiary_text = f'''Увеличение до x{'{0:.6f}'.format(self.doubling_data["value"] / 100 * 30)}'''
        # Удвоение майнинга с:{data["data"]["doubling"] } на 30%

        #        self.ids[
        #            'text_summation'].secondary_text = f'''Цена: {'{0:.6f}'.format(self.summation_data["summation_price"])} TON'''
        self.ids['TON_num'].text = f'''TON: {'{0:.6f}'.format(data["data"]["TON"])}'''
        # self.ids['video_shop'].secondary_text = f'''цена: {'{0:.6f}'.format(data["data"]["bot"]["price"])} TON'''
        # self.ids['text_bot_summation'].secondary_text = f'''цена: {data["data"]["bot"]["summation_price"]} TON'''
        #
        #             #App.get_running_app().root.ids['TON_num_natural'].text = f"точнее: {data["data"]['TON']}"
        #
        self.ids["tired_num"].text = f"   {int(data['data']['tired_num'])}"
        # print(self.ids)

        for key, obj in self.ids["bot_shop"].ids.items():
            if obj.name not in data['data']["inventory"]:

                self.ids["bot_shop"].ids[key].opacity = 0
            else:
                self.ids["bot_shop"].ids[key].opacity = 1
        for key, obj in self.ids["mining_shop"].ids.items():
            if obj.name not in data['data']["inventory"]:
                self.ids["mining_shop"].ids[key].opacity = 0
            else:
                self.ids["mining_shop"].ids[key].opacity = 1

    def to_auth(self):
        self.ids[cur_nav].set_state()
        self.ads.show_interstitial()
        self.manager.current = "auth"

    def miner_loop(self, dt):
        global auth_succefull
        # if auth_succefull:
        th = Thread(target=self.autominer)
        th.start()
        th = Thread(target=self.update_data)
        th.start()
        # if self.ids["mining_button"].state != "down" and data['data']["tired_num"] < 30:
        #     data['data']["tired_num"] += 1

    def tired_loop(self, dt):
        global auth_succefull
        # if auth_succefull:

        if self.ids["mining_button"].state != "down" and data['data']["tired_num"] < 40:
            data['data']["tired_num"] += 1

    def autominer(self):
        if data['data']["bot"]["alow_bot"]:
            video = data['data']["bot"]["video card"]

            boost = data['data']["inventory"][video]["boost"]

            data['data']["TON"] += boost

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
                    on_press=lambda event: self.buy(obj=line)

                )

                # line.add_widget(image)
                self.ids["auction_items"].add_widget(line)

    def open_chest(self, is_bought=False):
        t_b = random.randint(1, 5)
        if t_b == 1:
            # type_index = random.randint(0, (len(self.bonuses) - 1) * 10)
            # bonuse_items = self.store_items[]
            bonuse_index = random.randint(0, len(self.store_items) * 20)
            bonuse_index = int(bonuse_index / 20)
            for name, item in self.store_items.items():
                if bonuse_index == item["index"]:

                    bonuse = name
                    if item["type"] == "video card" and item["index"] >= \
                            self.store_items[data['data']["bot"]["video card"]][
                                "index"]:
                        data['data']["bot"]["video card"] = bonuse
                        data["data"]["inventory"][bonuse] = self.store_items[bonuse]
                        self.main_dialog.dismiss()

                        self.show_alert_dialog(title="Поздравляем!", text=f"Вам выпала видеокарта {bonuse}!")
                    elif item["type"] == "mouse" and item["index"] >= self.mouses[data['data']["mouse"]]["index"]:
                        data['data']["mouse"] = bonuse
                        data["data"]["inventory"][bonuse] = self.store_items[bonuse]
                        self.main_dialog.dismiss()

                        self.show_alert_dialog(title="Поздравляем!", text=f"Вам выпала мышь {bonuse}!")
                    else:

                        r = random.randint(30, 100)
                        r /= 100
                        data['data']["TON"] += data['data']["TON"] * r
                        self.main_dialog.dismiss()
                        self.show_alert_dialog(title="Поздравляем!",
                                               text=f"Вам выпало {'{0:.6f}'.format(data['data']['TON'] * r)} TON!")
                    break
        else:

            r = random.randint(30, 100)
            r /= 100
            data['data']["TON"] += data['data']["TON"] * r
            self.close_dialog()
            self.show_alert_dialog(title="Поздравляем!",
                                   text=f"Вам выпало {'{0:.6f}'.format(data['data']['TON'] * r)} TON!")
        if is_bought:
            data["data"]["TON"] -= data["data"]["chest"]["price"]
            data["data"]["chest"]["price"] += data["data"]["chest"]["price"] * 0.2
        # day = data['data']["chest_last_opened"].day
        # hour = data['data']["chest_last_opened"].hour
        # minute = data['data']["chest_last_opened"].minute
        #
        # if datetime.now() >= data['data']["chest_last_opened"] + timedelta(hours=2):
        #     type_index = random.randint(0, len(self.bonuses) - 1)
        #     bonuse_items = self.bonuses[type_index]
        #     bonuse_index = random.randint(0, len(bonuse_items) - 1)
        #     for name, item in bonuse_items.items():
        #         if bonuse_index == item["index"]:
        #
        #             bonuse = name
        #             if item["type"] == "video card" and item["index"] >= self.store_items[data['data']["bot"]["video card"]]["index"]:
        #                 data['data']["bot"]["video card"] = bonuse
        #                 self.show_alert_dialog(title="Поздравляем!", text=f"Вам выпала видеокарта {bonuse}")
        #             elif item["type"] == "mouse" and item["index"] >= self.mouses[data['data']["mouse"]]["index"]:
        #                 data['data']["mouse"] = bonuse
        #                 self.show_alert_dialog(title="Поздравляем!", text=f"Вам выпала мышь {bonuse}")
        #             data['data']["chest_last_opened"] = datetime.now()
        #
        #             break
        # else:
        #     print(data['data']["chest_last_opened"], int(str(datetime.now().hour) + str(datetime.now().minute)))
        #
        #     self.show_alert_dialog(title="Ой!", text=f'До следующего бесплатного сундука осталось {data['data']["chest_last_opened"] + timedelta(hours=2) - datetime.now()}')

    def add_auction(self):
        pass

    def nav_type(self, nav_type):
        if nav_type == "not_authed":
            self.ids["nav_drawer"].clear_widgets()
            kv = Builder.load_string('''
MDBoxLayout:
    #id: False
    orientation: 'vertical'
    padding: "8dp"
    spacing: "8dp"
    MDFillRoundFlatButton:

        #size_hint: .3, .3
        text: "Авторизация"
        pos_hint: {"center_x":.5}

        font_size: 25
        on_press: app.game.manager.current = "auth"
                        ''')
            self.ids["nav_drawer"].add_widget(kv)
            self.navigation_state = None
        if nav_type == "authed":
            print(124)
            # self.ids["nav_drawer"].clear_widgets()
            # kv = Builder.load_string('''

            #            ''')
            # self.ids["nav_drawer"].add_widget(kv)
            # self.navigation_state = None


class Loading(Screen):
    pass


class app(MDApp):
    def on_start(self):
        from kivy.base import EventLoop

        # attaching keyboard hook when app starts
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):

        # key == 27 means it is waiting for
        # back button tobe pressed
        if key == 27:
            # checking if we are at mainscreen or not
            # if self.screen_manager.current == 'mainscreen':

            # return True means do nothing
            # print("Key 27")
            return True
            # else:

            # return anything except True result in
            # closing of the app on button click
            # if are not at mainscreen and if we press
            # back button the app will get terminated
            #    pass

    def build(self):
        global auth_succefull, already_auth, data
        # c = Clicker

        # Clock.schedule_interval(self.start_loops, 1/30)
        self.screen_manager = ScreenManager()
        self.screen_manager.transition = NoTransition()
        Logger.info('Loader: Screeen manager has been loaded.')
        loading = Loading(name="loading")
        # self.screen_manager.add_widget(Navigate_without_account(name="scr"))
        self.screen_manager.add_widget(loading)
        Logger.info('Loader: Spinner screen has been loaded.')
        self.screen_manager.current = "loading"

        print(123)

        auth = Auth(name="auth")
        self.screen_manager.add_widget(auth)
        Logger.info('Loader: Auth screen has been loaded.')
        # d = Error_show(name="error_show")
        # self.screen_manager.add_widget(d)
        # Logger.info('Loader: Error screen has been loaded.')

        self.game = Clicker(name="clicker")

        # self.game = Clicker(name="clicker")
        #
        # self.screen_manager.add_widget(self.game)
        Clock.schedule_interval(self.game.miner_loop, 1)
        Clock.schedule_interval(self.game.main_loop, 1 / 10)
        Clock.schedule_interval(self.game.tired_loop, 1)

        # self.load_store_items()
        self.screen_manager.add_widget(self.game)

        # th = Thread(target=self.start_game)
        # .start()

        self.start_game()
        self.load_store_items()
        # th = Thread(target=self.load_store_items)
        # th.start()

        return self.screen_manager

    def load_store_items(self):
        import time
        start_time = time.time()

        for i in self.game.store_items:

            name = self.game.store_items[i]["name"]
            price = self.game.store_items[i]["price"]
            # index = self.game.store_items[i]["index"]
            type_item = self.game.store_items[i]["type"]
            texture = self.game.store_items[i]["texture"]
            if name in data["data"]["inventory"]:
                # boost = self.game.store_items[i]["boost"]
                price = data["data"]["inventory"][i]["price"]
                # index = self.game.store_items[i]["index"]
                type_item = data["data"]["inventory"][i]["type"]
                texture = data["data"]["inventory"][i]["texture"]
            # print(texture)

            # print("list loading")

            line = TwoLineAvatarIconListItem(

                text=name,
                # source="",
                secondary_text=f"Цена: {'{0:.6f}'.format(price)} TON",
                # font_name="main_font.ttf",
                # font_style="Subtitle1",
                # type=type_card,
                on_press=self.game.buy_confirm
            )
            line.name = name
            # body = IRightBodyTouch()
            # body.add_widget(Check())
            if "." in texture:
                image = ImageLeftWidget(source=texture)
            else:
                image = IconLeftWidget(icon=texture)
            line.add_widget(image)

            # self.game.ids["bot_shop"].add_widget(MDLabel(text="hi"))
            if type_item == "video card" or type_item == "processor":
                check = Check(group="current_video card", on_press=self.game.current_item)

                check.name = name
                line.add_widget(check)
                self.game.ids["bot_shop"].ids[f"choose_current_{name}"] = check
                self.game.ids["bot_shop"].add_widget(line)
            elif type_item == "mouse":
                check = Check(group="current_mouse", on_press=self.game.current_item)

                check.name = name
                line.add_widget(check)
                self.game.ids["mining_shop"].ids[f"choose_current_{name}"] = check
                self.game.ids["mining_shop"].add_widget(line)
                # print(line.size)

        print("--- %s seconds ---" % (time.time() - start_time))

    def start_game(self):
        global data, auth_succefull, cur_nav

        #

        d = SoundLoader.load("soundtrack.wav")

        if d:
            d.loop = True
            d.volume = .3
            d.play()

        # firebase_admin.delete_app(firebase_admin.get_app())
        cred_obj = firebase_admin.credentials.Certificate(
            'ton-clicker-firebase-adminsdk-cf1xz-8ad3090323.json')
        app_d = firebase_admin.initialize_app(cred_obj, {
            'databaseURL': "https://ton-clicker-default-rtdb.firebaseio.com/"
        })

        # print(p == "False")f

        try:
            with open("data.pickle", "rb") as f:
                data = pickle.load(f)
                auth_succefull = True
            #     data.update({
            #     "account": {"name": None,
            #                 "login": None,
            #                 "password": None,
            #                 "avatar": None,
            #                 "privilege": "Игрок",
            #
            #                 },
            #     "data": {"TON": 0,
            #              "inventory": {"Oklick 105S": {"index": 0, "texture": "mouse-variant", "type": "mouse",
            #                                            "name": "Oklick 105S",
            #                                            "boost": 0.000001, "price": 0.000100, "tired": 1},
            #                            "Celeron Pro": {"index": 0, "texture": "video card.png",
            #                                            "name": "Celeron Pro", "type": "processor",
            #                                            "boost": 0.000001, "price": 0.000600}
            #                            },
            #
            #              "doubling": {"value": 1, "price": 0.001},
            #              "bot": {"alow_bot": False, "doubling": {"value": 1, "doubling_price": 0.001},
            #                      "video card": "Celeron Pro", "price": 1,
            #                      "summation_price": 0.000001, "summation_num": 0},
            #              "token": {"price": 0.000350, "value": 5},
            #              "summation": {"price": 0.000001, "value": 0.000001},
            #              # "chest_last_opened": datetime(year=2021,month=1,day=1,hour=1,minute=1),
            #              "chest": {"num": 1, "price": 0.00015, "last_opened": datetime.datetime.now().isoformat()},
            #              "mouse": "Oklick 105S",
            #              "tired_num": 40,
            #              "is_tired": False,
            #
            #              }
            # })
            # print(data["account"])

        except:
            data = no_data
            auth_succefull = False
        # while True:
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
        # self.game.nav_type(nav_type="not_authed")
        try:
            if p != False and p != None and p < max_ping:

                ref = db.reference(f"/lock_app")
                d = ref.get()
                if d == "True":
                    raise BaseException("It is Star Wormwood inc. project!")

                if data["account"]["name"]:
                    ref = db.reference(f"/players/{data['account']['login']}")

                    ref.set(data)

                    # auth_succefull = True
                    # self.game.nav_type(nav_type="authed")

                    # self.navigation_state = "is_auth"
                    # self.screen_manager.current = "clicker"

            self.screen_manager.current = "clicker"

            set_data()

            if data["account"]["name"]:
                cur_nav = "nav_drawer1"
            else:
                cur_nav = "nav_drawer2"
            # if data["account"]["privilege"] == "Admin":
            #     b = OneLineIconListItem(
            #
            #         text="Выдать бан",
            #         on_release=lambda a: self.game.send_ban(),
            #
            #     )
            #     i = IconLeftWidget(
            #         icon="cancel"
            #     )
            #     b.add_widget(i)
            #     self.game.ids["nav_drawer_items"].add_widget(b)

        except:
            pass

        # self.cur_nav = "nav_drawer1"
    # def donate(self):
    #
    #     b = FloatLayout(pos_hint={"center_x": .5, "center_y": .5})
    #     self.amount = MDTextField(hint_text="Введите сумму пожертвования", mode="fill",
    #                               pos_hint={"center_x": .5, "center_y": .8}, helper_text_mode="on_error",
    #                               helper_text="Сумма не корректна")
    #
    #     b.add_widget(self.amount)
    #     b.add_widget(MDFillRoundFlatButton(text="Пожертвовать", font_name="main_font.ttf", font_size="35sp",
    #                                        md_bg_color=(0.1, 0.6, 0.9, 1.0),
    #                                        pos_hint={"center_x": .5, "center_y": .15},
    #                                        on_press=self.on_donate))
    #     self.dialog = Popup(title="Помочь", title_color=(0, 0, 0, 1), title_font="main_font.ttf",
    #                         separator_color=(1, 1, 1, 1), title_align="center", title_size="30sp", content=b,
    #                         size_hint=(.9, .5), background="dialog.png")
    #     self.dialog.open()
    #
    # def on_donate(self, event):
    #
    #     if not self.amount.text.isdigit():
    #         self.amount.error = True
    #     elif self.amount.text.isdigit() and int(self.amount.text) < 1000000000:
    #         self.amount.error = False
    #         api = Api(merchant_id=1396424,
    #                   secret_key='test')
    #         checkout = Checkout(api=api)
    #         data = {
    #             "currency": "RUB",
    #             "amount": int(self.amount.text) * 100
    #         }
    #         url = checkout.url(data).get('checkout_url')
    #         webbrowser.open(url)


# Запуск проекта
if __name__ == "__main__":
    import asyncio

    #
    # from kivy.app import async_runTouchApp
    # from kivy.uix.label import Label
    #
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(
    #     async_runTouchApp(app(), async_lib='asyncio'))
    # loop.close()
    app().run()
up_data = False
