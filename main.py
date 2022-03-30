# import webbrowser
import copy

from kivy.base import EventLoop
import webbrowser
from kivy.uix.button import Button
from kivymd.uix.list import IconLeftWidget
from kivy.uix.screenmanager import *
# from kivymd.uix.button import MDIconButton
from kivmob import KivMob, RewardedListenerInterface, TestIds
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDIconButton, MDFillRoundFlatButton, MDFillRoundFlatIconButton
from kivy.core.audio import SoundLoader
from functools import partial
import pickle
from kivymd.uix.textfield import MDTextFieldRound, MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.tab import MDTabsBase
from decimal import Decimal
from kivymd.uix.snackbar import Snackbar
from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.utils import get_hex_from_color

main_font_size = 20
import os
import requests
import firebase_admin
from firebase_admin import db
import random
import time
from ping3 import ping
from threading import Thread
from kivy.logger import Logger
from kivymd.uix.list import TwoLineAvatarIconListItem, OneLineIconListItem
from kivy.uix.popup import Popup
from kivymd.uix.floatlayout import FloatLayout, MDFloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import copy
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import IRightBodyTouch, IRightBody, ILeftBody, ImageLeftWidget, ImageRightWidget
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.image import AsyncImage, Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.animation import Animation
# from kivy.uix.boxlayout import BoxLayout
import datetime
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.graphics import RoundedRectangle
import asynckivy as ak
from kivy.uix.tabbedpanel import TabbedPanel
import re
# from kivy.lang.builder import Builder
from os.path import join, dirname, realpath
import plyer
from Account import Auth, CustomLabel, show_dialog, db
import Account

try:
    from plyer.platforms.android.notification import AndroidNotification as notification
except:
    print("Platform: windows")
up_data = True
auth_succefull = False
offline = False
already_auth = False
#data = {}
#cur_nav = "nav_drawer2"
max_ping = 300
version = "2.4.9"
notifications = []
store_items = {
    "Celeron Pro": {"index": 0, "texture": "video card.png", "name": "Celeron Pro", "type": "processor",
                    "boost": 0.000001, "price": 0.100000},
    "Gt 770": {"index": 1, "texture": "video card.png", "name": "Gt 770", "type": "video card",
               "boost": 0.000020, "price": 1.000000},
    "Gt 870": {"index": 2, "texture": "video card.png", "name": "Gt 870", "type": "video card",
               "boost": 0.000020, "price": 1.589000},
    "Intel Xeon E3": {"index": 3, "texture": "video card.png", "name": "Intel Xeon E3", "type": "video card",
                      "boost": 0.000034, "price": 2.000000},
    "AMD FX-8300": {"index": 4, "texture": "video card.png", "name": "AMD FX-8300", "type": "video card",
                    "boost": 0.000040, "price": 2.500000},
    "Intel Core i7-5960X": {"index": 5, "texture": "video card.png", "name": "Intel Core i7-5960X",
                            "type": "video card",
                            "boost": 0.000056, "price": 2.960000},
    "Intel Core i7-6700K": {"index": 6, "texture": "video card.png", "name": "Intel Core i7-6700K",
                            "type": "video card",
                            "boost": 0.000078, "price": 3.500000},
    "Sapphire NITRO": {"index": 7, "texture": "video card.png", "name": "Sapphire NITRO", "type": "video card",
                       "boost": 0.00089, "price": 4.300000},
    "Gtx 970": {"index": 8, "texture": "video card.png", "name": "Gtx 970", "type": "video card",
                "boost": 0.000099, "price": 5.000000},
    "Rtx 3090 Super TI": {"index": 9, "texture": "video card.png", "name": "Gtx 970", "type": "video card",
                          "boost": 0.000114, "price": 5.000000},
    "Rtx 8000 Super TI Extreme": {"index": 10, "texture": "video card.png", "name": "Gtx 970", "type": "video card",
                                  "boost": 0.000130, "price": 5.000000},
    "GeForce RTX Founders": {"index": 11, "texture": "video card.png", "name": "Gtx 970", "type": "video card",
                             "boost": 0.000150, "price": 5.000000},
    "Rtx 1050": {"index": 12, "texture": "video card.png", "name": "Rtx 1050", "type": "video card",
                 "boost": 0.000165, "price": 6.000000},
    "Rtx 1070": {"index": 13, "texture": "video card.png", "name": "Rtx 1070", "type": "video card",
                 "boost": 0.000180, "price": 6.900000},
    "Rtx 2060": {"index": 14, "texture": "video card.png", "name": "Rtx 2060", "type": "video card",
                 "boost": 0.000190, "price": 7.700000},
    "Rtx 2070 Super": {"index": 15, "texture": "video card.png", "name": "Rtx 2070 Super", "type": "video card",
                       "boost": 0.000205, "price": 8.400000},
    "Rtx 2080 TI": {"index": 16, "texture": "video card.png", "name": "Rtx 2080 TI", "type": "video card",
                    "boost": 0.000220, "price": 10.000000},
    "Rtx 3060 TI Super)": {"index": 17, "texture": "video card.png", "name": "Rtx 3060 TI Super)", "type": "video card",
                           "boost": 0.000270, "price": 15.000000},

    "Oklick 105S": {"index": 0, "texture": "mouse-variant", "type": "mouse", "name": "Oklick 105S",
                    "boost": 0.000001, "price": 0.000100, "tired": 2},
    "Canyon CNE-CMS05DG": {"index": 1, "texture": "mouse-variant", "type": "mouse",
                           "name": "Canyon CNE-CMS05DG", "boost": 0.00001, "price": 0.002000, "tired": 2},

    "Logitech G-502": {"index": 2, "texture": "mouse-variant", "type": "mouse",
                       "name": "Logitech G-502", "boost": 0.000005, "price": 0.006000, "tired": 2},
    "Razer EPIC-8": {"index": 3, "texture": "mouse-variant", "type": "mouse",
                     "name": "Razer EPIC-8", "boost": 0.00001, "price": 0.009000, "tired": 2},
    "Corsair M-65": {"index": 4, "texture": "mouse-variant", "type": "mouse",
                     "name": "Corsair M-65", "boost": 0.000014, "price": 0.020000, "tired": 2},

    "Razer Basilisk": {"index": 5, "texture": "mouse-variant", "type": "mouse",
                       "name": "Corsair M-65", "boost": 0.000029, "price": 0.020000, "tired": 2},
    "Razer Naga Trinity": {"index": 6, "texture": "mouse-variant", "type": "mouse",
                           "name": "Corsair M-65", "boost": 0.000037, "price": 0.020000, "tired": 2},

    "Razer Death": {"index": 7, "texture": "mouse-variant", "type": "mouse",
                    "name": "Razer Death", "boost": 0.000046, "price": 0.027000, "tired": 2},
    "LOGITECH G302": {"index": 8, "texture": "mouse-variant", "type": "mouse",
                      "name": "LOGITECH G302", "boost": 0.000051, "price": 0.030000, "tired": 2},
    "Zalman ZM-M300": {"index": 9, "texture": "mouse-variant", "type": "mouse",
                       "name": "Zalman ZM-M300", "boost": 0.000065, "price": 0.033200, "tired": 2},
    "SteelSeries Rival": {"index": 10, "texture": "mouse-variant", "type": "mouse",
                          "name": "SteelSeries Rival", "boost": 0.000070, "price": 0.037000, "tired": 2},
    "QUMO Office M14": {"index": 11, "texture": "mouse-variant", "type": "mouse", "name": "QUMO Office M14",
                        "boost": 0.000085, "price": 0.040000, "tired": 2},
    "Ritmix ROM-111": {"index": 12, "texture": "mouse-variant", "type": "mouse", "name": "Ritmix ROM-111",
                       "boost": 0.000097, "price": 0.043000, "tired": 2},
    "Oklick 145M": {"index": 13, "texture": "mouse-variant", "type": "mouse", "name": "Oklick 145M",
                    "boost": 0.000105, "price": 0.090000, "tired": 2},
    "Ritmix ROM-202": {"index": 14, "texture": "mouse-variant", "type": "mouse", "name": "Ritmix ROM-202",
                       "boost": 0.000115, "price": 10.990000, "tired": 2},
    "Smartbuy ONE SBM-265-K": {"index": 15, "texture": "mouse-variant", "type": "mouse",
                               "name": "Smartbuy ONE SBM-265-K", "boost": 0.000125, "price": 1000.000000,
                               "tired": 2},

}
bonuse_items_names = {

    "Logitech G-502": {"type_effect": "disable_tired", "chance": 20},
    "Razer Basilisk": {"type_effect": "disable_tired", "chance": 25},
    "Rtx 3090 Super TI": {"type_effect": "double_click", "lvl": 2, "chance": 7},
    "Rtx 8000 Super TI Extreme": {"type_effect": "double_click", "lvl": 2, "chance": 7},
    "GeForce RTX Founders": {"type_effect": "double_click", "lvl": 2, "chance": 7},
    "Razer Naga Trinity": {"type_effect": "double_click", "lvl": 2, "chance": 10},

}
no_data = {
    "account": {},
    "data": {"TON": 0,

             # "doubling": {"value": 1, "price": 0.001},
             "bot": {"alow_bot": False,
                     "video card": "Celeron Pro", "price": 1,
                     "active": False,
                     },
             # "token": {"price": 0.000100, "value": 5},
             # "summation": {"price": 0.000001, "value": 0.000001},
             # "chest_last_opened": datetime(year=2021,month=1,day=1,hour=1,minute=1),
             "chest": {"num": 1, "price": 0.000150, "last_opened": datetime.datetime.now().isoformat()},
             "mouse": "Oklick 105S",
             "tired_num": 100,
             "is_tired": False,

             }
}

t = 0

threads = {}


def set_data():
    c = Clicker

    c.account = Account.data["account"]
    c.player_data = Account.data["data"]
    c.bot_data = Account.data["data"]["bot"]
    c.doubling_data = Account.data["data"]["doubling"]
    c.summation_data = Account.data["data"]["summation"]

    # adaptive_width = True


def check_lost_keys():
    if "active" not in Account.data["data"]["bot"]:
        Account.data["data"]["bot"]["active"] = False


def timer(command, seconds=1, name=None):
    if not name:
        name = random.uniform(0, 1000)
    if name not in threads:
        th = Thread(target=lambda: start_timer(command, name, seconds))
        threads[name] = th

        th.start()


def start_timer(command, name, seconds=1):
    # for i in range(seconds):
    # for i in range(seconds):

    time.sleep(seconds)
    Clock.schedule_once(lambda dt: command())
    threads.pop(name)





# import pygame
class Rewards_Handler(RewardedListenerInterface):

    def __init__(self, other):
        self.AppObj = other

    Reward = "None"
    Reward_Amount = "None"

    def on_rewarded(self, reward_name, reward_amount):

        self.Reward = reward_name
        self.Reward_Amount = reward_amount
        Account.data["data"]["tired_num"] += reward_amount

    def on_rewarded_video_ad_completed(self):
        self.on_rewarded(self.Reward, self.Reward_Amount)

    def on_rewarded_video_ad_started(self):
        self.AppObj.load_video()

    def on_rewarded_video_ad_left_application(self):
        pass


class RoundedRectangleButton(Button):
    pass


class Test(TabbedPanel):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.on_tab_width, 0.1)


# class ImageLeftWidget(ILeftBody, AsyncImage):
#     pass
class GameTemplate(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.finded_numbers = 0

    def load_template(self, *args):
        # name = args[0]
        name, self.find_li, self.bet = args
        self.platform = GridLayout(
            pos_hint={"center_x": .5},
            cols=5,
            size_hint=(.5, .5)
        )
        self.add_widget(self.platform)
        self.add_widget(CustomLabel(
            text=f"Текущий выигрыш: ",
            font_name="main_font.ttf",
            font_size="25sp"
        ))
        self.add_widget(MDFillRoundFlatIconButton(
            text="Забрать",
            font_size="25sp",
            font_name="main_font.ttf",
            color=(1, .1, .1, 1),
            on_press=lambda a: self.is_won(name="bombs")
        ))
        for y in range(5):
            for x in range(5):
                b = ButImage(size=(.1, .1), source="card_normal.jpg", pos_hint={"x": x * .1, "y": y * .1},
                             )
                # b.bind()
                b.name = "bombs"
                if self.find_li[y][x] == 1:
                    b.bind(on_press=self.game_process)
                else:
                    b.bind(on_press=self.is_loose)
                # b.background_normal = "card_normal.jpg"
                # self.ids["withdraw_bombs"].opacity = 1

                # self.ids["find_it_start_button"].opacity = 0
                # self.ids["bombs_platform"].opacity = 1
                self.platform.add_widget(platform)
        # self.ids["find_bombs_field"].disabled = False
        # self.ids["find_bombs_field"].opacity = 1
        # self.ids["bombs_platform"].opacity = 1

    # except:
    #    self.ids['bet_find_it'].helper_text = "Ставка не корректна!"
    #    self.ids['bet_find_it'].error = True

    def show_bet_find_it_value(self, obj):
        self.ids["text_find_it"].text = f'Ваша ставка: {"{0:.6f}".format(data["data"]["TON"] / 100 * obj.value)} TON'

    def game_process(self, obj):
        if obj.name == "bombs":
            self.finded_numbers += 1

    def is_won(self, name):
        if name.name == "bombs":
            name.source = "card_loose.jpg"
            n = 0
            # bombs_count = 0
            # for i in self.finded_numbers:
            # if i.name == 1:

            # self.finded_numbers = []
            # time.sleep(1)
            title = "Поздравляем!"
            # if self.finded_numbers > 0: title = "Поздравляем!"
            # else: title =
            # print(self.bet)
            show_dialog(title=title,
                        text=f"Вы прошли: {self.finded_numbers} плит\nВы выиграли {'{0:.6f}'.format(self.finded_numbers * self.bet)} TON",
                        command=self.undo_find_it)
            Account.data["data"]["TON"] += self.finded_numbers * self.bet
            self.finded_numbers = 0

    def is_loose(self, name):
        if name.name == "bombs":
            show_dialog(title="Увы!",
                        text=f"Проиграли {'{0:.6f}'.format(self.finded_numbers * self.bet)} TON.",
                        command=self.undo_find_it)

    def undo_find_it(self):
        self.clear_widgets()


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

        if p and p < max_ping:
            auth_succefull = False
            os.remove("data.pickle")
            self.game.manager.current = "auth"
        else:

            show_dialog(title="Ошибка!", text='''
Проверьте подключение к интернету и попробуйте снова.
        ''')

    def show_alert_dialog(self, title, text, command=lambda: print("Hello!")):
        # lambda
        self.dialog = None
        if not self.dialog:
            b = MDBoxLayout(
                orientation="vertical",
                # padding=20,
                size_hint_y=.8,
                pos_hint={"center_y": .5},
                spacing=30
            )
            b.add_widget(
                CustomLabel(text=text,
                            halign="center",
                            font_name="main_font.ttf",
                            font_size="20sp",

                            # theme_text_color="Custom",
                            # color=(0, 0, 0, 1),
                            )
            )
            c2 = MDFillRoundFlatButton(
                text="Ок",
                font_size="25sp",
                font_name="main_font.ttf",
                # halign="center",
                pos_hint={"center_x": .5},
                size_hint=(.3, None),

            )
            b.add_widget(c2)
            # b.add_widget(b2)
            self.dialog = Popup(title=title, title_color=(0, 0, 0, 1), separator_height="4dp",
                                title_font="main_font.ttf",
                                title_align="center", title_size="30sp", content=b,
                                size_hint=(.9, .7), background="dialog.png")
            c2.bind(on_press=[self.dialog.dismiss(), command()])

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

        if p and p < max_ping:
            auth_succefull = False
            os.remove("data.pickle")
            self.manager.current = "auth"
        else:

            show_dialog(title="Ошибка!", text='''
Проверьте подключение к интернету и попробуйте снова.
        ''')


class Edit_profile(MDBoxLayout):
    def __init__(self, dialog, **kwargs):
        super().__init__(**kwargs)
        self.main_dialog = dialog
        self.ids["avatar"].text = Account.data["account"]["avatar"]
        self.ids["name_r"].text = Account.data["account"]["name"]
        self.ids["password_r"].text = Account.data["account"]["password"]

    def close_dialog(self):
        if self.dialog:
            self.dialog.dismiss()

    def load_avatar(self, p):
        if p:
            self.ids["avatar_image"].source = p
        else:
            self.ids["avatar_image"].source = "classic_avatar.png"

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
        if p and p < max_ping:

            if player_password != "" and player_name != "" and string_check == None:
                # print(string_check)
                try:
                    ref = db.reference(f"/players/{player_name}")
                    account = ref.get()

                    if account == None:
                        # account = Account.data["account"]
                        ref = db.reference(f'/players/{data["account"]["name"]}')
                        ref.delete()

                        Account.data["account"]["name"] = player_name
                        Account.data["account"]["login"] = player_name
                        Account.data["account"]["password"] = player_password
                        Account.data["account"]["avatar"] = avatar

                        # print(data["account"]["privilege"])
                        # print(data["account"])
                        self.main_dialog.dismiss()
                        # set_data()

                        # p = ping('ton-clicker-default-rtdb.firebaseio.com', unit="ms")

                        ref = db.reference(f"/players/{player_name}")
                        ref.set(data)
                        # os.remove("avatar.png")
                        auth_succefull = True
                        # self.start_loops()
                    elif account["name"] == Account.data["account"]["name"]:
                        # self.manager.transition = NoTransition()
                        # self.manager.current = "auth"
                        show_dialog('''
Некоторые данные совпадают с предыдущими!
                                    ''')
                    else:
                        # self.manager.transition = NoTransition()
                        # self.manager.current = "auth"
                        show_dialog('''
Аккаунт с таким ником уже существует!
Придумайте новый!
            ''')

                except:
                    # self.manager.current = "auth"
                    show_dialog('''
Ошибка подключения!
Повторите попытку!
                                            ''')

            elif string_check:
                # self.manager.current = "auth"
                show_dialog('''
Все поля должны быть заполнены!
И не должны содержать специальные симбволы: пробела и '[#$. /?]'
            ''')
        else:
            # self.manager.current = "auth"
            show_dialog('''
Ошибка подключения!
Повторите попытку!
                        ''')


class RightText(IRightBody, Label):
    pass


class Check(MDCheckbox, IRightBodyTouch):
    pass


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


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




class ButImage(ButtonBehavior, Image):
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
                Account.data = pickle.load(f)

                offline = True
                auth_succefull = True
                # set_data()
                self.manager.current = "clicker"

        except:
            show_dialog(text='''
Вы не вошли в свой аккаунт!
Подключитесь к интернету и войдите в систему.            
''')
            offline = False

    def reconnect(self):

        global auth_succefull, data
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")

        if p and p < max_ping:

            # firebase_admin.delete_app(firebase_admin.get_app())
            cred_obj = firebase_admin.credentials.Certificate('ton-clicker-firebase-adminsdk-cf1xz-8ad3090323.json')
            app_d = firebase_admin.initialize_app(cred_obj, {
                'databaseURL': "https://ton-clicker-default-rtdb.firebaseio.com/"
            })

            try:
                with open("data.pickle", "rb") as f:
                    Account.data = pickle.load(f)

                    ref = db.reference(f"/players/{data['account']['login']}")
                    ref.set(data)

                auth_succefull = True
                # set_data()
                self.manager.current = "clicker"

            except:

                self.manager.current = "auth"



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
    # #set_data()
    def __init__(self, **kwargs):
        import time
        start_time = time.time()
        # self.start_game()
        # self.screen_manager.current = "clicker"

        super().__init__(**kwargs)
        print("--- %s seconds ---" % (time.time() - start_time))
        # self.f1 = Widget()

        # Logger.info('Loader: Game screen has been loaded.')
        # print(122222222222222222222222222)
        # self.main_font_size = main_font_size
        self.connect_error = False
        self.name = "clicker"
        # self.bitcoin = 0
        # self.bitcoin = 0
        self.bombs = None
        # self.size_hint = (1,1)

        self.money = {
            "0.000050": {"type": "TON", "index": 0},
            "0.000100": {"type": "TON", "index": 1},
            "0.000150": {"type": "TON", "index": 2},
            "0.000200": {"type": "TON", "index": 3},
            "0.000250": {"type": "TON", "index": 4},

        }
        # import sys
        self.stage = 0
        self.i = 0
        self.tr = None
        # print(sys.getsizeof(store_items))
        self.bonuses = [self.money, store_items]
        self.n = 0
        self.update_nav_drawer = False
        self.current_effect = {"name": None, "time": 0, "lvl": 0}
        # self.cur_nav = "nav_drawer2"
        # self.rewards = Rewards_Handler(self)
        # self.ads = KivMob("ca-app-pub-9371118693960899~5621013296")
        # print(TestIds.REWARDED_VIDEO)
        # self.ads.load_rewarded_ad("ca-app-pub-9371118693960899/9603139268")
        # Add any callback functionality to this class.
        self.rewards = Rewards_Handler(self)
        self.ads = KivMob("ca-app-pub-9371118693960899~5621013296")
        # print(TestIds.APP)
        self.ads.new_banner(TestIds.BANNER, False)
        self.ads.new_interstitial("ca-app-pub-9371118693960899/7807033752")
        self.ads.request_banner()
        self.ads.request_interstitial()
        self.ads.set_rewarded_ad_listener(self.rewards)
        self.ads.load_rewarded_ad("ca-app-pub-9371118693960899/9603139268")
        # self.ads = KivMob("ca-app-pub-9371118693960899~5621013296")
        # self.ads.load_rewarded_ad("ca-app-pub-9371118693960899/9603139268")
        # self.ads.new_interstitial("ca-app-pub-9371118693960899/5940984013")
        self.show_banner = False
        # Add any callback functionality to this class.
        # self.ads.set_rewarded_ad_listener(RewardedListenerInterface())

        # def set_data(self):
        #     global auth_succefull
        #     self.account = Account.data["account"]
        #     self.player_data = Account.data["data"]
        #     self.bot_data = Account.data["data"]["bot"]
        #     self.summation_data = Account.data["data"]["summation"]
        self.finded_numbers = []
        self.toggled = False

    def toggle_banner(self):
        self.show_banner = not self.show_banner
        if self.show_banner:
            self.ads.show_banner()
        else:
            self.ads.hide_banner()

    def load_video(self):
        self.ads.load_rewarded_ad("ca-app-pub-9371118693960899/9603139268")

    def open_link(self, link):
        webbrowser.open(link)

    def open_support(self):
        b = MDBoxLayout(orientation="vertical")
        b.add_widget(CustomLabel(text=f'[ref=https://t.me/ast4gost]Наш Telegram[/ref]',
                                 halign="center",
                                 font_name="main_font.ttf",
                                 font_size="35sp",
                                 on_ref_press=lambda a, d: self.open_link("https://t.me/ast4gost"),
                                 # theme_text_color="Custom",
                                 color=(.1, .1, 1, 1),
                                 markup=True
                                 )
                     )

        b.add_widget(CustomLabel(
            text=f'[ref=https://discord.gg/PQyktZGhyE]Наш Disord[/ref]',
            halign="center",
            font_name="main_font.ttf",
            font_size="35sp",
            color=(.1, .1, 1, 1),
            # theme_text_color="Custom",
            # text_color=(1,1,1,1)
            on_ref_press=lambda a, d: self.open_link("https://discord.gg/PQyktZGhyE"),
            markup=True
        )
        )

        b.add_widget(
            MDFillRoundFlatButton(text="Отмена", md_bg_color=(0.1, 0.6, 0.9, 1.0), font_name="main_font.ttf",
                                  font_size="25sp",
                                  pos_hint={"center_x": .5},
                                  on_press=lambda a: self.close_dialog()))
        # b.add_widget(b)
        # b.add_widget(MDLabel(text="Описание: Увеличивает майнинг в x раз"))
        # Buy_content(price=self.doubling_data["price"], boost=f'Увеличение удвоения майнинга с {self.doubling_data["price"]} TON/клик до {self.doubling_data["value"] + self.doubling_data["value"] / 100 * 30} TON/клик', description="Увеличивает майнинг в x раз"),
        self.dialog = Popup(title="Наши контакты", title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                            title_align="center", title_size="30sp", content=b,
                            size_hint=(.9, .7), background="dialog.png")
        #
        self.dialog.open()

    def current_item(self, obj):
        # print(222)
        name = obj.name

        # print(self.player_data["inventory"][name]["type"])
        if Account.data["data"]["inventory"][name]["type"] == "video card" or Account.data["data"]["inventory"][name][
            "type"] == "processor":
            Account.data["data"]["bot"]["video card"] = name
            Snackbar(text=f"Выбрана видеокарта {name}",
                     snackbar_x="10dp",
                     snackbar_y="15dp",

                     pos_hint={"center_x": .5},
                     duration=.1).open()
            # print(data["data"]["bot"]["video card"])
        if Account.data["data"]["inventory"][name]["type"] == "mouse":
            Account.data["data"]["mouse"] = name
            Snackbar(text=f"Выбрана мышка {name}",
                     snackbar_x="10dp",
                     snackbar_y="15dp",

                     pos_hint={"center_x": .5},
                     duration=.1).open()

    def load_top(self):
        self.ids["error_load_top"].opacity = 0
        self.ids["loading_top_text"].opacity = 1
        # self.ids["fl"].opacity = 0
        # self.ids["scroll_top"].opacity = 0
        # self.ids["scroll_top"].do_scroll = False
        # self.ids["retry_load_top"].opacity = 0
        # self.ids["top_loading"].active = False

        # self.ids["top_loading"].active = True

        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")

        if p and p < max_ping:
            # try:
            # self.ids["fl"].disabled = True
            # Clock.schedule_once(ld)

            # self.ids["top_loading"].active = False
            import time
            start_time = time.time()
            # self.start_game()
            # self.screen_manager.current = "clicker"
            #
            # Clock.schedule_once(self.loading_top)
            # self.loading_top()
            # self.loading_top()

            Thread(target=self.loading_top).start()

            print("--- %s seconds ---" % (time.time() - start_time))
            # self.loading_top()

        else:
            self.ids["loading_top_text"].opacity = 0
            self.ids["players_top"].opacity = 0
            self.ids["players_top"].disabled = True
            self.ids["error_load_top"].opacity = 1
            # self.ids["players_top"].add_widget(
        #     CustomLabel(text="Произошла ошибка подключения!\nОбновите список заново", font_name="main_font.ttf",
        #                 font_size="25sp"))
        # self.ids["fl"].disabled = False
        # self.ids["error_load_top"].opacity = 1
        # self.ids["retry_load_top"].opacity = 1
        # self.ids["top_loading"].active = False

    def bot_state(self, state):
        if state == "on":
            Account.data["data"]["bot"]["active"] = True
        if state == "off":
            Account.data["data"]["bot"]["active"] = False

    def open_ban_dialog(self, obj=None):

        b = MDBoxLayout(
            orientation="vertical",
            # padding=20,
            size_hint_y=.8,
            pos_hint={"center_y": .5},
            spacing=30
        )

        if not obj:
            self.player = MDTextField(
                hint_text="Имя",
                font_name="main_font.ttf",
                # icon_right="account",
                font_size="20sp",
                pos_hint={"center_x": .5},
                # on_focus=self.seach_player(),
                # color_active=[1, 1, 1, 1],
                helper_text="Сумма не корректна!",
                helper_text_mode="on_error"
            )
            b.add_widget(self.player)
            # name = player.text
        else:
            name = obj.name
        cause = MDTextField(
            hint_text="Причина",
            font_name="main_font.ttf",
            # icon_right="account",
            font_size="20sp",
            pos_hint={"center_x": .5},
            # on_focus=self.seach_player(),
            # color_active=[1, 1, 1, 1],
            helper_text="Сумма не корректна!",
            helper_text_mode="on_error"
        )
        b.add_widget(cause)
        b2 = MDBoxLayout(
            # orientation="vertical",
            # size_hint_y=.5,
            # md_bg_color=(1,0,0,1),
            # padding=20,
            spacing="2sp"
        )
        c2 = MDFillRoundFlatButton(
            text="Отмена",
            font_name="main_font.ttf",
            font_size="20sp",
            size_hint=(.3, None),
        )
        b2.add_widget(c2)
        c = MDFillRoundFlatButton(
            text="Забанить",
            font_name="main_font.ttf",
            font_size="20sp",
            size_hint=(.3, None),

        )
        b2.add_widget(c)

        b.add_widget(b2)
        ban_dialog = Popup(title="Забанить?", title_color=(0, 0, 0, 1), content=b, title_font="main_font.ttf",
                           title_align="center", title_size="30sp",
                           size_hint=(.9, .7), background="dialog.png")
        c2.bind(on_release=lambda a: ban_dialog.dismiss())
        c.bind(on_release=lambda a: self.send_ban(obj=ban_dialog, name=self.player.text, cause=cause.text))
        ban_dialog.open()

    def open_info_dialog(self, obj):
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
        # print(p)
        try:
            if p and p < max_ping:
                info = db.reference(f"/players/{obj.name}/data").get()
                b = MDBoxLayout(
                    orientation="vertical",
                    # padding=20,
                    size_hint_y=.8,
                    pos_hint={"center_y": .5},
                    spacing=30
                )
                if info["bot"]["active"]:
                    alow_bot = "Активен"
                else:
                    alow_bot = "Неактивен"
                if not info["bot"]["active"]:
                    alow_bot = "Не куплен"
                l = CustomLabel(
                    text=f'''
Всего открыто предметов: {len(info["inventory"])}
Майнинг: {'{0:.6f}'.format(info["inventory"][info["mouse"]]["boost"])} TON за клик
                    ''',
                    font_name="main_font.ttf",
                    font_size="25sp",
                    halign="center",
                    pos_hint={"center_x": .5, "center_y": .85},
                    markup=True,

                )
                b.add_widget(l)
                b2 = MDBoxLayout(
                    # orientation="vertical",
                    size_hint_y=.3,
                    # md_bg_color=(1,0,0,1),
                    # padding=20,

                    spacing="2sp"
                )
                c2 = MDFillRoundFlatButton(
                    text="Закрыть",
                    font_name="main_font.ttf",
                    font_size="20sp",
                    size_hint=(.3, None),
                )
                b2.add_widget(c2)
                if Account.data["account"].get("privilege") == "Админ":
                    c = MDFillRoundFlatButton(
                        text="Забанить",
                        font_name="main_font.ttf",
                        font_size="20sp",
                        size_hint=(.3, None),

                    )
                    b2.add_widget(c)

                b.add_widget(b2)
                ban_dialog = Popup(title=obj.name, title_color=(0, 0, 0, 1), content=b, title_font="main_font.ttf",
                                   title_align="center", title_size="30sp",
                                   size_hint=(.9, .7), background="dialog.png")
                c2.bind(on_release=lambda a: ban_dialog.dismiss())
                if Account.data["account"].get("privilege") == "Админ":
                    c.bind(on_release=lambda a: (self.open_ban_dialog(obj=obj), ban_dialog.dismiss()))
                ban_dialog.open()
            else:
                show_dialog(title="Ошибка!", text='''
Ошибка подключения!
Повторите попытку!
                            ''')

        except:
            # else:
            # print(133)
            show_dialog(title="Ошибка!", text='''
Ошибка подключения!
Повторите попытку!
                                        ''')

    def loading_top(self):
        ref = db.reference(f'/players/')
        sorted_data = ref.order_by_child(f'data/TON').limit_to_last(30).get()
        results = list(sorted_data)

        def lt(dt):
            stage = 0
            self.ads.show_interstitial()
            if self.ids["players_top"].children:
                for i in range(len(results) - 1, -1, -1):
                    # time.sleep(1)
                    stage += 1
                    # print(sorted_data[results[i]]["data"]["TON"])
                    ton = sorted_data[results[i]]["data"]["TON"]
                    name = sorted_data[results[i]]["account"]["name"]

                    avatar = sorted_data[results[i]]["account"]["avatar"]
                    # print(name)
                    privilege = sorted_data[results[i]]["account"]["privilege"]
                    old_players = self.ids["players_top"].children

                    widget = old_players[i]

                    widget.text = f"{stage}: {name}"
                    widget.secondary_text = f"TON: {'{0:.6f}'.format(ton)}"
                    widget.avatar.source = "dialog.png"
                    widget.name = name
                    widget.avatar.source = avatar
                    # if Account.data["account"] and Account.data["account"]["privilege"] == "Админ":
                    #     widget.bind(on_press=self.open_ban_dialog)
                    #
                    #
                    # else:
                    #     widget.bind(on_press=lambda a: print())
                    # widget.remove_widget(widget.avatar)
                    # print(widget.avatar.parent)

                    # widget.right_text.text = ""
                    if Account.data["account"] and Account.data["account"]["name"] == name:
                        widget.text = f"[b]Вы: {name}[/b]"

                    if privilege == "Админ":
                        widget.text += " - Админ"
                        widget.theme_text_color = "Custom"
                        widget.text_color = (1, .1, .1, 1)
                        self.ids["privilege"].color = (1, 0, 0, 1)
                    if privilege == "Модератор":
                        widget.text += " - Модератор"
                        widget.theme_text_color = "Custom"
                        widget.text_color = (1, .67, .2, 1)

                    if privilege == "Helper":
                        widget.text += " - Helper"
                        widget.theme_text_color = "Custom"
                        widget.text_color = (0.2, .9, .88, 1)
                    if stage == 1:
                        widget.medal.source = "gold_medal.png"
                    elif stage == 2:
                        widget.medal.source = "silver_medal.png"
                    elif stage == 3:
                        widget.medal.source = "bronze_medal.png"

                    # if name == Account.data["account"]["name"]:
                    #     # text = RightText(text="Вы")
                    #     widget.right_text.text = "Вы"


            else:
                self.ids["players_top"].clear_widgets()

                for i in range(len(results) - 1, -1, -1):
                    # time.sleep(1)
                    stage += 1
                    # print(sorted_data[results[i]]["data"]["TON"])
                    ton = sorted_data[results[i]]["data"]["TON"]
                    name = sorted_data[results[i]]["account"]["name"]

                    avatar = sorted_data[results[i]]["account"]["avatar"]
                    # print(name)
                    privilege = sorted_data[results[i]]["account"]["privilege"]
                    # print(data["data"])
                    # if Account.data["account"] and Account.data["account"]["privilege"] == "Админ":
                    line = TwoLineAvatarIconListItem(
                        text=f"{stage}: {name}",
                        # source="",
                        secondary_text=f"TON: {'{0:.6f}'.format(ton)}",

                        # font_name="main_font.ttf",
                        # font_style="H6",
                        # type=type_card,
                        on_press=self.open_info_dialog
                    )
                    line.name = name
                    # else:

                    # on_press=lambda a: print("Hello")
                    if Account.data["account"] and Account.data["account"]["name"] == name:
                        line.text = f"[b]Вы: {name}[/b]"
                    if privilege == "Админ":
                        line.text += " - Админ"
                        line.theme_text_color = "Custom"
                        line.text_color = (1, .1, .1, 1)
                        self.ids["privilege"].color = (1, 0, 0, 1)
                    if privilege == "Модератор":
                        line.text += " - Модератор"
                        line.theme_text_color = "Custom"
                        line.text_color = (1, .67, .2, 1)

                    if privilege == "Helper":
                        line.text += " - Helper"
                        line.theme_text_color = "Custom"
                        line.text_color = (0.2, .9, .88, 1)
                    medal = ImageRightWidget()

                    line.add_widget(medal)
                    line.medal = medal

                    if stage == 1:
                        line.medal.source = "gold_medal.png"
                    elif stage == 2:
                        line.medal.source = "silver_medal.png"
                    elif stage == 3:
                        line.medal.source = "bronze_medal.png"

                    # line.add_widget(text)
                    # line.right_text = text
                    # try:
                    image = ImageLeftWidget(source=avatar)
                    line.add_widget(image)

                    line.avatar = image

                    # ak.and_()

                    self.ids["players_top"].add_widget(line)
            self.ids["players_top"].opacity = 1
            self.ids["players_top"].disabled = False
            self.ids["loading_top_text"].opacity = 0

        Clock.schedule_once(lt)

    def effect(self, name, time, lvl):
        self.current_effect = {"name": name, "time": time, "lvl": lvl}
        timer(self.clear_effect, 30, "disable_tired")

    def clear_effect(self):
        Snackbar(text="Эффект бодрости снят",
                 snackbar_x="10dp",
                 snackbar_y="15dp",

                 pos_hint={"center_x": .5},
                 duration=.4).open()
        self.current_effect = {"name": None, "time": None, "lvl": None}

    def start_game(self, name, *args):
        if name == "roulette":

            b = Account.data["data"]["TON"] / 100 * self.ids['bet_value'].value
            if b >= Account.data["data"]["TON"] * .2 and b <= Account.data["data"]["TON"] and b >= 0.000100:
                self.ids['bet_value'].error = False
                r = random.randint(1, 20)

                # l = b * (-1) + self.ids['bet_value'].max
                # m = Account.data["data"]["TON"] - s
                bet = b
                Account.data["data"]["TON"] -= bet
                if r > 13 and r < 20:
                    Account.data["data"]["TON"] += bet
                    show_dialog(title="Увы!", text=f"Вам ничего не выпало! \nТы не проиграл и не выииграл")
                if r > 4 and r < 13:
                    # Account.data["data"]["TON"] +-= bet
                    show_dialog(title="Увы!", text=f"Вы проиграли {'{0:.6f}'.format(bet)} TON.")
                if r > 1 and r < 4:
                    bet *= 1.5
                    Account.data["data"]["TON"] += bet
                    show_dialog(title="Поздравляем!", text=f"Вы выиграли {'{0:.6f}'.format(bet)} TON!")
                if r == 4:
                    self.effect(name="disable_tired", time=30, lvl=2)
                    Account.data["data"]["TON"] += bet
                    show_dialog(title="Поздравляем!", text=f"Вам выдан еффект бодрости 2 уровня на 30 секунд!\n")
                if r == 16:
                    self.effect(name="disable_tired", time=30, lvl=4)
                    Account.data["data"]["TON"] += bet
                    show_dialog(title="Поздравляем!", text=f"Вам выдан еффект бодрости 4 уровня на 30 сукунд!\n")
            elif b < 0.000100:
                Snackbar(text=f'''Вы должны поставить не меньше {'{0:.6f}'.format(0.000_100)} TON''',
                         snackbar_x="10dp",
                         snackbar_y="15dp",

                         pos_hint={"center_x": .5},
                         duration=2).open()
            elif b < Account.data["data"]["TON"] * .3:
                Snackbar(text=f'''Ставка не может быть меньше {'{0:.6f}'.format(data["data"]["TON"] * .3)} TON''',
                         snackbar_x="10dp",
                         snackbar_y="15dp",

                         pos_hint={"center_x": .5},
                         duration=2).open()

            elif b > Account.data["data"]["TON"]:
                Snackbar(text=f'''Ставка не может быть больше {'{0:.6f}'.format(data["data"]["TON"])} TON''',
                         snackbar_x="10dp",
                         snackbar_y="15dp",

                         pos_hint={"center_x": .5},
                         duration=2).open()

        # Account.data["data"]["TON"] -= w

        # print('{0:.6f}'.format(data["data"]["TON"]), '{0:.7f}'.format(s / 100 * l))
        # if r < 40:
        #     Account.data["data"]["TON"] += w * 2
        #     show_dialog(title="Поздравляем!!!", text=f"Вы выиграли {'{0:.6f}'.format(w * 2)} TON")
        #
        # else:
        #     show_dialog(title="Увы!", text=f"Вы проиграли {'{0:.6f}'.format(w * 2)} TON")
        elif name == "bombs":
            b = Account.data["data"]["TON"] / 100 * self.ids['bet_find_it'].value

            if self.bombs and b >= Account.data["data"]["TON"] * .2 and b <= Account.data["data"]["TON"] and b >= 0.000100:
                # self.ids['bet_find_it'].error = False
                # self.bombs = args[0]
                # if Account.data["data"]["token"]["value"] - 1 >= 0:
                # Account.data["data"]["token"]["value"] -= 1
                from kivymd.uix.floatlayout import MDFloatLayout
                self.bombs_platform = MDFloatLayout(md_bg_color=(1, 1, 1, 1))

                self.platform = GridLayout(
                    pos_hint={"center_x": .5},
                    cols=5,
                    spacing="4sp",
                    size_hint=(.6, .6)
                )
                self.bombs_platform.add_widget(self.platform)
                self.win_label = CustomLabel(
                    text=f"Текущий выигрыш: \n0 TON",
                    font_name="main_font.ttf",
                    font_size="25sp",
                    halign="center",
                    pos_hint={"center_x": .5, "center_y": .85},
                    markup=True,

                )
                self.bombs_platform.add_widget(self.win_label)
                self.collect = MDFillRoundFlatIconButton(
                    text="Забрать",
                    font_size="25sp",
                    font_name="main_font.ttf",
                    icon="cash-100",
                    # color=(1, .1, .1, 1),
                    md_bg_color="fe5722",
                    pos_hint={"center_x": .5, "center_y": .7},
                    on_press=lambda a: self.is_won(name="bombs")
                )
                self.bombs_platform.add_widget(self.collect)
                self.ids["bombs_layout"].add_widget(self.bombs_platform)
                bet = float(self.ids["bet_find_it"].text)
                self.old_bet = bet
                Account.data["data"]["TON"] -= bet
                if self.bombs == 5:
                    self.bet = bet * .5
                if self.bombs == 10:
                    self.bet = bet * 2
                if self.bombs == 15:
                    self.bet = bet * 2.5
                if self.bombs == 24:
                    self.bet = bet * 3
                self.find_li = [[0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0],
                                ]
                bombs = 25 - self.bombs
                for i in range(25 - self.bombs):
                    if bombs > 0:
                        while 1:
                            x = random.randint(0, 4)
                            y = random.randint(0, 4)

                            if self.find_li[y][x] == 0:
                                self.find_li[y][x] = 1
                                bombs -= 1
                                break
                    # else:

                for y in range(5):
                    for x in range(5):
                        b = RoundedRectangleButton(size_hint=(.1, .1),
                                                   color="1f97f3",
                                                   # radius=[6],

                                                   pos_hint={"x": x * .1, "y": y * .1},
                                                   on_press=self.find_it)
                        # b.bind()
                        if self.find_li[y][x] == 1:
                            b.name = 1
                            # b.source="card_win.jpg"
                        else:
                            b.name = 0
                        # b.background_normal = "card_normal.jpg"

                        self.platform.add_widget(b)
            elif b < 0.000100:
                Snackbar(text=f'''Вы должны поставить не меньше {'{0:.6f}'.format(0.000100)} TON''',
                         snackbar_x="10dp",
                         snackbar_y="15dp",

                         pos_hint={"center_x": .5},
                         duration=2).open()
            elif self.bombs == None:
                Snackbar(text="Количество бомб не выбрано!",
                         snackbar_x="10dp",
                         snackbar_y="15dp",

                         pos_hint={"center_x": .5},
                         duration=.4).open()
            elif b < Account.data["data"]["TON"] * .3:
                Snackbar(text=f'''Ставка не может быть меньше {'{0:.6f}'.format(data["data"]["TON"] * .3)} TON''',
                         snackbar_x="10dp",
                         snackbar_y="15dp",

                         pos_hint={"center_x": .5},
                         duration=2).open()

            elif b > Account.data["data"]["TON"]:
                Snackbar(text=f'''Ставка не может быть больше {'{0:.6f}'.format(data["data"]["TON"])} TON''',
                         snackbar_x="10dp",
                         snackbar_y="15dp",

                         pos_hint={"center_x": .5},
                         duration=2).open()

        # Account.data["data"]["T    ON"] += self.finded_numbers * self.bet
        # if obj.name == 0:

        # print("ty")
        # if len(self.finded_numbers) >= self.bombs:
        # print(">3")

    def is_won(self, name):
        if name == "bombs":
            show_dialog(title="Поздравляем!",
                        auto_close=False,
                        text=f'Вы забрали {"{0:.6f}".format(len(self.finded_numbers) * self.bet)} TON',
                        command=lambda: self.ids["bombs_layout"].remove_widget(self.bombs_platform))
            Account.data["data"]["TON"] += len(self.finded_numbers) * self.bet
            self.finded_numbers = []

    def find_it(self, obj):
        # self.ids["find_it"].opacity = 1
        # print(obj.name)
        # if len(self.finded_numbers) < self.bombs:

        if obj.name == 1:
            self.finded_numbers.append(obj)
            # obj.source = "plate_win.png"
            self.win_label.text = f'Текущий выигрыш: \n[color=37e066][b]{"{0:.6f}".format(len(self.finded_numbers) * self.bet)} TON[/b][/color]'

            # timer(1, lambda: self.game_state("set_black_win_text"))
            obj.color = "37e066"
            obj.disabled = True
        if obj.name == 0:
            # obj.disabled = True
            self.collect.disabled = True
            for i in self.platform.children:
                i.disabled = True
                if i.name == 0:
                    i.color = "f54334"
                else:
                    i.color = "388e3c"
                if i in self.finded_numbers:
                    i.color = "37e066"
            # for i in self.finded_numbers:
            #     i.color = C("37e066")
            # obj.color = C("f54334")
            self.win_label.text = f'Текущий выигрыш: \n[color=ff0000][b]-{"{0:.6f}".format(self.old_bet)} TON[/b][/color]'
            timer(lambda: self.game_state("bombs_undo"), 3)

            self.finded_numbers = []

    def game_state(self, *args):
        if args[0] == "bombs":
            self.ids["bombs_game_start"].text = f"Сыграть в {args[1]} бомб"
            self.bombs = args[1]
            for i in self.ids["bombs_num"].children:

                if i == args[2]:

                    i.source = f"{i.name}_down.png"
                else:
                    i.source = f"{i.name}.png"
        if args[0] == "bombs_undo":
            self.ids["bombs_layout"].remove_widget(self.bombs_platform)

            self.finded_numbers = []
        # self.ids["withdraw_bombs"].opacity = 0
        if args[0] == "set_black_win_text":
            self.win_label.color = 000000
            # print(self.win_label.color)

    # def show_rewarded_ad(self, command=None):
    #     self.ads.show_rewarded_ad()
    #     self.ads.on_rewarded_video_ad_completed = self.open_chest(is_bought=False)

    # def load_video(self):
    #     self.ads.load_rewarded_ad("ca-app-pub-9371118693960899/7509498390")

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

            if name == "автомайнер":
                if not Account.data["data"]["bot"]["alow_bot"]:
                    f = FloatLayout()
                    b = MDBoxLayout(orientation="vertical")

                    b.add_widget(CustomLabel(text=f'Цена: {"{0:.6f}".format(data["data"]["bot"]["price"])} TON',
                                             halign="center",
                                             # color=(0, 0, 0, 1),
                                             font_name="main_font.ttf",
                                             font_size="25sp", ))
                    b.add_widget(CustomLabel(
                        text=f'Для автоматической добычи валюты требуется видеокарта',
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
                    b2 = MDBoxLayout(spacing="5sp")

                    b2.add_widget(
                        MDFillRoundFlatButton(text="Отмена", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                              font_name="main_font.ttf",
                                              size_hint=(.3, None), font_size="25sp",
                                              on_press=lambda a: self.close_dialog()))
                    b2.add_widget(
                        MDFillRoundFlatButton(text="Купить!", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                              font_name="main_font.ttf",
                                              size_hint=(.3, None), font_size="25sp",
                                              on_press=lambda a: self.buy(obj=obj, disabled=True)))
                    b.add_widget(b2)
                    # f.add_widget(b)

                    # b.add_widget(MDMDLabel(text="Описание: Увеличивает майнинг в x раз"))
                    # Buy_content(price=self.doubling_data["price"], boost=f'Увеличение удвоения майнинга с {self.doubling_data["price"]} TON/клик до {self.doubling_data["value"] + self.doubling_data["value"] / 100 * 30} TON/клик', description="Увеличивает майнинг в x раз"),
                    self.dialog = Popup(title=name.capitalize(), title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                                        title_align="center", title_size="30sp", content=b,
                                        size_hint=(.9, .7), background="dialog.png")
                else:
                    if not Account.data["data"]["bot"]["active"]:
                        Account.data["data"]["bot"]["active"] = True
                        obj.secondary_text = "Активен"
                    elif Account.data["data"]["bot"]["active"]:
                        Account.data["data"]["bot"]["active"] = False
                        obj.secondary_text = "Неактивен"
            elif name in store_items and store_items[name]["type"] == "video card" or store_items[name][
                "type"] == "processor":
                if name in Account.data["data"]["inventory"]:
                    f = FloatLayout()
                    b = MDBoxLayout(orientation="vertical")
                    if name in bonuse_items_names:
                        t = CustomLabel(
                            text=f'Не прокачивается!',
                            halign="center",
                            # color=(0, 0, 0, 1),
                            font_name="main_font.ttf",
                            font_size="25sp", )
                        b.add_widget(t)
                        if bonuse_items_names[name]["type_effect"] == "double_click":
                            effect = CustomLabel(
                                text=f"Еффект:\nШанс {bonuse_items_names[name]['chance']}% на двойной клик",
                                halign="center",
                                # color=(0, 0, 0, 1),
                                font_name="main_font.ttf",
                                color="ff9100",
                                font_size="25sp",
                                markup=True,
                            )
                            b.add_widget(effect)
                        # b2 = MDBoxLayout(spacing="5sp")

                        b.add_widget(MDFillRoundFlatButton(text="Закрыть", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                                           pos_hint={"center_x": .5},
                                                           on_press=lambda a: self.close_dialog(),
                                                           font_name="main_font.ttf",
                                                           size_hint=(.3, None), font_size="25sp"))
                    else:
                        self.video_card_price = CustomLabel(
                            text=f'Цена: {"{0:.7f}".format(data["data"]["inventory"][name]["price"])} TON',
                            halign="center",
                            # color=(0, 0, 0, 1),
                            font_name="main_font.ttf",
                            font_size="25sp", )
                        b.add_widget(self.video_card_price)

                        self.video_card_speed = CustomLabel(
                            text=f'Скорость: {"{0:.7f}".format(data["data"]["inventory"][name]["boost"])}[color=2dbb54] + {"{0:.7f}".format(data["data"]["inventory"][name]["boost"] * .3)} TON/сек[/color]',
                            halign="center",
                            # color=(0, 0, 0, 1),
                            font_name="main_font.ttf",
                            font_size="25sp",
                            markup=True,
                        )
                        b.add_widget(self.video_card_speed)

                        # f.add_widget(b)
                        b2 = MDBoxLayout(spacing="5sp")

                        b2.add_widget(
                            MDFillRoundFlatButton(text="Отмена", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                                  font_name="main_font.ttf",
                                                  size_hint=(.3, None), font_size="25sp",
                                                  on_press=lambda a: self.close_dialog()))
                        b2.add_widget(
                            MDFillRoundFlatButton(text="Прокачать!", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                                  font_name="main_font.ttf",
                                                  size_hint=(.3, None), font_size="25sp",
                                                  on_press=lambda a: self.boosting(obj=obj)))
                        b.add_widget(b2)
                    # f.add_widget(b)

                    # b.add_widget(MDMDLabel(text="Описание: Увеличивает майнинг в x раз"))
                    # Buy_content(price=self.doubling_data["price"], boost=f'Увеличение удвоения майнинга с {self.doubling_data["price"]} TON/клик до {self.doubling_data["value"] + self.doubling_data["value"] / 100 * 30} TON/клик', description="Увеличивает майнинг в x раз"),
                    self.dialog = Popup(title=name, title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                                        title_align="center", title_size="30sp", content=b,
                                        size_hint=(.9, .7), background="dialog.png")
                elif name not in bonuse_items_names:
                    f = FloatLayout()
                    b = MDBoxLayout(orientation="vertical")

                    b.add_widget(CustomLabel(text=f'Цена: {"{0:.6f}".format(store_items[name]["price"])}',
                                             halign="center",
                                             # color=(0, 0, 0, 1),
                                             font_name="main_font.ttf",
                                             font_size="25sp", ))
                    b.add_widget(CustomLabel(
                        text=f'Скорость: {"{0:.6f}".format(store_items[name]["boost"])} TON/сек',
                        halign="center",
                        # color=(0, 0, 0, 1),
                        font_name="main_font.ttf",
                        font_size="25sp", ))

                    # f.add_widget(b)
                    b2 = MDBoxLayout(spacing="5sp")

                    b2.add_widget(
                        MDFillRoundFlatButton(text="Отмена", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                              font_name="main_font.ttf",
                                              size_hint=(.3, None), font_size="25sp",
                                              on_press=lambda a: self.close_dialog()))
                    b2.add_widget(
                        MDFillRoundFlatButton(text="Купить!", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                              font_name="main_font.ttf",
                                              size_hint=(.3, None), font_size="25sp",
                                              on_press=lambda a: self.buy(obj=obj, disabled=True)))
                    b.add_widget(b2)
                    # f.add_widget(b)

                    # b.add_widget(MDMDLabel(text="Описание: Увеличивает майнинг в x раз"))
                    # Buy_content(price=self.doubling_data["price"], boost=f'Увеличение удвоения майнинга с {self.doubling_data["price"]} TON/клик до {self.doubling_data["value"] + self.doubling_data["value"] / 100 * 30} TON/клик', description="Увеличивает майнинг в x раз"),
                    self.dialog = Popup(title=name, title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                                        title_align="center", title_size="30sp", content=b,
                                        size_hint=(.9, .7), background="dialog.png")
            elif name in store_items and store_items[name]["type"] == "mouse":

                if name in Account.data["data"]["inventory"]:
                    f = FloatLayout()
                    b = MDBoxLayout(orientation="vertical")
                    if name in bonuse_items_names:
                        effect = CustomLabel(
                            text=f"Не прокачивается!",
                            halign="center",
                            # color=(0, 0, 0, 1),
                            # color="ff9100",
                            font_name="main_font.ttf",
                            font_size="25sp",
                            markup=True,
                        )
                        b.add_widget(effect)
                        if bonuse_items_names[name]["type_effect"] == "double_click":
                            effect = CustomLabel(
                                text=f"Еффект:\nШанс {bonuse_items_names[name]['chance']}% на двойной клик",
                                halign="center",
                                # color=(0, 0, 0, 1),
                                color="ff9100",
                                font_name="main_font.ttf",
                                font_size="25sp",
                                markup=True,
                            )
                            b.add_widget(effect)
                        if bonuse_items_names[name]["type_effect"] == "disable_tired":
                            effect = CustomLabel(
                                text=f"Еффект:\nШанс {bonuse_items_names[name]['chance']}% вернуть 5% энергии",
                                halign="center",
                                # color=(0, 0, 0, 1),
                                color="ff9100",
                                font_name="main_font.ttf",
                                font_size="25sp",
                                markup=True,
                            )
                            b.add_widget(effect)
                        b.add_widget(MDFillRoundFlatButton(text="Закрыть", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                                           pos_hint={"center_x": .5},
                                                           on_press=lambda a: self.close_dialog(),
                                                           font_name="main_font.ttf",
                                                           size_hint=(.3, None), font_size="25sp"))
                    else:
                        self.mouse_price = CustomLabel(
                            text=f'Цена: {"{0:.6f}".format(data["data"]["inventory"][name]["price"])}',
                            halign="center",
                            # color=(0, 0, 0, 1),
                            font_name="main_font.ttf",
                            font_size="25sp", )
                        b.add_widget(self.mouse_price)
                        self.mouse_speed = CustomLabel(
                            text=f'Скорость: {"{0:.7f}".format(data["data"]["inventory"][name]["boost"])}[color=2dbb54] + {"{0:.7f}".format(data["data"]["inventory"][name]["boost"] * .3)} TON/клик[/color]',
                            halign="center",
                            # color=(0, 0, 0, 1),
                            font_name="main_font.ttf",
                            font_size="25sp",
                            markup=True,
                        )

                        b.add_widget(self.mouse_speed)
                        self.mouse_tired = CustomLabel(
                            text=f'Расход энергиии: {round(data["data"]["inventory"][data["data"]["mouse"]]["tired"], 1)}%[color=ff0000] - 0.1%[/color]',
                            halign="center",
                            # color=(0, 0, 0, 1),
                            font_name="main_font.ttf",
                            font_size="25sp",
                            markup=True,
                        )
                        b.add_widget(self.mouse_tired)

                        # f.add_widget(b)
                        b2 = MDBoxLayout(spacing="5sp")

                        b2.add_widget(MDFillRoundFlatButton(text="Отмена", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                                            on_press=lambda a: self.close_dialog(),
                                                            font_name="main_font.ttf",
                                                            size_hint=(.3, None), font_size="25sp"))
                        b2.add_widget(MDFillRoundFlatButton(text="Прокачать!", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                                            on_press=lambda a: self.boosting(obj=obj),
                                                            font_name="main_font.ttf",
                                                            size_hint=(.3, None), font_size="25sp"))
                        b.add_widget(b2)
                    # f.add_widget(b)

                    # b.add_widget(MDLabel(text="Описание: Увеличивает майнинг в x раз"))
                    # Buy_content(price=self.doubling_data["price"], boost=f'Увеличение удвоения майнинга с {self.doubling_data["price"]} TON/клик до {self.doubling_data["value"] + self.doubling_data["value"] / 100 * 30} TON/клик', description="Увеличивает майнинг в x раз"),
                    self.dialog = Popup(title=name, title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                                        title_align="center", title_size="30sp", content=b,
                                        size_hint=(.9, .7), background="dialog.png")
                elif name not in bonuse_items_names:
                    f = FloatLayout()
                    b = MDBoxLayout(orientation="vertical")

                    b.add_widget(CustomLabel(text=f'Цена: {"{0:.6f}".format(store_items[name]["price"])}',
                                             halign="center",
                                             # color=(0, 0, 0, 1),
                                             font_name="main_font.ttf",
                                             font_size="25sp", ))
                    b.add_widget(CustomLabel(
                        text=f'Скорость: {"{0:.6f}".format(store_items[name]["boost"])} TON/клик',
                        halign="center",
                        # color=(0, 0, 0, 1),
                        font_name="main_font.ttf",
                        font_size="25sp", ))
                    b.add_widget(CustomLabel(
                        text=f'Расход энергиии: {round(data["data"]["inventory"][data["data"]["mouse"]]["tired"], 1)}%',
                        halign="center",
                        # color=(0, 0, 0, 1),
                        font_name="main_font.ttf",
                        font_size="25sp", ))
                    # f.add_widget(b)
                    b2 = MDBoxLayout(spacing="5sp")

                    b2.add_widget(MDFillRoundFlatButton(text="Отмена", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                                        on_press=lambda a: self.close_dialog(),
                                                        font_name="main_font.ttf",
                                                        size_hint=(.3, None), font_size="25sp"))
                    b2.add_widget(MDFillRoundFlatButton(text="Купить!", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                                        on_press=lambda a: self.buy(obj=obj, disabled=True),
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
                Account.data["data"]["chest"].setdefault("last_opened", datetime.datetime.now().isoformat()))
            if now - last_opened > datetime.timedelta(hours=24):

                b2 = MDBoxLayout(orientation="vertical",
                                 # padding=20,
                                 # size_hint_y=.8,
                                 pos_hint={"center_y": .5},
                                 spacing=30)
                b2.add_widget(CustomLabel(text=f'У вас есть 1 бесплатный сундук',
                                          halign="center",
                                          pos_hint={"center_x": .5},
                                          font_name="main_font.ttf",
                                          font_size="25sp",

                                          # theme_text_color="Custom",
                                          # color=(0, 0, 0, 1),
                                          )
                              )
                b1 = MDBoxLayout(size_hint_y=.3, spacing="2sp")
                b1.add_widget(
                    MDFillRoundFlatButton(text="Закрыть", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                          pos_hint={"center_x": .5},
                                          font_name="main_font.ttf",
                                          font_size="25sp",
                                          size_hint=(.3, None),
                                          on_press=lambda a: self.chest_dialog.dismiss()))
                b1.add_widget(
                    MDFillRoundFlatButton(text="Открыть!", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                                          pos_hint={"center_x": .5},
                                          font_name="main_font.ttf",
                                          font_size="25sp",
                                          size_hint=(.3, None),
                                          on_press=lambda a: self.open_chest(is_bought=False)))
                b2.add_widget(b1)
                self.chest_dialog = Popup(title="Открыть сундук?", title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                                          title_align="center", title_size="30sp", content=b2,
                                          size_hint=(.9, .5), background="dialog.png")
                b1.bind(on_release=lambda a: self.chest_dialog.dismiss())

                self.chest_dialog.open()
            else:
                t = last_opened + datetime.timedelta(hours=12) - now
                hours = t.seconds // 3600
                minutes = t.seconds % 3600 // 60
                # m
                houres_text = "час"
                minutes_text = "минуту"
                print(int(str(hours)[-1]) >= 5, int(str(hours)[-1]) == 0, hours > 5, hours < 21)
                if hours > 5:
                    houres_text = "часов"
                elif hours > 1:
                    houres_text = "часа"
                if int(str(minutes)[-1]) >= 5 or int(str(minutes)[-1]) == 0 or minutes < 21 and minutes > 5:
                    minutes_text = "минут"
                elif int(str(minutes)[-1]) < 5 and int(str(minutes)[-1]) > 1 or minutes < 0:
                    minutes_text = "минуты"

                show_dialog(title="Открыть сундук",
                            text=f"Следуюший сундук через {hours} {houres_text} {minutes} {minutes_text}.")
                # b2 = BoxLayout(orientation="vertical", spacing="5sp")
                # b2.add_widget(CustomLabel(text=f'УСледу',
                #                           halign="center",
                #                           pos_hint={"center_x": .5},
                #                           font_name="main_font.ttf",
                #                           font_size="25sp",
                #
                #                           # theme_text_color="Custom",
                #                           # color=(0, 0, 0, 1),
                #                           )
                #               )
                # b2.add_widget(
                #     MDFillRoundFlatButton(text="Открыть!", md_bg_color=(0.1, 0.6, 0.9, 1.0),
                #                           pos_hint={"center_x": .5},
                #                           font_name="main_font.ttf",
                #                           font_size="25sp",
                #                           on_press=lambda a: self.open_chest(is_bought=False)))
                # b = MDFlatButton(
                #     text="Отмена",
                #     font_size="20sp",
                #     font_name="main_font.ttf",
                #     pos_hint={"right": 1, "center_y": .1},
                # )
                # b2.add_widget(b)
                # self.chest_dialog = Popup(title="Открыть сундук?", title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                #                           title_align="center", title_size="30sp",
                #                           content=b2,
                #                           size_hint=(.9, .5), background="dialog.png")
                # self.chest_dialog.content = Chest_content(dialog=self.chest_dialog)
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
            # self.chest_dialog.open()

    def boosting(self, obj):
        name = obj.name

        video = Account.data["data"]["bot"]["video card"]
        index = Account.data["data"]["inventory"][name]["index"]
        price = Account.data["data"]["inventory"][name]["price"]
        type_item = Account.data["data"]["inventory"][name]["type"]

        # if index < store_items[name]["index"]:
        if Account.data["data"]["TON"] - price >= 0:
            # print(type_item)
            Account.data["data"]["TON"] -= price

            if type_item == "mouse":
                Account.data["data"]["inventory"][name]["price"] += Account.data["data"]["inventory"][name]["price"] * 100
                Account.data["data"]["inventory"][name]["boost"] += Account.data["data"]["inventory"][name]["boost"] * .2
                Account.data["data"]["inventory"][name]["tired"] -= Account.data["data"]["inventory"][name]["tired"] * .1
                Account.data["data"]["mouse"] = name
                self.mouse_price.text = f'Цена: {"{0:.6f}".format(data["data"]["inventory"][name]["price"])}'
                self.mouse_tired.text = f'Расход энергиии: {round(data["data"]["inventory"][data["data"]["mouse"]]["tired"], 1)}%[color=ff0000] - 0.1%[/color]'
                self.mouse_speed.text = f'Скорость: {"{0:.7f}".format(data["data"]["inventory"][name]["boost"])}[color=2dbb54] + {"{0:.7f}".format(data["data"]["inventory"][name]["boost"] * .3)} TON/клик[/color]'
            elif type_item == "video card":
                # print("23456")
                Account.data["data"]["inventory"][name]["price"] += Account.data["data"]["inventory"][name]["price"] * 100
                Account.data["data"]["inventory"][name]["boost"] += Account.data["data"]["inventory"][name]["boost"] * .2

                Account.data["data"]["bot"]["video card"] = name
                self.video_card_price.text = f'Цена: {"{0:.6f}".format(data["data"]["inventory"][name]["price"])} TON'
                self.video_card_speed.text = f'Скорость: {"{0:.7f}".format(data["data"]["inventory"][name]["boost"])}[color=2dbb54] + {"{0:.7f}".format(data["data"]["inventory"][name]["boost"] * .3)} TON/сек[/color]'
            # Account.data["data"]["inventory"][name]["price"] += Account.data["data"]["inventory"][name]["price"] * 300
            # obj.secondary_text = f'Цена: {"{0:.6f}".format(data["data"]["inventory"][name]["price"])} TON'
            obj.secondary_text = f'''Цена: {'{0:.6f}'.format(data["data"]["inventory"][name]["price"])} TON'''
        elif Account.data["data"]["TON"] - price <= 0:
            Snackbar(text="У вас не хватает на это TON!",
                     snackbar_x="10dp",
                     snackbar_y="15dp",

                     pos_hint={"center_x": .5},
                     duration=.4).open()

    def buy(self, obj, disabled=False):

        name = obj.name
        self.close_dialog()
        # obj.disabled = disabled
        # obj.children.disabled = False
        if name in store_items:
            video = Account.data["data"]["bot"]["video card"]
            index = store_items[video]["index"]
            price = store_items[name]["price"]
            type_item = store_items[name]["type"]

            if Account.data["data"]["TON"] - price >= 0 and video != name:

                Account.data["data"]["TON"] -= price
                if type_item == "mouse":
                    # print(self.ids["bot_shop"].ids)
                    self.ids["mining_shop"].ids[f"choose_current_{name}"].opacity = 1
                    self.ids["mining_shop"].ids[f"choose_current_{name}"].active = True
                    self.ids["mining_shop"].ids[f"choose_current_{name}"].disabled = False
                    Snackbar(text=f"Выбрана мышка {name}",
                             snackbar_x="10dp",
                             snackbar_y="15dp",

                             pos_hint={"center_x": .5},
                             duration=.1).open()
                    # for key, obj in self.ids["bot_shop"].ids.items():
                    #     if obj.name not in Account.data['data']["inventory"]:
                    #
                    #         self.ids["bot_shop"].ids[key].opacity = 0
                    #     else:
                    #         self.ids["bot_shop"].ids[key].opacity = 1
                    # for key, obj in self.ids["mining_shop"].ids.items():
                    #     if obj.name not in Account.data['data']["inventory"]:
                    #         self.ids["mining_shop"].ids[key].opacity = 0
                    #     else:
                    #         self.ids["mining_shop"].ids[key].opacity = 1
                    Account.data["data"]["mouse"] = name
                elif type_item == "video card":
                    self.ids["bot_shop"].ids[f"choose_current_{name}"].opacity = 1
                    self.ids["bot_shop"].ids[f"choose_current_{name}"].active = True
                    self.ids["bot_shop"].ids[f"choose_current_{name}"].disabled = False
                    Account.data["data"]["bot"]["video card"] = name
                    Snackbar(text=f"Выбрана видеокарта {name}",
                             snackbar_x="10dp",
                             snackbar_y="15dp",

                             pos_hint={"center_x": .5},
                             duration=.1).open()
                Account.data["data"]["inventory"][name] = store_items[name]
                Account.data["data"]["inventory"][name]["price"] += Account.data["data"]["inventory"][name]["price"] * 30


            elif Account.data["data"]["TON"] - price <= 0:
                Snackbar(text="У вас не хватает на это TON!",
                         snackbar_x="10dp",
                         snackbar_y="15dp",

                         pos_hint={"center_x": .5},
                         duration=.4).open()

        # elif name in self.mouses:видеокарта
        #     button = Account.data["data"]["mouse"]
        #     index = self.mouses[button]["index"]
        #     price = self.mouses[name]["price"]
        #     if index < self.mouses[name]["index"]:
        #         if Account.data["data"]["TON"] - price >= 0 and button != name:
        #
        #             Account.data["data"]["TON"] -= price
        #             Account.data["data"]["mouse"] = name
        #         elif Account.data["data"]["TON"] - price <= 0:
        #             Snackbar(text="У вас не хватает на это валюты!",duration=.2)
        #     elif index > self.mouses[name]["index"]:
        #         Snackbar(text="Эта мышь хуже, чем у вас есть!",duration=.2)
        #     elif index == self.mouses[name]["index"]:
        #         Snackbar(text="У вас уже усть эта мышь!",duration=.2)
        elif name == "token":
            if Account.data["data"]["TON"] - Account.data["data"]["token"]["price"] >= 0:
                Account.data["data"]["TON"] -= Account.data["data"]["token"]["price"]
                # Account.data["data"]["token"]["price"] += Account.data["data"]["token"]["price"] / 100 * 20
                Account.data["data"]["token"]["value"] += 1

            else:
                # self.dialog.dismiss()f
                Snackbar(text="У вас не хватает на это TON!",
                         snackbar_x="10dp",
                         snackbar_y="15dp",

                         pos_hint={"center_x": .5},
                         duration=.4).open()

        elif name == "chest":
            # self.ads.show_rewarded_ad()
            if Account.data["data"]["TON"] - Account.data["data"]["chest"]["price"] >= 0:

                # Account.data["data"]["chest"]["price"] += Account.data["data"]["chest"]["price"] / 100 * 20

                # else:
                self.open_chest(is_bought=True)

            else:
                # self.dialog.dismiss()
                Snackbar(text="У вас не хватает на это TON!",
                         snackbar_x="10dp",
                         snackbar_y="15dp",

                         pos_hint={"center_x": .5},
                         duration=.4).open()

        elif name == "удвоение майнинга":
            if Account.data["data"]["TON"] - self.doubling_data["price"] >= 0:
                self.doubling_data["value"] += self.doubling_data["value"] / 100 * 50

                Account.data["data"]["TON"] -= self.doubling_data["price"]
                self.doubling_data["price"] += self.doubling_data["price"] / 100 * 50

            else:
                Snackbar(text="У вас не хватает на это TON!",
                         snackbar_x="10dp",
                         snackbar_y="15dp",

                         pos_hint={"center_x": .5},
                         duration=.4).open()
        elif name == "суммирование майнинга":
            if Account.data["data"]["TON"] - self.summation_data["price"] >= 0:
                Account.data["data"]["TON"] -= self.summation_data["price"]

                self.summation_data["value"] += 0.000001

                self.summation_data["price"] += 0.000001 * 100
            else:
                Snackbar(text="У вас не хватает на это TON!",
                         snackbar_x="10dp",
                         snackbar_y="15dp",

                         pos_hint={"center_x": .5},
                         duration=.4).open()
        elif name == "прокачка майнинга бота":
            if Account.data["data"]["TON"] - Account.data["data"]["bot"]["summation_price"] >= 0:
                Account.data["data"]["TON"] -= Account.data["data"]["bot"]["summation_price"]

                Account.data["data"]["bot"]["summation_num"] += 0.000001

                Account.data["data"]["bot"]["summation_price"] += 0.000001 * 100
            else:
                Snackbar(text="У вас не хватает на это TON!",
                         snackbar_x="10dp",
                         snackbar_y="15dp",

                         pos_hint={"center_x": .5},
                         duration=.4).open()
        elif name == "автомайнер":
            if Account.data["data"]["TON"] - Account.data["data"]["bot"]["price"] >= 0:
                Account.data["data"]["TON"] -= Account.data["data"]["bot"]["price"]
                Account.data["data"]["bot"]["alow_bot"] = True
                obj.secondary_text = "Активен"



            else:
                Snackbar(text="У вас не хватает на это TON!",
                         snackbar_x="10dp",
                         snackbar_y="15dp",

                         pos_hint={"center_x": .5},
                         duration=.4).open()
        # self.ui_update()

    def show_value(self, obj, name):
        b = obj.value

        # m = Account.data["data"]["TON"] - s

        w = Account.data["data"]["TON"] / 100 * b
        self.ids[name].text = f"Ваша ставка: {'{0:.6f}'.format(w)} TON"

    def show_info(self):
        if Account.data["data"]["bot"]["active"]:
            alow_bot = "Активен"
        else:
            alow_bot = "Неактивен"
        if not Account.data["data"]["bot"]["active"]:
            alow_bot = "Не куплен"
        show_dialog(title="Информация", text=f'''
Клик: {'{0:.6f}'.format(data["data"]["inventory"][data["data"]["mouse"]]["boost"])} TON
Расход энергиии: {round(data["data"]["inventory"][data["data"]["mouse"]]["tired"], 1)}%
Мышка: {data["data"]["mouse"]}

Автомайнер: {alow_bot}
Текущая видеокарта: {data["data"]["bot"]["video card"]}
Майнинг автомайнера: {'{0:.6f}'.format(data["data"]["inventory"][data["data"]["bot"]["video card"]]["boost"])} TON в секунду
''')

    # Жетоны: {data["data"]["token"]["value"]}
    def show_alert_dialog(self, title, text, command=lambda: print("Hello!")):
        # lambda
        self.dialog = None
        if not self.dialog:
            b = MDBoxLayout(
                orientation="vertical",
                # padding=20,
                size_hint_y=.8,
                pos_hint={"center_y": .5},
                spacing=30
            )
            b.add_widget(
                CustomLabel(text=text,
                            halign="center",
                            font_name="main_font.ttf",
                            font_size="20sp",

                            # theme_text_color="Custom",
                            # color=(0, 0, 0, 1),
                            )
            )
            c2 = MDFillRoundFlatButton(
                text="Ок",
                font_size="25sp",
                font_name="main_font.ttf",
                # halign="center",
                pos_hint={"center_x": .5},
                size_hint=(.3, None),

            )
            b.add_widget(c2)
            # b.add_widget(b2)
            self.dialog = Popup(title=title, title_color=(0, 0, 0, 1), separator_height="4dp",
                                title_font="main_font.ttf",
                                title_align="center", title_size="30sp", content=b,
                                size_hint=(.9, .7), background="dialog.png")
            c2.bind(on_press=lambda a: [self.dialog.dismiss(), command()])

        self.dialog.open()

    def close_dialog(self):
        try:
            self.dialog.dismiss()
        except:
            pass
        self.connect_error = False

    def version_control_dialog(self, dt):

        b = MDBoxLayout(
            orientation="vertical",
            # padding=20,
            size_hint_y=.8,
            pos_hint={"center_y": .5},
            spacing=30
        )
        b.add_widget(
            CustomLabel(text="Доступна новая версия TON кликер.\nЗагрузите её сейчас.",
                        halign="center",
                        font_name="main_font.ttf",
                        font_size="30sp",

                        # theme_text_color="Custom",
                        # color=(0, 0, 0, 1),
                        )
        )
        c2 = MDFillRoundFlatButton(
            text="Обновить",
            font_size="25sp",
            font_name="main_font.ttf",
            # halign="center",
            pos_hint={"center_x": .5},
            size_hint=(.4, None),
            on_press=lambda a: webbrowser.open(
                "https://play.google.com/store/apps/details?id=org.tonclicker.tonclicker"),

        )
        b.add_widget(c2)
        version_control = Popup(title="Обновление", title_color=(0, 0, 0, 1), auto_dismiss=False,
                                separator_height="4dp",

                                title_font="main_font.ttf",
                                title_align="center", title_size="30sp", content=b,
                                size_hint=(.9, .5))
        version_control.background = "dialog.png"
        # self.dialog = MDDialog(
        #     text="Доступна новая версия TON кликер.\nЗагрузите её сейчас.",
        #     radius=[20, 7, 20, 7],
        #     auto_dismiss=False)
        version_control.open()

    def update_data(self):
        # print(data["data"])
        global offline, data, version
        # print(self.cur_nav)
        # print(data["account"]["login"])
        # print('{0:.6f}'.format(data["data"]["TON"])
        # )

        with open("data.pickle", "wb") as f:
            pickle.dump({"account": Account.data["account"], "data": Account.data["data"]}, f)

            # print(p)
        try:
            p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
            if p and p < max_ping:

                # self.ids["wifi_error"].opacity = 0
                ref = db.reference(f"/version")
                if ref.get() != version:
                    # print(ref.get())
                    # dialog = None
                    # if not dialog:
                    Clock.schedule_once(self.version_control_dialog)
                    version = ref.get()
                else:
                    if Account.data["account"]:

                        # ref = db.reference(f"/players/{data['account']['name']}/data/TON")
                        # ton = ref.get()
                        # print('{0:.6f}'.format(ton))

                        ref = db.reference(f"/ban/{data['account']['name']}/cause")
                        ban = ref.get()
                        if ban is not None:
                            # print(ref.get()["cause"])
                            Clock.schedule_once(lambda a: show_dialog(title="Вы забанены!",
                                                                      text=f"Бан выдан по причине: {ban}\nВаш аккаунт был удалён.",
                                                                      auto_close=False))
                            name = Account.data["account"]["name"]
                            # self.ids[cur_nav].set_state("close")
                            self.sign_out()
                            db.reference(f"/players/{name}/").delete()
                            db.reference(f"/ban/{name}/").delete()
                        ref = db.reference(f"/new_privileges/{data['account']['name']}")
                        priv = ref.get()

                        # elif ton > Account.data["data"]["TON"]:

                        if priv != None:
                            Account.data["account"]["privilege"] = priv
                            if Account.data["account"]["privilege"] == "Админ":
                                color = (1, 0, 0, 1)
                            elif Account.data["account"]["privilege"] == "Модератор":
                                color = (1, .67, .2, 1)
                            elif Account.data["account"]["privilege"] == "Helper":
                                color = (0.2, .9, .88, 1)
                            else:
                                color = (0, 0, 0, 1)
                            print(color)
                            Clock.schedule_once(
                                lambda a: show_dialog(title="Внимание!",
                                                      text=f"Ваша привилегия теперь [color={get_hex_from_color(color)}]{priv}[/color]."))
                            if plyer.utils.platform == "win":
                                Clock.schedule_once(lambda a: self.show_notify(title="Внимание!",
                                                                               message=f"Ваша привилегия теперь {priv}!",
                                                                               app_icon="chest_normal.ico"))
                            else:
                                Clock.schedule_once(lambda a: self.show_notify(title="Внимание!",
                                                                               message=f"Ваша привилегия теперь {priv}!",
                                                                               app_icon="blue.png"))
                            ref.delete()
                        ref = db.reference(f"/transfers/{data['account']['name']}")
                        # ref.set(data)
                        transfer_ton_list = ref.get()
                        if transfer_ton_list:
                            for key, transfer in transfer_ton_list.items():
                                # ref = db.reference(f"/transfers/{data['account']['name']}/{i}")
                                # ref.set(data)
                                name = transfer["name"]
                                ton = transfer["TON"]
                                # transfer_ton = ref.get()
                                Clock.schedule_once(lambda a: show_dialog(title="Внимание!",
                                                                          text=f'Игрок {name} перевёл вам {"{0:.6f}".format(ton)} TON.'))
                                Account.data["data"]["TON"] += ton
                                ref = db.reference(f"/transfers/{data['account']['name']}/{key}")
                                # print(key)
                                ref.delete()
                        db.reference(f"/players/{data['account']['name']}").set(data)
        #                     ref = db.reference(f"/players/{data['account']['name']}/account/ban/is_banned")
        #
        #                     if ref.get() == "True":
        #                         Account.data = no_data.copy()
        #                         self.game.show_alert_dialog(title="Вы забанены!", text=f'''
        # Вы забанены по пречине: {ref.get("cause")}.
        # Обратитесь за помошью в дискорд сервер.
        # Приятной игры!
        #                                         ''')

        # print(2222)

        # print(ref.get())

        except:
            pass

    def transfer_ton(self):
        b = MDBoxLayout(
            orientation="vertical",
            # padding=20,
            size_hint_y=.8,
            pos_hint={"center_y": .5},
            spacing=30
        )
        name = MDTextField(
            hint_text="Ник игрока",
            font_name="main_font.ttf",
            # icon_right="account",
            font_size="20sp",
            pos_hint={"center_x": .5},
            # on_focus=self.seach_player(),
            # color_active=[1, 1, 1, 1],
            helper_text="Нет такого игрока! Или вы им являетесь!",
            helper_text_mode="on_error"
        )
        b.add_widget(name)
        ton = MDTextField(
            hint_text="Сумма",
            font_name="main_font.ttf",
            # icon_right="account",
            font_size="20sp",
            pos_hint={"center_x": .5},
            # on_focus=self.seach_player(),
            # color_active=[1, 1, 1, 1],
            helper_text="Сумма не корректна!",
            helper_text_mode="on_error"
        )
        b.add_widget(ton)
        b2 = MDBoxLayout(
            # orientation="vertical",
            # size_hint_y=.5,
            # md_bg_color=(1,0,0,1),
            # padding=20,
            spacing="2sp"
        )
        c2 = MDFillRoundFlatButton(
            text="Отмена",
            font_size="20sp",
            font_name="main_font.ttf",
            size_hint=(.3, None),
        )
        b2.add_widget(c2)
        c = MDFillRoundFlatButton(
            text="Перевести",
            font_size="20sp",
            font_name="main_font.ttf",
            size_hint=(.3, None),
            on_release=lambda a: self.transfer(name=name, ton=ton)
        )
        b2.add_widget(c)

        b.add_widget(b2)
        self.pay_dialog = Popup(title="Перевод", title_color=(0, 0, 0, 1), content=b, title_font="main_font.ttf",
                                title_align="center", title_size="30sp",
                                size_hint=(.9, .7), background="dialog.png")
        c2.bind(on_press=lambda a: self.pay_dialog.dismiss())
        self.pay_dialog.open()

    def transfer(self, name, ton):
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
        # print(p)
        try:
            if p and p < max_ping:
                ton.error = False
                name.error = False

                ref = db.reference(f"/players/{name.text}")
                g = ref.get()
                try:
                    if Account.data["data"]["TON"] - float(ton.text) >= 0 and float(ton.text) != 0:
                        if g and name.text != Account.data["account"]["name"]:
                            Account.data["data"]["TON"] -= float(ton.text)
                            ref = db.reference(f"/transfers/{name.text}")
                            # g = 0
                            # g +=
                            ref.push({"name": Account.data["account"]["name"], "TON": float(ton.text)})

                            b = MDBoxLayout(
                                orientation="vertical",
                                # padding=20,
                                size_hint_y=.8,
                                pos_hint={"center_y": .5},
                                spacing=30
                            )
                            b.add_widget(
                                MDIconButton(icon="check-circle", pos_hint={"center_x": .5}, user_font_size="50sp"))
                            b.add_widget(
                                CustomLabel(text=f'Игроку {name.text} было перечислено {ton.text} TON',
                                            halign="center",
                                            font_name="main_font.ttf",
                                            font_size="25sp",

                                            # theme_text_color="Custom",
                                            # color=(0, 0, 0, 1),
                                            )
                            )
                            c2 = MDFillRoundFlatButton(
                                text="Закрыть",
                                font_size="20sp",
                                font_name="main_font.ttf",
                                # halign="center",
                                pos_hint={"center_x": .5},
                                size_hint=(.3, None),
                                on_press=lambda a: self.pay_dialog.dismiss(),
                            )
                            b.add_widget(c2)
                            self.pay_dialog.content = b
                            # self.pay_dialog.dismiss()
                        else:
                            Snackbar(text=f"Такого игрока не существует!",
                                     snackbar_x="10dp",
                                     snackbar_y="15dp",

                                     pos_hint={"center_x": .5},
                                     duration=.5).open()
                    else:
                        Snackbar(text=f"Сумма не корректна!",
                                 snackbar_x="10dp",
                                 snackbar_y="15dp",

                                 pos_hint={"center_x": .5},
                                 duration=.5).open()

                except ValueError:
                    Snackbar(text=f"Сумма не корректна!",
                             snackbar_x="10dp",
                             snackbar_y="15dp",

                             pos_hint={"center_x": .5},
                             duration=.5).open()
            else:
                show_dialog(title="Ощибка!", text='''
Ошибка подключения!
Повторите попытку!
                ''')
        except:
            # else:
            show_dialog(title="Ощибка!", text='''
Ошибка подключения!
Повторите попытку!
                            ''')

    def on_tap(self):
        # print('{0:.6f}'.format(data["data"]["TON"]))
        mouse = Account.data["data"]["mouse"]
        r = random.randint(1, 100)
        if Account.data["data"]["tired_num"] - Account.data["data"]["inventory"][mouse]["tired"] >= 0:
            if self.current_effect["name"] == "disable_tired":
                Account.data["data"]["tired_num"] -= self.current_effect["lvl"] / self.current_effect["lvl"] ** 3
            if mouse in bonuse_items_names and bonuse_items_names[mouse][
                "type_effect"] == "disable_tired" and random.randint(1, 100) <= bonuse_items_names[mouse]["chance"]:
                Account.data["data"]["tired_num"] += 5

            else:
                Account.data["data"]["tired_num"] -= Account.data["data"]["inventory"][mouse]["tired"]

            if mouse in bonuse_items_names and bonuse_items_names[mouse][
                "type_effect"] == "double_click" and random.randint(1, 100) <= bonuse_items_names[mouse]["chance"]:
                Account.data["data"]["TON"] += Account.data["data"]["inventory"][mouse]["boost"] * 2
                # print("double")
            else:
                Account.data["data"]["TON"] += Account.data["data"]["inventory"][mouse]["boost"]


        else:
            old_color_icon = (1, .8, 0, 1)
            # if self.ids["tired_icon"].color != (1, 0, 0, 1):

            self.ids["tired_icon"].color = (1, 0, 0, 1)
            self.ids["tired_num"].color = (1, 0, 0, 1)
            self.ads.show_rewarded_ad()

            timer(self.start_animation, .9, "tired_color")

        # Account.data["data"]["is_tired"] = True
        # print(App.get_running_app().root.ids['hi'])

    def start_animation(self):
        self.ids["tired_icon"].color = "ffad30"

        self.ids["tired_num"].color = "ffad30"

    def set_color(self, obj, color):
        obj.color = color

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
            font_name="main_font.ttf",
            font_size="20sp",
            on_release=lambda a: self.rasban()
        )
        self.dialog = Popup(title="Разбанить", title_color=(0, 0, 0, 1), content=b, title_font="main_font.ttf",
                            title_align="center", title_size="30sp",
                            size_hint=(.9, .7), background="dialog_reg.png")

    def send_ban(self, obj, name=None, cause=None):
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
        # print(p)
        try:
            if p and p < max_ping:

                ref = db.reference(f"/players/{name}")
                g = ref.get()
                # try:
                print(name)
                string_check = re.match('''[#$. /?]''', name)

                if name and cause and string_check == None and g:

                    ref = db.reference(f"/ban/{name}")
                    # g = 0
                    # g +=
                    ref.set({"cause": cause})
                    obj.dismiss()
                    Snackbar(text=f"Игрок {name} был успешно забанен!",
                             snackbar_x="10dp",
                             snackbar_y="15dp",

                             pos_hint={"center_x": .5},
                             duration=.5).open()
                elif not g:
                    Snackbar(text=f"Такого игрока не существует!",
                             snackbar_x="10dp",
                             snackbar_y="15dp",

                             pos_hint={"center_x": .5},
                             duration=.5).open()
                else:

                    show_dialog('''
Все поля должны быть заполнены!
И не должны содержать специальные симбволы пробела и #$./?
                ''')
            else:
                show_dialog(title="Ошибка!", text='''
Ошибка подключения!
Повторите попытку!
                        ''')

        except:
            # else:
            show_dialog(title="Ошибка!", text='''
Ошибка подключения!
Повторите попытку!
                                    ''')

    def rasban(self):
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
        # print(p)
        try:
            if p and p < max_ping:
                # self.ids["wifi_error"].opacity = 0
                ref = db.reference(f"/{self.ban_name.text}/ban")
                ref.set({"is_banned": False, "cause": None})
        except:
            pass

    def ban(self):
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
        # print(p)
        try:
            if p and p < max_ping:
                # self.ids["wifi_error"].opacity = 0
                ref = db.reference(f"/{self.ban_name.text}/ban")
                ref.set({"is_banned": True, "cause": self.ban_cause.text})
        except:
            pass

    def sign_out(self):
        # print(self.manager.current)
        global offline, data, cur_nav, auth_succefull
        auth_succefull = False
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")

        # if p and p < max_ping:
        # auth_succefull = False

        Account.data = copy.deepcopy(no_data)

        # os.remove("avatar.png")
        try:
            os.remove("data.pickle")
        except:
            pass

        # set_data()
        self.ids[Account.cur_nav].set_state("close")
        Account.cur_nav = "nav_drawer2"
        self.ads.show_interstitial()

        # print(self.ids[cur_nav].state)
        # os.remove("data.pickle")
        # self.manager.current = "auth"
        # else:

    #             show_dialog(title="Ошибка!", text='''
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
        self.ids[Account.cur_nav].set_state("open")

    def main_loop(self, dt):
        global auth_succefull
        # if auth_succefull:
        #     pass
        # Thread(target=self.shop_update).start()

        self.ui_update()
        # self.ui_update()

    async def shop_update(self, dd):
        while True:
            await ak.sleep(1 / 3)
            for name, values in store_items.items():
                if name in Account.data["data"]["inventory"]:
                    if values["type"] == "mouse":
                        check = self.ids["mining_shop"].ids[f"choose_current_{name}"]

                        check.disabled = False
                    else:
                        check = self.ids["bot_shop"].ids[f"choose_current_{name}"]

                        check.disabled = False
                    if Account.data["data"]["mouse"] == name or Account.data["data"]["bot"]["video card"] == name:
                        check.active = True
                else:
                    if values["type"] == "mouse":
                        check = self.ids["mining_shop"].ids[f"choose_current_{name}"]

                        check.disabled = True
                    else:
                        check = self.ids["bot_shop"].ids[f"choose_current_{name}"]

                        check.disabled = True

            for i in self.ids["mining_shop"].children:
                # if i.name in Account.data["data"]["inventory"]:
                i.theme_text_color = "Custom"
                if i.name in bonuse_items_names and i.name not in Account.data["data"][
                    "inventory"]:  # Если эта мышь призовая и не выбита из сундука
                    i.text_color = "ff9100"
                    i.secondary_text = f"[color=ff9100]Можно найти в сундуке[/color]"

                elif i.name in Account.data["data"]["inventory"]:  # Если купили мышь
                    price = Account.data["data"]["inventory"][i.name]["price"]
                    if i.name in bonuse_items_names:
                        i.secondary_text = f"[color=ff9100]Не прокачивается![/color]"
                        i.text_color = "ff9100"
                    else:
                        # if i.name in bonuse_items_names:
                        i.secondary_text = f"Цена прокачки: {'{0:.6f}'.format(price)} TON"
                else:  # Если не куплена
                    price = store_items[i.name]["price"]

                    i.secondary_text = f"Цена: {'{0:.6f}'.format(price)} TON"
            for i in self.ids["bot_shop"].children:
                i.theme_text_color = "Custom"
                if i.name in bonuse_items_names and i.name not in Account.data["data"][
                    "inventory"]:  # Если эта видеокарта призовая и не выбита из сундука
                    i.text_color = "ff9100"
                    i.secondary_text = f"[color=ff9100]Можно найти в сундуке[/color]"

                elif i.name in Account.data["data"]["inventory"]:  # Если купили видеокарту
                    price = Account.data["data"]["inventory"][i.name]["price"]
                    if i.name in bonuse_items_names:
                        i.secondary_text = f"[color=ff9100]Не прокачивается![/color]"
                        i.text_color = "ff9100"
                    else:
                        # if i.name in bonuse_items_names:
                        i.secondary_text = f"Цена прокачки: {'{0:.6f}'.format(price)} TON"
                else:  # Если не куплена
                    if i.name in store_items:
                        price = store_items[i.name]["price"]

                        i.secondary_text = f"Цена: {'{0:.6f}'.format(price)} TON"

    def show_privilege_permissions(self, permission):
        if permission == "Админ":
            # print(123)
            scr = ScrollView()
            b = MDBoxLayout(
                orientation="vertical",
                # padding=20,
                size_hint_y=.8,
                pos_hint={"center_y": .5},
                spacing=30
            )
            b3 = MDBoxLayout(
                orientation="vertical",
                # padding=20,
                size_hint_y=.8,
                pos_hint={"center_y": .5},
                spacing=30
            )
            c = MDFillRoundFlatButton(
                text="Забанить игрока",
                font_name="main_font.ttf",
                font_size="20sp",
                pos_hint={"center_x": .5},
                size_hint=(.3, None),
            )
            b3.add_widget(c)
            scr.add_widget(b3)
            b2 = MDBoxLayout(
                # orientation="vertical",
                size_hint_y=.4,
                # md_bg_color=(1,0,0,1),
                # padding=20,
                spacing="2sp"
            )
            c2 = MDFillRoundFlatButton(
                text="Закрыть",
                font_name="main_font.ttf",
                font_size="20sp",
                size_hint=(.3, None),
            )
            b2.add_widget(c2)

            b.add_widget(scr)
            b.add_widget(b2)

            # b.add_widget(scr)

            ban_dialog = Popup(title=permission, title_color=(0, 0, 0, 1), content=b, title_font="main_font.ttf",
                               title_align="center", title_size="30sp",
                               size_hint=(.9, .7), background="dialog.png")
            c2.bind(on_release=lambda a: ban_dialog.dismiss())
            c.bind(on_release=lambda a: self.open_ban_dialog())
            ban_dialog.open()

    def ui_update(self):
        # print(12344444)
        # self.ids["tokens_num_games"].text = f'''Жетоны: {data["data"]["token"]["value"]}'''
        # print(data)
        if Account.data["data"]["bot"]["alow_bot"]:
            if Account.data["data"]["bot"]["active"]:
                self.ids["autominer"].secondary_text = "Активен"

            else:
                self.ids["autominer"].secondary_text = "Неактивен"

        self.ids["ton_num_shop"].text = f'''TON: {'{0:.6f}'.format(Account.data["data"]["TON"])}'''
        self.ids["ton_num_games"].text = f'''TON: {'{0:.6f}'.format(Account.data["data"]["TON"])}'''
        # self.ids[
        #     "summation_text"].secondary_text = f'''Цена: {'{0:.6f}'.format(data["data"]["summation"]["price"])} TON'''
        # print(data["account"])
        if Account.data["account"]:
            self.ids["player_name"].text = f'''Имя: {Account.data["account"]["name"]}'''
            self.ids["privilege"].text = f'''{Account.data["account"]["privilege"]}'''
            self.ids["privilege_icon"].on_press = lambda: self.show_privilege_permissions(Account.data["account"]["privilege"])

            self.ids["player_password"].text = f'''Пароль: {Account.data["account"]["password"]}'''

            self.ids["avatar"].source = Account.data["account"]["avatar"]
        if Account.data["account"].get("privilege") == "Админ":
            self.ids["privilege"].color = (1, 0, 0, 1)
            self.ids["privilege_icon"].source = "admin.png"
            self.ids["privilege_icon"].disabled = False
            self.ids["privilege_icon"].opacity = 1

        elif Account.data["account"].get("privilege") == "Модератор":
            self.ids["privilege"].color = (1, .67, .2, 1)
            self.ids["privilege_icon"].source = "moderator.png"
            self.ids["privilege_icon"].disabled = False
            self.ids["privilege_icon"].opacity = 1
        elif Account.data["account"].get("privilege") == "Helper":
            self.ids["privilege"].color = (0.2, .9, .88, 1)
            self.ids["privilege_icon"].source = "helper.png"
            self.ids["privilege_icon"].disabled = False
            self.ids["privilege_icon"].opacity = 1
        else:
            self.ids["privilege"].color = (0, 0, 0, 1)
            self.ids["privilege_icon"].disabled = True
            self.ids["privilege_icon"].opacity = 0
        # self.ids["token_price"].text = f'''Цена: {'{0:.6f}'.format(data["data"]["token"]["price"])} TON'''

        # print(data["account"])
        # self.ids[
        #     'text_doubling'].secondary_text = f'''Цена: {'{0:.6f}'.format(self.doubling_data["price"])} TON'''
        # self.ids[
        #     'text_doubling'].tertiary_text = f'''Увеличение до x{'{0:.6f}'.format(self.doubling_data["value"] / 100 * 30)}'''
        # Удвоение майнинга с:{data["data"]["doubling"] } на 30%

        #        self.ids[
        #            'text_summation'].secondary_text = f'''Цена: {'{0:.6f}'.format(self.summation_data["summation_price"])} TON'''
        self.ids['TON_num'].text = f'''TON: {'{0:.6f}'.format(Account.data["data"]["TON"])}'''
        # self.ids['video_shop'].secondary_text = f'''цена: {'{0:.6f}'.format(data["data"]["bot"]["price"])} TON'''
        # self.ids['text_bot_summation'].secondary_text = f'''цена: {data["data"]["bot"]["summation_price"]} TON'''
        #
        #             #App.get_running_app().root.ids['TON_num_natural'].text = f"точнее: {data["data"]['TON']}"
        #
        self.ids["tired_num"].text = f"   {int(Account.data['data']['tired_num'])}%"
        # print(self.ids["mining_shop"].ids)

    def to_auth(self):
        self.ids[Account.cur_nav].set_state()
        self.ads.show_interstitial()
        self.manager.current = "auth"

    def miner_loop(self, dt):
        global auth_succefull
        # if auth_succefull:

        # if auth_succefull:
        self.autominer()

        # if self.ids["mining_button"].state != "down" and Account.data['data']["tired_num"] < 30:
        #     Account.data['data']["tired_num"] += 1

    def tired_loop(self, dt):
        global auth_succefull
        # if auth_succefull:

        if self.ids["mining_button"].state != "down" and Account.data['data']["tired_num"] < 100:
            Account.data['data']["tired_num"] += 1

    def show_notify(self, title, message, app_icon, name="notify"):
        if name not in notifications:
            plyer.notification.notify(title=title, message=message,
                                      ticker="TON кликер", app_name="TON кликер", app_icon=app_icon)
            notifications.append(name)

    def autominer(self):
        if Account.data['data']["bot"]["alow_bot"]:
            video = Account.data['data']["bot"]["video card"]

            boost = Account.data['data']["inventory"][video]["boost"]

            Account.data['data']["TON"] += boost

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

    def delete_account_confirm(self):
        show_dialog(title="Удалить?", text="Этот аккаунт удалится безвозвратно!", exit=True,
                    command=self.delete_account)

    def delete_account(self):
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")

        try:
            if p and p < max_ping:
                name = Account.data['account']['name']
                self.sign_out()
                ref = db.reference(f"/players/{name}")
                ref.delete()
            else:
                show_dialog(title="Ошибка!", text='''
        Проверьте подключение к интернету и попробуйте снова.
                                            ''')

        except:
            show_dialog(title="Ошибка!", text='''
        Проверьте подключение к интернету и попробуйте снова.
                            ''')

    def open_chest(self, is_bought=False):
        # t_b = random.randint(1, 5)
        # if t_b == 1:
        # type_index = random.randint(0, (len(self.bonuses) - 1) * 10)
        # bonuse_items = store_items[]
        r = random.randint(0, 15)
        # r = int(bonuse_index)
        # for name, item in store_items.items():

        if r == 4:
            bonuse = random.choice(list(bonuse_items_names))
            item = store_items[bonuse]
            # self.main_dialog.dismiss()
            Account.data["data"]["inventory"][bonuse] = item
            if item["type"] == "video card":
                show_dialog(title="Поздравляем!", text=f"Вам выпала видеокарта {bonuse}!")
            else:
                show_dialog(title="Поздравляем!", text=f"Вам выпала мышь {bonuse}!")
        else:

            r = round(random.uniform(0, 1), 6)
            # r /= 100
            Account.data['data']["TON"] += Account.data['data']["TON"] * r
            # self.main_dialog.dismiss()
            show_dialog(title="Поздравляем!",
                        text=f"Вам выпало {'{0:.6f}'.format(data['data']['TON'] * r)} TON!")
        self.chest_dialog.dismiss()
        # break
        # else:
        #
        #     r = random.randint(30, 100)
        #     r /= 100
        #     Account.data['data']["TON"] += Account.data['data']["TON"] * r
        #     self.chest_dialog.dismiss()
        #     show_dialog(title="Поздравляем!",
        #                 text=f"Вам выпало {'{0:.6f}'.format(data['data']['TON'] * r)} TON!")
        notifications.remove("open_chest_info")
        if is_bought:
            Account.data["data"]["TON"] -= Account.data["data"]["chest"]["price"]
            Account.data["data"]["chest"]["price"] += Account.data["data"]["chest"]["price"] * 0.2
        else:
            now = datetime.datetime.now()
            Account.data["data"]["chest"]["last_opened"] = now.isoformat()
        # day = Account.data['data']["chest_last_opened"].day
        # hour = Account.data['data']["chest_last_opened"].hour
        # minute = Account.data['data']["chest_last_opened"].minute
        #
        # if datetime.now() >= Account.data['data']["chest_last_opened"] + timedelta(hours=2):
        #     type_index = random.randint(0, len(self.bonuses) - 1)
        #     bonuse_items = self.bonuses[type_index]
        #     bonuse_index = random.randint(0, len(bonuse_items) - 1)
        #     for name, item in bonuse_items.items():
        #         if bonuse_index == item["index"]:
        #
        #             bonuse = name
        #             if item["type"] == "video card" and item["index"] >= store_items[data['data']["bot"]["video card"]]["index"]:
        #                 Account.data['data']["bot"]["video card"] = bonuse
        #                 show_dialog(title="Поздравляем!", text=f"Вам выпала видеокарта {bonuse}")
        #             elif item["type"] == "mouse" and item["index"] >= self.mouses[data['data']["mouse"]]["index"]:
        #                 Account.data['data']["mouse"] = bonuse
        #                 show_dialog(title="Поздравляем!", text=f"Вам выпала мышь {bonuse}")
        #             Account.data['data']["chest_last_opened"] = datetime.now()
        #
        #             break
        # else:
        #     print(data['data']["chest_last_opened"], int(str(datetime.now().hour) + str(datetime.now().minute)))
        #
        #     show_dialog(title="Ой!", text=f'До следующего бесплатного сундука осталось {data['data']["chest_last_opened"] + timedelta(hours=2) - datetime.now()}')

    def add_auction(self):
        pass


class Loading(Screen):
    pass


class app(MDApp):
    def on_start(self):

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
        import time
        start_time = time.time()
        # Clock.schedule_interval(self.start_loops, 1/30)
        self.screen_manager = ScreenManager()
        self.screen_manager.transition = NoTransition()
        # Logger.info('Loader: Screeen manager has been loaded.')
        self.loading = Loading(name="loading")

        # self.screen_manager.add_widget(Navigate_without_account(name="scr"))
        self.screen_manager.add_widget(self.loading)
        # Logger.info('Loader: Spinner screen has been loaded.')
        self.screen_manager.current = "loading"
        # template = GameTemplate(name="template")
        # self.screen_manager.add_widget(template)
        # print(123)
        self.loading.ids["loading"].text = "Загрузка экранов..."
        auth = Auth(name="auth")
        self.screen_manager.add_widget(auth)
        # Logger.info('Loader: Auth screen has been loaded.')
        # d = Error_show(name="error_show")
        # self.screen_manager.add_widget(d)
        # Logger.info('Loader: Error screen has been loaded.')

        # th = Thread(target=self.start_game)
        # .start()
        self.i = 0

        # Clock.schedule_once(self.start_game)

        # self.game.ids["scroll_mining"].do_scroll = False
        # self.game.ids["scroll_bot"].do_scroll = False
        # self.game.ids["scroll_mining"].opacity = 0
        # self.game.ids["scroll_bot"].opacity = 0
        # self.game = Clicker(name="clicker")
        #
        import time
        start_time = time.time()
        # self.start_game()

        # th = Thread(target=self.load_store_items)
        # th.start()

        # self.load_store_items()
        # self.fps_monitor_start()
        # self.load_music()

        #
        print("Загрузка главного экрана...")
        self.game = Clicker(name="clicker")
        #
        # self.screen_manager.add_widget(self.game)

        # Clock.schedule_interval(self.game.miner_loop, 1)

        # # self.load_store_items()
        self.screen_manager.add_widget(self.game)
        print("Загрузка главного экрана завершена длительностью: %s сек " % (time.time() - start_time))
        # print(list(store_items))
        # self.lsi = Clock.schedule_interval(self.load_store_items, 1/60)
        # import time
        # start_time = time.time()
        # print(list(store_items))

        # print(list(store_items))
        #
        # cred_obj = firebase_admin.credentials.Certificate(
        #     'ton-clicker-firebase-adminsdk-cf1xz-8ad3090323.json')
        # app_d = firebase_admin.initialize_app(cred_obj, {
        #     'databaseURL': "https://ton-clicker-default-rtdb.firebaseio.com/"
        # })

        import time
        start_time = time.time()
        # self.start_game()
        # self.load_store_items()

        # self.load_store_items()
        # self.fps_monitor_start()
        # self.load_music()

        Thread(target=self.load_store_items).start()
        # self.load_music()
        # print("--- %s seconds ---" % (time.time() - start_time))
        return self.screen_manager

    def load_music(self, dt):
        d = SoundLoader.load("soundtrack.wav")

        if d:
            d.loop = True
            d.volume = .3
            # d.pitch = .5
            d.play()
            # print("--- %s seconds ---" % (time.time() - start_time))
        # pygame.init()
        # #sound_effect = pygame.mixer.Sound('soundtrack.wav')
        # pygame.mixer.music.load('soundtrack.wav')
        # pygame.mixer.music.play()

    def load_store_items(self):
        global auth_succefull
        import time
        e = ak.Event()
        # start_time = time.time()
        # import time
        # start_time = time.time()

        # print("--- %s seconds ---" % (time.time() - start_time))
        # print("--- %s seconds ---" % (time.time() - start_time))
        self.loading.ids["loading"].text = "Подключение к серверу..."
        self.start_game()
        Clock.schedule_interval(self.game.main_loop, 1 / 10)

        async def ls(dt):
            self.loading.ids["loading"].text = "Загрузка магазина..."
            self.game.ids["mining_shop"].do_scroll_y = False
            self.game.ids["bot_shop"].do_scroll_y = False
            for name, value in store_items.items():
                await ak.sleep(1 / 60)
                # name = value["name"]
                price = value["price"]
                # index = value["index"]
                type_item = value["type"]
                texture = value["texture"]
                # print(i, Account.data["data"]["inventory"])
                if name in Account.data["data"]["inventory"]:
                    # print(i)
                    # boost = value["boost"]
                    price = Account.data["data"]["inventory"][name]["price"]
                    # index = value["index"]
                    type_item = Account.data["data"]["inventory"][name]["type"]
                    texture = Account.data["data"]["inventory"][name]["texture"]

                # print(texture)

                # print("list loading")
                start_time = time.time()
                # self.start_game()
                # self.screen_manager.current = "clicker"
                # print("--- %s seconds ---" % (time.time() - start_time))
                if name in bonuse_items_names and name not in Account.data["data"]["inventory"]:
                    line = TwoLineAvatarIconListItem(

                        text=f"[color=ff9100]{name}[/color]",

                        # source="",
                        secondary_text=f"[color=ff9100]Можно найти в сундуке[/color]",
                        # font_style="Custom",
                        # font_name="main_font.ttf",
                        # font_style="Subtitle1",
                        # type=type_card,
                        on_press=self.game.buy_confirm
                    )
                else:
                    line = TwoLineAvatarIconListItem(

                        text=name,

                        # source="",
                        secondary_text=f"Цена: {'{0:.6f}'.format(price)} TON",
                        # font_style="Custom",
                        # font_name="main_font.ttf",
                        # font_style="Subtitle1",
                        # type=type_card,
                        on_press=self.game.buy_confirm
                    )
                line.name = name
                # body = IRightBodyTouch()
                # body.add_widget(Check())
                image = IconLeftWidget(icon=texture)
                line.add_widget(image)

                # self.game.ids["bot_shop"].add_widget(MDLabel(text="hi"))
                if type_item == "video card" or type_item == "processor":

                    if name == Account.data["data"]["bot"]["video card"]:
                        check = Check(group="current_video card", radio_icon_down="check-circle",
                                      radio_icon_normal="check-circle", active=True, on_press=self.game.current_item)
                    else:
                        # if name == Account.data["data"]["mouse"]:
                        check = Check(group="current_video card", radio_icon_down="check-circle",
                                      radio_icon_normal="check-circle", on_press=self.game.current_item)
                    if name in Account.data["data"]["inventory"]:
                        check.opacity = 1

                    else:
                        check.opacity = 0
                        check.disabled = True
                    check.name = name

                    line.add_widget(check)
                    # print(name)
                    self.game.ids["bot_shop"].ids[f"choose_current_{name}"] = check
                    self.game.ids["bot_shop"].add_widget(line)

                elif type_item == "mouse":
                    if name == Account.data["data"]["mouse"]:
                        check = Check(group="current_mouse", radio_icon_down="check-circle",
                                      radio_icon_normal="check-circle", active=True, on_press=self.game.current_item)
                    else:
                        # if name == Account.data["data"]["mouse"]:
                        check = Check(group="current_mouse", radio_icon_down="check-circle",
                                      radio_icon_normal="check-circle", on_press=self.game.current_item)
                    if name in Account.data["data"]["inventory"]:
                        check.opacity = 1
                    else:
                        check.opacity = 0
                        check.disabled = True
                    check.name = name
                    line.add_widget(check)
                    self.game.ids["mining_shop"].ids[f"choose_current_{name}"] = check
                    self.game.ids["mining_shop"].add_widget(line)

            # self.load_music()

            # Clock.schedule_interval(self.game.shop_update, 1)
            # Clock.schedule_interval(self.game.shop_update, 10 / 5)
            self.loading.ids["loading"].text = "Загрузка..."
            self.screen_manager.current = "clicker"
            ak.start(self.game.shop_update(e))
            self.game.ids["mining_shop"].do_scroll_y = True
            self.game.ids["bot_shop"].do_scroll_y = True

        ak.start(ls(e))
        # Clock.schedule_once(ls)
        timer(lambda: self.game.bot_state("off"), 30 * 60)
        self.background_loop_state = True

        # async def background_loop(bb):

        while self.background_loop_state:
            time.sleep(1)
            # await ak.sleep(1)
            self.game.tired_loop(dt=1)
            if Account.data["data"]["bot"]["active"]:
                self.game.miner_loop(dt=1)
            # print(123)
            # Если пользователь зарегистрирован
            th = Thread(target=self.game.update_data)
            th.start()
            now = datetime.datetime.now()
            last_opened = datetime.datetime.fromisoformat(
                Account.data["data"]["chest"].setdefault("last_opened", datetime.datetime.now().isoformat()))
            # print(now - last_opened > datetime.timedelta(hours=24))

            if now - last_opened > datetime.timedelta(hours=24):
                if plyer.utils.platform == "win":
                    Clock.schedule_once(
                        lambda a: self.game.show_notify(title="TON кликер",
                                                        message="Вы снова вы можете открыть сундук!",
                                                        app_icon="chest_normal.ico", name="open_chest_info"))
                else:
                    Clock.schedule_once(
                        lambda a: self.game.show_notify(title="TON кликер",
                                                        message="Вы снова вы можете открыть сундук!",
                                                        app_icon="blue.png", name="open_chest_info"))

        # ak.start(background_loop(e))

    # @cache
    #    def ls(self, i):
    # time.sleep(1)

    def start_game(self):
        global data, auth_succefull, cur_nav
        no_data["data"]["inventory"] = {"Oklick 105S": store_items["Oklick 105S"],
                                        "Celeron Pro": store_items["Celeron Pro"]}
        try:
            with open("data.pickle", "rb") as f:
                Account.data = pickle.load(f)
                #check_lost_keys()
                Logger.info('INFO: Account detected')
                #print(Account.data)


        except:

            Account.data = copy.deepcopy(no_data)

            Logger.info('INFO: No account')

        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")

        if p and p < max_ping:
            d = None
            try:
                ref = db.reference(f"/disable_app")
                d = ref.get()

            except:
                pass
            if d == "True":
                raise BaseException("It is Star Wormwood inc. project!")

        # set_data()

        if Account.data["account"]:
            Account.cur_nav = "nav_drawer1"
        else:
            Account.cur_nav = "nav_drawer2"

        auth_succefull = True
        # self.screen_manager.current = "clicker"
        # Clock.schedule_once(self.load_music)


# Запуск проекта
if __name__ == "__main__":
    app().run()

up_data = False
