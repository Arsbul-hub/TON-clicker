# import webbrowser
import asynckivy
from kivy.base import EventLoop
import webbrowser
from kivy.uix.button import Button
from kivymd.uix.list import IconLeftWidget
from kivy.uix.screenmanager import *
# from kivymd.uix.button import MDIconButton
from kivmob import KivMob, RewardedListenerInterface
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
from kivy.utils import get_color_from_hex as C

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

from kivy.clock import Clock

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

from kivy.uix.tabbedpanel import TabbedPanel

# from kivy.lang.builder import Builder

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

             # "doubling": {"value": 1, "price": 0.001},
             "bot": {"alow_bot": False, "doubling": {"value": 1, "doubling_price": 0.001},
                     "video card": "Celeron Pro", "price": 1,
                     "active": False,
                     "summation_price": 0.000001, "summation_num": 0},
             # "token": {"price": 0.000100, "value": 5},
             # "summation": {"price": 0.000001, "value": 0.000001},
             # "chest_last_opened": datetime(year=2021,month=1,day=1,hour=1,minute=1),
             "chest": {"num": 1, "price": 0.000150, "last_opened": datetime.datetime.now().isoformat()},
             "mouse": "Oklick 105S",
             "tired_num": 40,
             "is_tired": False,

             }
}

t = 0


def set_data():
    c = Clicker

    c.account = data["account"]
    c.player_data = data["data"]
    c.bot_data = data["data"]["bot"]
    c.doubling_data = data["data"]["doubling"]
    c.summation_data = data["data"]["summation"]

    # adaptive_width = True


def check_lost_keys():
    if "active" not in data["data"]["bot"]:
        data["data"]["bot"]["active"] = False


def timer(command, seconds=1):
    Thread(target=lambda: start_timer(command, seconds)).start()


def start_timer(command, seconds=1):
    # for i in range(seconds):
    time.sleep(seconds)
    command()


def show_dialog(text, title="Ошибка!", auto_close=True, exit=False, command=lambda: print("Hello")):
    dialog = None
    if not dialog:
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
                        font_size="25sp",

                        # theme_text_color="Custom",
                        # color=(0, 0, 0, 1),
                        )
        )
        c2 = MDFillRoundFlatButton(
            text="Ок",
            font_size="25sp",
            # halign="center",
            pos_hint={"center_x": .5},
            size_hint=(.3, None),

        )
        if exit:
            b2 = MDBoxLayout(spacing="5sp")
            c1 = MDFillRoundFlatButton(
                text="Отмена",
                font_size="25sp",
                # halign="center",
                pos_hint={"center_x": .5},
                size_hint=(.3, None),

            )
            b2.add_widget(c1)

            b2.add_widget(c2)
            b.add_widget(b2)
        else:
            b.add_widget(c2)
        dialog = Popup(title=title, title_color=(0, 0, 0, 1), auto_dismiss=auto_close, separator_height="4dp",
                       title_font="main_font.ttf",
                       title_align="center", title_size="30sp", content=b,
                       size_hint=(.9, .7))

        dialog.background = "dialog.png"
        # print(dialog.background)
        c2.bind(on_press=lambda a: [dialog.dismiss(), command()])
        if exit:
            c1.bind(on_press=lambda a: dialog.dismiss())
        dialog.open()


# import pygame


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
            data["data"]["TON"] += self.finded_numbers * self.bet
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


        if p != False and p != None and p < max_ping:
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


        if p != False and p != None and p < max_ping:
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
                    else:
                        # self.manager.transition = NoTransition()
                        # self.manager.current = "auth"
                        show_dialog('''
Аккаует с таким ником уже существует!
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


class CustomLabel(Label):
    pass


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
                data = pickle.load(f)

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
                # set_data()
                self.manager.current = "clicker"

            except:

                self.manager.current = "auth"


class Auth(Screen):
    norm = StringProperty('')

    def __init__(self, **kwargs):

        # self.f1 = Widget()
        super().__init__(**kwargs)

        # self.main_font_size = main_font_size

    def close_dialog(self):
        if self.dialog:
            self.dialog.dismiss()

    def load_avatar(self, p):
        self.ids["avatar_image"].source = p

    def login(self):
        # self.manager.current = "loading"
        self.start_login()
        # th = Thread(target=self.start_login)
        # th.start()

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
                        show_dialog('''
Неверный логин или пароль!
Проверьте их корректность!
                    ''')
                except:
                    self.manager.current = "auth"
                    show_dialog('''
Ошибка подключения!
Повторите попытку!
                                    ''')



            else:
                self.manager.current = "auth"
                show_dialog('''
Все поля должны быть заполнены!
И не должны содержать специальные симбволы пробела и #$./?
    ''')
        else:
            self.manager.current = "auth"
            show_dialog('''
Ошибка подключения!
Повторите попытку!
                ''')

    def registration(self):
        # self.manager.current = "loading"
        # th = Thread(target=self.start_registration)
        # th.start()
        self.start_registration()

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
            if len(player_name) >= 5 and player_password != "" and player_name != "" and string_check == None:
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

                        self.ids["password_r"].ids["text_field"].text = self.norm

                        self.start_loops()
                    else:
                        # self.manager.transition = NoTransition()
                        self.manager.current = "auth"
                        show_dialog('''
Аккаует с таким ником уже существует!
Придумайте новый!
    ''')
                except:
                    self.manager.current = "auth"
                    show_dialog('''
Ошибка подключения!
Повторите попытку!
                                    ''')
            elif len(player_name) < 5:
                show_dialog('''
Имя должнобыть не меньше 5 симбволов в длину!
''')
            else:
                self.manager.current = "auth"
                show_dialog('''
Все поля должны быть заполнены!
И не должны содержать специальные симбволы пробела и #$./?
    ''')

        else:
            self.manager.current = "auth"
            show_dialog('''
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

            show_dialog(title="Ошибка!", text='''
Проверьте подключение к интернету и попробуйте снова.
        ''')

    def start_loops(self):
        global auth_succefull, offline, data, cur_nav

        # c = Clicker()
        # c.#set_data()
        # set_data()
        check_lost_keys()
        auth_succefull = True
        self.game = Clicker
        cur_nav = "nav_drawer1"

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

        self.store_items = {
            "Celeron Pro": {"index": 0, "texture": "video card.png", "name": "Celeron Pro", "type": "processor",
                            "boost": 0.000001, "price": 0.100000},
            "Gt 770": {"index": 1, "texture": "video card.png", "name": "Gt 770", "type": "video card",
                       "boost": 0.000020, "price": 1.000000},
            "Gt 870": {"index": 2, "texture": "video card.png", "name": "Gt 870", "type": "video card",
                       "boost": 0.000020, "price": 10.000000},
            "Gtx 970": {"index": 3, "texture": "video card.png", "name": "Gtx 970", "type": "video card",
                        "boost": 0.000030, "price": 100.000000},
            "Rtx 1050": {"index": 4, "texture": "video card.png", "name": "Rtx 1050", "type": "video card",
                         "boost": 0.000040, "price": 1000.000000},
            "Rtx 1070": {"index": 5, "texture": "video card.png", "name": "Rtx 1070", "type": "video card",
                         "boost": 0.000050, "price": 10000.000000},
            "Rtx 2060": {"index": 6, "texture": "video card.png", "name": "Rtx 2060", "type": "video card",
                         "boost": 0.000060, "price": 100000.000000},
            "Rtx 2070 Super": {"index": 7, "texture": "video card.png", "name": "Rtx 2070 Super", "type": "video card",
                               "boost": 0.000070, "price": 1000000.000000},
            "Rtx 2080 TI": {"index": 8, "texture": "video card.png", "name": "Rtx 2080 TI", "type": "video card",
                            "boost": 0.000080, "price": 10000000.000000},
            "Rtx 3060 Super": {"index": 9, "texture": "video card.png", "name": "Rtx 3060 Super", "type": "video card",
                               "boost": 0.000090, "price": 100000000.000000},
            # "Rtx 3090 Super TI": {"index": 10, "texture": "video card.png", "name": "Rtx 3090 Super TI",
            #                      "type": "video card", "boost": 0.000100, "price": 0.029541},
            # "Rtx 8000 Super TI Extreme Edition": {"index": 11, "texture": "video card.png",
            #                                      "name": "Rtx 8000 Super TI Extreme Edition", "type": "video card",
            #                                      "boost": 0.0003, "price": 0.035000},

            "Oklick 105S": {"index": 0, "texture": "mouse-variant", "type": "mouse", "name": "Oklick 105S",
                            "boost": 0.000001, "price": 0.000001, "tired": 1},
            "Canyon CNE-CMS05DG": {"index": 1, "texture": "mouse-variant", "type": "mouse",
                                   "name": "Canyon CNE-CMS05DG", "boost": 0.00001, "price": 0.000010, "tired": .9},
            "QUMO Office M14": {"index": 2, "texture": "mouse-variant", "type": "mouse", "name": "QUMO Office M14",
                                "boost": 0.00005, "price": 0.001000, "tired": .8},
            "Ritmix ROM-111": {"index": 3, "texture": "mouse-variant", "type": "mouse", "name": "Ritmix ROM-111",
                               "boost": 0.0001, "price": 0.100000, "tired": .7},
            "Oklick 145M": {"index": 4, "texture": "mouse-variant", "type": "mouse", "name": "Oklick 145M",
                            "boost": 0.0005, "price": 1.000000, "tired": .6},
            "Ritmix ROM-202": {"index": 5, "texture": "mouse-variant", "type": "mouse", "name": "Ritmix ROM-202",
                               "boost": 0.001, "price": 10.000000, "tired": .9},
            "Smartbuy ONE SBM-265-K": {"index": 6, "texture": "mouse-variant", "type": "mouse",
                                       "name": "Smartbuy ONE SBM-265-K", "boost": 0.005, "price": 1000.000000,
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
        self.stage = 0
        self.i = 0
        self.tr = None
        # print(sys.getsizeof(self.store_items))
        self.bonuses = [self.money, self.store_items]
        self.n = 0
        self.update_nav_drawer = False
        self.current_effect = {"name": None, "time": 0, "lvl": 0}
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
        self.dialog = Popup(title="Контакты", title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                            title_align="center", title_size="30sp", content=b,
                            size_hint=(.9, .7), background="dialog.png")
        #
        self.dialog.open()

    def current_item(self, obj):
        # print(222)
        name = obj.name

        # print(self.player_data["inventory"][name]["type"])
        if data["data"]["inventory"][name]["type"] == "video card" or data["data"]["inventory"][name][
            "type"] == "processor":
            data["data"]["bot"]["video card"] = name
            Snackbar(text=f"Выбрана видеокарта {name}", duration=.1).open()
            # print(data["data"]["bot"]["video card"])
        if data["data"]["inventory"][name]["type"] == "mouse":
            data["data"]["mouse"] = name
            Snackbar(text=f"Выбрана мышка {name}", duration=.1).open()

    def load_top(self):
        self.ids["error_load_top"].text = ""
        # self.ids["fl"].opacity = 0
        # self.ids["scroll_top"].opacity = 0
        # self.ids["scroll_top"].do_scroll = False
        # self.ids["retry_load_top"].opacity = 0
        # self.ids["top_loading"].active = False

        # self.ids["top_loading"].active = True
        self.ads.show_interstitial()
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
        # print(p)
        if p != False and p != None and p < max_ping:
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


            self.ids["loading_top_text"].opacity = 1
            timer(self.loading_top, .1)


            print("--- %s seconds ---" % (time.time() - start_time))
            # self.loading_top()
        # th.join()

        # except:
        # self.ids["players_top"].add_widget(CustomLabel(text="Произошла ошибка подключения!\nОбновите список заново", font_name="main_font.ttf", font_size="25sp"))
        # self.ids["fl"].disabled = False
        #    self.ids["error_load_top"].text = "Произошла ошибка подключения!\nОбновите список"
        # self.ids["retry_load_top"].opacity = 1
        # self.ids["top_loading"].active = False
        else:
            self.ids["players_top"].opacity = 0
            self.ids["players_top"].disabled = True
            self.ids["error_load_top"].text = "Произошла ошибка подключения!\nОбновите список"
            # self.ids["players_top"].add_widget(
        #     CustomLabel(text="Произошла ошибка подключения!\nОбновите список заново", font_name="main_font.ttf",
        #                 font_size="25sp"))
        # self.ids["fl"].disabled = False
        # self.ids["error_load_top"].opacity = 1
        # self.ids["retry_load_top"].opacity = 1
        # self.ids["top_loading"].active = False

    def bot_state(self, state):
        if state == "on":
            data["data"]["bot"]["active"] = True
        if state == "off":
            data["data"]["bot"]["active"] = False

    def loading_top(self):
        ref = db.reference(f'/players/')
        sorted_data = ref.order_by_child(f'data/TON').limit_to_last(15).get()
        results = list(sorted_data)
        # print(results)

        stage = 0
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

                widget.text = f"{name}"
                widget.secondary_text = f"TON: {'{0:.6f}'.format(ton)}"
                widget.avatar.source = avatar
                widget.text_color = (0, 0, 0, 1)
                # widget.right_text.text = ""
                if privilege and privilege == "Админ":
                    widget.text = f"{name} - Админ"
                    widget.theme_text_color = "Custom"
                    widget.text_color = (1, .1, .1, 1)
                if stage == 1:
                    widget.medal.source = "gold_medal.png"
                elif stage == 2:
                    widget.medal.source = "silver_medal.png"
                elif stage == 3:
                    widget.medal.source = "bronze_medal.png"
                # if name == data["account"]["name"]:
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
                line = TwoLineAvatarIconListItem(
                    text=f"{name}",
                    # source="",
                    secondary_text=f"TON: {'{0:.6f}'.format(ton)}",
                    # font_name="main_font.ttf",
                    # font_style="H6",
                    # type=type_card,
                )
                # on_press=lambda a: print("Hello")

                if privilege and privilege == "Админ":
                    line.text = f"{name} - Админ"
                    line.theme_text_color = "Custom"
                    line.text_color = (1, .1, .1, 1)
                medal = ImageRightWidget()

                line.add_widget(medal)
                line.medal = medal
                if stage == 1:
                    medal.source = "gold_medal.png"
                elif stage == 2:
                    medal.source = "silver_medal.png"
                elif stage == 3:
                    medal.source = "bronze_medal.png"
                # text = RightText(text="")
                # if name == data["account"]["name"]:
                #     text.text = "Вы"
                # line.add_widget(text)
                # line.right_text = text
                try:
                    image = ImageLeftWidget(source=avatar)

                    line.add_widget(image)
                    line.avatar = image
                except:
                    pass

                # ak.and_()

                self.ids["players_top"].add_widget(line)
        self.ids["players_top"].opacity = 1
        self.ids["players_top"].disabled = False
        self.ids["loading_top_text"].opacity = 0
    def effect(self, name, time, lvl):
        self.current_effect = {"name": name, "time": time, "lvl": lvl}
        timer(self.clear_effect, 60)

    def clear_effect(self):
        Snackbar(text="Эффект бодрости снят", duration=.4).open()
        self.current_effect = {"name": None, "time": None, "lvl": None}

    def start_game(self, name, *args):
        if name == "roulette":
            try:
                b = float(self.ids['bet_value'].text)
                if b >= data["data"]["TON"] * .2 and b <= data["data"]["TON"]:
                    self.ids['bet_value'].error = False
                    r = random.randint(1, 7)

                    # l = b * (-1) + self.ids['bet_value'].max
                    # m = data["data"]["TON"] - s
                    bet = b
                    data["data"]["TON"] -= bet
                    if r == 2 or r == 5:
                        data["data"]["TON"] += bet
                        show_dialog(title="Увы!", text=f"Вам ничего не выпало! \nТы не проиграл и не выииграл")
                    if r == 4 or r == 7:
                        # data["data"]["TON"] +-= bet
                        show_dialog(title="Увы!", text=f"Вы проиграли {'{0:.6f}'.format(bet)} TON.")
                    if r == 1:
                        bet *= 1.5
                        data["data"]["TON"] += bet
                        show_dialog(title="Поздравляем!", text=f"Вы выиграли {'{0:.6f}'.format(bet)} TON!")
                    if r == 3:
                        self.effect(name="disable_tired", time=60, lvl=2)
                        data["data"]["TON"] += bet
                        show_dialog(title="Поздравляем!", text=f"Вам выдан еффект бодрости 2 уровня на 60 секунд!\n")
                    if r == 6:
                        self.effect(name="disable_tired", time=60, lvl=4)
                        data["data"]["TON"] += bet
                        show_dialog(title="Поздравляем!", text=f"Вам выдан еффект бодрости 4 уровня на 60 сукунд!\n")
                elif b < data["data"]["TON"] * .3:
                    self.ids[
                        'bet_value'].helper_text = f'''Ставка не может быть меньше {'{0:.6f}'.format(data["data"]["TON"] * .3)} TON'''
                    self.ids['bet_value'].error = True
                elif b > data["data"]["TON"]:
                    self.ids[
                        'bet_value'].helper_text = f'''Ставка не может быть больше {'{0:.6f}'.format(data["data"]["TON"])} TON'''
                    self.ids['bet_value'].error = True
            except:
                self.ids['bet_value'].helper_text = "Ставка не корректна!"
                self.ids['bet_value'].error = True

            # data["data"]["TON"] -= w

            # print('{0:.6f}'.format(data["data"]["TON"]), '{0:.7f}'.format(s / 100 * l))
            # if r < 40:
            #     data["data"]["TON"] += w * 2
            #     show_dialog(title="Поздравляем!!!", text=f"Вы выиграли {'{0:.6f}'.format(w * 2)} TON")
            #
            # else:
            #     show_dialog(title="Увы!", text=f"Вы проиграли {'{0:.6f}'.format(w * 2)} TON")
        elif name == "bombs":
            try:
                b = float(self.ids['bet_find_it'].text)

                if self.bombs and b >= data["data"]["TON"] * .2 and b <= data["data"]["TON"]:
                    # self.ids['bet_find_it'].error = False
                    # self.bombs = args[0]
                    # if data["data"]["token"]["value"] - 1 >= 0:
                    # data["data"]["token"]["value"] -= 1
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
                        text=f"Текущий выигрыш: ",
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
                        md_bg_color=C("fe5722"),
                        pos_hint={"center_x": .5, "center_y": .7},
                        on_press=lambda a: self.is_won(name="bombs")
                    )
                    self.bombs_platform.add_widget(self.collect)
                    self.ids["bombs_layout"].add_widget(self.bombs_platform)
                    bet = float(self.ids["bet_find_it"].text)
                    self.old_bet = bet
                    data["data"]["TON"] -= bet
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
                                                       color=C("1f97f3"),
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
                elif self.bombs == None:
                    Snackbar(text="Количество бомб не выбрано!", duration=.4).open()
                elif b < data["data"]["TON"] * .3:
                    self.ids[
                        'bet_find_it'].helper_text = f'''Ставка не может быть меньше {'{0:.6f}'.format(data["data"]["TON"] * .3)} TON'''
                    self.ids['bet_find_it'].error = True
                elif b > data["data"]["TON"]:
                    self.ids[
                        'bet_find_it'].helper_text = f'''Ставка не может быть больше {'{0:.6f}'.format(data["data"]["TON"])} TON'''
                    self.ids['bet_find_it'].error = True
            except:
                self.ids[
                    'bet_find_it'].helper_text = f'''Ставка не коректна'''
                self.ids['bet_find_it'].error = True
        # data["data"]["T    ON"] += self.finded_numbers * self.bet
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
            data["data"]["TON"] += len(self.finded_numbers) * self.bet
            self.finded_numbers = []
            for i in self.ids["bombs_num"].children:
                i.opacity = .6

    def find_it(self, obj):
        # self.ids["find_it"].opacity = 1
        # print(obj.name)
        # if len(self.finded_numbers) < self.bombs:

        if obj.name == 1:
            self.finded_numbers.append(obj)
            # obj.source = "plate_win.png"
            self.win_label.text = f'Текущий выигрыш: \n[color=37e066][b]{"{0:.6f}".format(len(self.finded_numbers) * self.bet)} TON[/b][/color]'

            # timer(1, lambda: self.game_state("set_black_win_text"))
            obj.color = C("37e066")
            obj.disabled = True
        if obj.name == 0:
            # obj.disabled = True
            self.collect.disabled = True
            for i in self.platform.children:
                i.disabled = True
                if i.name == 0:
                    i.color = C("f54334")
                else:
                    i.color = C("388e3c")
                if i in self.finded_numbers:
                    i.color = C("37e066")
            # for i in self.finded_numbers:
            #     i.color = C("37e066")
            # obj.color = C("f54334")
            self.win_label.text = f'Текущий выигрыш: \n[color=ff0000][b]-{"{0:.6f}".format(self.old_bet)} TON[/b][/color]'
            timer(lambda: self.game_state("bombs_undo"), 3)

            # bombs_count = 0
            # for i in self.finded_numbers:
            # if i.name == 1:

            # self.finded_numbers = []
            # time.sleep(1)
            # title = "Увы!"
            # if self.finded_numbers > 0: title = "Поздравляем!"
            # else: title =
            # print(self.bet)

            # self.bombs = None
        # if obj.name == 0:

        # print("ty")
        # if len(self.finded_numbers) >= self.bombs:
        # print(">3")

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
            self.win_label.color = C("000000")
            # print(self.win_label.color)

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
                b = MDBoxLayout(orientation="vertical")
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

                b2 = MDBoxLayout(spacing="5sp")
                b2.add_widget(
                    MDFillRoundFlatButton(text="Купить!", md_bg_color=(0.1, 0.6, 0.9, 1.0), font_name="main_font.ttf",
                                          font_size="25sp",
                                          on_press=lambda a: self.buy(obj=obj)))
                b2.add_widget(
                    MDFillRoundFlatButton(text="Отмена", md_bg_color=(0.1, 0.6, 0.9, 1.0), font_name="main_font.ttf",
                                          font_size="25sp",
                                          on_press=lambda a: self.close_dialog()))
                b.add_widget(b2)
                # b.add_widget(MDLabel(text="Описание: Увеличивает майнинг в x раз"))
                # Buy_content(price=self.doubling_data["price"], boost=f'Увеличение удвоения майнинга с {self.doubling_data["price"]} TON/клик до {self.doubling_data["value"] + self.doubling_data["value"] / 100 * 30} TON/клик', description="Увеличивает майнинг в x раз"),
                self.dialog = Popup(title=name.capitalize(), title_color=(0, 0, 0, 1), title_font="main_font.ttf",
                                    title_align="center", title_size="30sp", content=b,
                                    size_hint=(.9, .7), background="dialog.png")
            if name == "удвоение майнинга":
                b = MDBoxLayout(orientation="vertical")
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

                b2 = MDBoxLayout(spacing="5sp")
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
                    if not data["data"]["bot"]["active"]:
                        data["data"]["bot"]["active"] = True
                        obj.secondary_text = "Активен"
                    elif data["data"]["bot"]["active"]:
                        data["data"]["bot"]["active"] = False
                        obj.secondary_text = "Неактивен"
            elif name in self.store_items and self.store_items[name]["type"] == "video card" or self.store_items[name][
                "type"] == "processor":
                if name in data["data"]["inventory"]:
                    f = FloatLayout()
                    b = MDBoxLayout(orientation="vertical")
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
                else:
                    f = FloatLayout()
                    b = MDBoxLayout(orientation="vertical")

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
            elif name in self.store_items and self.store_items[name]["type"] == "mouse":

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
                        text=f'Скорость: {"{0:.7f}".format(data["data"]["inventory"][name]["boost"])}[color=2dbb54] + {"{0:.7f}".format(data["data"]["inventory"][name]["boost"] * .3)} TON/клик[/color]',
                        halign="center",
                        # color=(0, 0, 0, 1),
                        font_name="main_font.ttf",
                        font_size="25sp",
                        markup=True,
                    )
                    b.add_widget(self.mouse_speed)
                    self.mouse_tired = CustomLabel(
                        text=f'Склонность к усталости: {int(data["data"]["inventory"][name]["tired"] * 100)}%[color=ff0000] - 2%[/color]',
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
                data["data"]["chest"].setdefault("last_opened", datetime.datetime.now().isoformat()))
            if now - last_opened > datetime.timedelta(hours=24):

                b2 = MDBoxLayout(orientation="vertical", spacing="5sp")
                b2.add_widget(CustomLabel(text=f'У вас есть 1 бесплатный сундук',
                                          halign="center",
                                          pos_hint={"center_x": .5},
                                          font_name="main_font.ttf",
                                          font_size="25sp",

                                          # theme_text_color="Custom",
                                          # color=(0, 0, 0, 1),
                                          )
                              )
                b1 = MDBoxLayout(
                    # orientation="vertical",
                    # size_hint_x=.5,
                    # pos_hint={"center_x": .5},
                    # md_bg_color=(1,0,0,1),
                    # padding=20,

                    spacing="2sp"
                )
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
                                          size_hint=(.9, .7), background="dialog.png")
                b1.bind(on_release=lambda a: self.chest_dialog.dismiss())

                self.chest_dialog.open()
            else:
                t = last_opened + datetime.timedelta(hours=12) - now
                hours = t.seconds // 3600
                minutes = t.seconds % 3600 // 60
                # m

                show_dialog(title="Открыть сундук", text=f"Следуюший сундук через {hours} часа(ов) {minutes} минут(ы).")
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

        video = data["data"]["bot"]["video card"]
        index = data["data"]["inventory"][name]["index"]
        price = data["data"]["inventory"][name]["price"]
        type_item = data["data"]["inventory"][name]["type"]

        # if index < self.store_items[name]["index"]:
        if data["data"]["TON"] - price >= 0:
            # print(type_item)
            data["data"]["TON"] -= price

            if type_item == "mouse":
                data["data"]["inventory"][name]["price"] += data["data"]["inventory"][name]["price"] * 30
                data["data"]["inventory"][name]["boost"] += data["data"]["inventory"][name]["boost"] * .3
                data["data"]["inventory"][name]["tired"] -= data["data"]["inventory"][name]["tired"] * .02
                data["data"]["mouse"] = name
                self.mouse_price.text = f'Цена: {"{0:.6f}".format(data["data"]["inventory"][name]["price"])}'
                self.mouse_tired.text = f'Склонность к усталости: {int(data["data"]["inventory"][name]["tired"] * 100)}% - 2%'
                self.mouse_speed.text = f'Скорость: {"{0:.6f}".format(data["data"]["inventory"][name]["boost"])} + {"{0:.6f}".format(data["data"]["inventory"][name]["boost"] * .3)} TON/клик'
            elif type_item == "video card":
                # print("23456")
                data["data"]["inventory"][name]["price"] += data["data"]["inventory"][name]["price"] * 30
                data["data"]["inventory"][name]["boost"] += data["data"]["inventory"][name]["boost"] * .3

                data["data"]["bot"]["video card"] = name
                self.video_card_price.text = f'Цена: {"{0:.6f}".format(data["data"]["inventory"][name]["price"])} TON'
                self.video_card_speed.text = f'Скорость: {"{0:.6f}".format(data["data"]["inventory"][name]["boost"])} + {"{0:.8f}".format(data["data"]["inventory"][name]["boost"] * .3)} TON/сек'
            # data["data"]["inventory"][name]["price"] += data["data"]["inventory"][name]["price"] * 300
            # obj.secondary_text = f'Цена: {"{0:.6f}".format(data["data"]["inventory"][name]["price"])} TON'
            obj.secondary_text = f'''Цена: {'{0:.6f}'.format(data["data"]["inventory"][name]["price"])} TON'''
        elif data["data"]["TON"] - price <= 0:
            Snackbar(text="У вас не хватает на это TON!", duration=.4).open()

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
                    # print(self.ids["bot_shop"].ids)
                    self.ids["mining_shop"].ids[f"choose_current_{name}"].opacity = 1
                    self.ids["mining_shop"].ids[f"choose_current_{name}"].active = True
                    self.ids["mining_shop"].ids[f"choose_current_{name}"].disabled = False
                    Snackbar(text=f"Выбрана мышка {name}", duration=.1).open()
                    # for key, obj in self.ids["bot_shop"].ids.items():
                    #     if obj.name not in data['data']["inventory"]:
                    #
                    #         self.ids["bot_shop"].ids[key].opacity = 0
                    #     else:
                    #         self.ids["bot_shop"].ids[key].opacity = 1
                    # for key, obj in self.ids["mining_shop"].ids.items():
                    #     if obj.name not in data['data']["inventory"]:
                    #         self.ids["mining_shop"].ids[key].opacity = 0
                    #     else:
                    #         self.ids["mining_shop"].ids[key].opacity = 1
                    data["data"]["mouse"] = name
                elif type_item == "video card":
                    self.ids["bot_shop"].ids[f"choose_current_{name}"].opacity = 1
                    self.ids["bot_shop"].ids[f"choose_current_{name}"].active = True
                    self.ids["bot_shop"].ids[f"choose_current_{name}"].disabled = False
                    data["data"]["bot"]["video card"] = name
                    Snackbar(text=f"Выбрана видеокарта {name}", duration=.1).open()
                data["data"]["inventory"][name] = self.store_items[name]
                data["data"]["inventory"][name]["price"] += data["data"]["inventory"][name]["price"] * 30
                obj.secondary_text = f'Цена: {"{0:.6f}".format(data["data"]["inventory"][name]["price"])} TON'

            elif data["data"]["TON"] - price <= 0:
                Snackbar(text="У вас не хватает на это TON!", duration=.4).open()

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
        #             Snackbar(text="У вас не хватает на это валюты!",duration=.2)
        #     elif index > self.mouses[name]["index"]:
        #         Snackbar(text="Эта мышь хуже, чем у вас есть!",duration=.2)
        #     elif index == self.mouses[name]["index"]:
        #         Snackbar(text="У вас уже усть эта мышь!",duration=.2)
        elif name == "token":
            if data["data"]["TON"] - data["data"]["token"]["price"] >= 0:
                data["data"]["TON"] -= data["data"]["token"]["price"]
                # data["data"]["token"]["price"] += data["data"]["token"]["price"] / 100 * 20
                data["data"]["token"]["value"] += 1

            else:
                # self.dialog.dismiss()f
                Snackbar(text="У вас не хватает на это TON!", duration=.4).open()

        elif name == "chest":
            # self.ads.show_rewarded_ad()
            if data["data"]["TON"] - data["data"]["chest"]["price"] >= 0:

                # data["data"]["chest"]["price"] += data["data"]["chest"]["price"] / 100 * 20

                # else:
                self.open_chest(is_bought=True)

            else:
                # self.dialog.dismiss()
                Snackbar(text="У вас не хватает на это TON!", duration=.4).open()

        elif name == "удвоение майнинга":
            if data["data"]["TON"] - self.doubling_data["price"] >= 0:
                self.doubling_data["value"] += self.doubling_data["value"] / 100 * 50

                data["data"]["TON"] -= self.doubling_data["price"]
                self.doubling_data["price"] += self.doubling_data["price"] / 100 * 50

            else:
                Snackbar(text="У вас не хватает на это TON!", duration=.4).open()
        elif name == "суммирование майнинга":
            if data["data"]["TON"] - self.summation_data["price"] >= 0:
                data["data"]["TON"] -= self.summation_data["price"]

                self.summation_data["value"] += 0.000001

                self.summation_data["price"] += 0.000001 * 100
            else:
                Snackbar(text="У вас не хватает на это TON!", duration=.4).open()
        elif name == "прокачка майнинга бота":
            if data["data"]["TON"] - data["data"]["bot"]["summation_price"] >= 0:
                data["data"]["TON"] -= data["data"]["bot"]["summation_price"]

                data["data"]["bot"]["summation_num"] += 0.000001

                data["data"]["bot"]["summation_price"] += 0.000001 * 100
            else:
                Snackbar(text="У вас не хватает на это TON!", duration=.4).open()
        elif name == "автомайнер":
            if data["data"]["TON"] - data["data"]["bot"]["price"] >= 0:
                data["data"]["TON"] -= data["data"]["bot"]["price"]
                data["data"]["bot"]["alow_bot"] = True
                obj.secondary_text = "Активен"



            else:
                Snackbar(text="У вас не хватает на это TON!", duration=.4).open()
        # self.ui_update()

    def show_value(self):
        b = self.ids['bet_value'].value

        # m = data["data"]["TON"] - s

        w = data["data"]["TON"] / 100 * b
        self.ids['value_bet_text'].text = f"Ваша ставка: {'{0:.6f}'.format(w)} TON"

    def show_info(self):
        if data["data"]["bot"]["active"]:
            alow_bot = "Активен"
        else:
            alow_bot = "Неактивен"
        if not data["data"]["bot"]["active"]:
            alow_bot = "Не куплен"
        show_dialog(title="Информация", text=f'''
Клик: {'{0:.6f}'.format(data["data"]["inventory"][data["data"]["mouse"]]["boost"])} TON
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

    def update_data(self):
        # print(data["data"])
        global offline, data, version
        # print(self.cur_nav)
        # print(data["account"]["login"])
        # print('{0:.6f}'.format(data["data"]["TON"])
        # )

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
                    version = 100000

                if data["account"]["name"] and auth_succefull:

                    # ref = db.reference(f"/players/{data['account']['name']}/data/TON")
                    # ton = ref.get()
                    # print('{0:.6f}'.format(ton))
                    ref = db.reference(f"/players/{data['account']['name']}/account/privilege")
                    priv = ref.get()
                    # print(priv)
                    if priv == data["account"]["privilege"]:
                        ref = db.reference(f"/players/{data['account']['name']}")
                        ref.set(data)

                    # elif ton > data["data"]["TON"]:

                    elif priv != None and priv != data["account"]["privilege"]:
                        data["account"]["privilege"] = priv
                        show_dialog(title="Внимание!", text=f"Ваша привилегия теперь {priv}!")
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
                            show_dialog(title="Внимание!",
                                        text=f'Игрок {name} перевёл вам {"{0:.6f}".format(ton)} TON.')
                            data["data"]["TON"] += ton
                            ref = db.reference(f"/transfers/{data['account']['name']}/{key}")
                            # print(key)
                            ref.delete()
                    ref = db.reference(f"/players/{data['account']['name']}/account/ban/is_banned")

                    if ref.get() == "True":
                        data = no_data
                        self.game.show_alert_dialog(title="Вы забанены!", text=f'''
Вы забанены по пречине: {ref.get("cause")}.
Обратитесь за помошью в дискорд сервер.
Приятной игры!
                                        ''')

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
            size_hint=(.3, None),
        )
        b2.add_widget(c2)
        c = MDFillRoundFlatButton(
            text="Перевести",
            font_size="20sp",
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
            if p != False and p != None and p < max_ping:
                ton.error = False
                name.error = False

                ref = db.reference(f"/players/{name.text}")
                g = ref.get()
                try:
                    if data["data"]["TON"] - float(ton.text) >= 0 and float(ton.text) != 0:
                        if g and name.text != data["account"]["name"]:
                            data["data"]["TON"] -= float(ton.text)
                            ref = db.reference(f"/transfers/{name.text}")
                            # g = 0
                            # g +=
                            ref.push({"name": data["account"]["name"], "TON": float(ton.text)})

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
                                # halign="center",
                                pos_hint={"center_x": .5},
                                size_hint=(.3, None),
                                on_press=lambda a: self.pay_dialog.dismiss(),
                            )
                            b.add_widget(c2)
                            self.pay_dialog.content = b
                            # self.pay_dialog.dismiss()
                        else:
                            name.error = True
                    else:
                        ton.error = True

                except ValueError:
                    ton.error = True
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
        mouse = data["data"]["mouse"]

        if data["data"]["tired_num"] - float(Decimal(f'{data["data"]["inventory"][mouse]["tired"]}')) >= 0:

            data["data"]["TON"] += data["data"]["inventory"][mouse]["boost"]

            if self.current_effect["name"] == "disable_tired":
                data["data"]["tired_num"] -= self.current_effect["lvl"] / self.current_effect["lvl"] ** 3
            else:
                data["data"]["tired_num"] -= float(Decimal(f'{data["data"]["inventory"][mouse]["tired"]}'))
        else:
            old_color_icon = (1, .8, 0, 1)
            if self.ids["tired_num"].color != (1, 0, 0, 1):
                self.ids["tired_icon"].color = (1, 0, 0, 1)
                self.ids["tired_num"].color = (1, 0, 0, 1)
            timer(self.start_animation, .5)
            self.ads.show_interstitial()
        # data["data"]["is_tired"] = True
        # print(App.get_running_app().root.ids['hi'])

    def start_animation(self):
        self.ids["tired_num"].color = (1, .8, 0, 1)
        oc = self.ids["tired_icon"].color
        self.ids["tired_icon"].color = (1, .8, 0, 1)


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
        global offline, data, cur_nav, auth_succefull
        auth_succefull = False
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")

        print(p)

        # if p != False and p != None and p < max_ping:
        # auth_succefull = False
        data = no_data
        # os.remove("avatar.png")
        os.remove("data.pickle")
        # set_data()
        self.ids[cur_nav].set_state()
        cur_nav = "nav_drawer2"
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
        self.ids[cur_nav].set_state("open")

    def main_loop(self, dt):
        global auth_succefull
        # if auth_succefull:
        #     pass
        th = Thread(target=self.ui_update)
        th.start()
        # self.ui_update()

    def ui_update(self):

        # self.ids["tokens_num_games"].text = f'''Жетоны: {data["data"]["token"]["value"]}'''
        if data["data"]["bot"]["alow_bot"]:
            if data["data"]["bot"]["active"]:
                self.ids["autominer"].secondary_text = "Активен"

            else:
                self.ids["autominer"].secondary_text = "Неактивен"

        self.ids["ton_num_shop"].text = f'''TON: {'{0:.6f}'.format(data["data"]["TON"])}'''
        self.ids["ton_num_games"].text = f'''TON: {'{0:.6f}'.format(data["data"]["TON"])}'''
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
        # self.ids["token_price"].text = f'''Цена: {'{0:.6f}'.format(data["data"]["token"]["price"])} TON'''

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

    def to_auth(self):
        self.ids[cur_nav].set_state()
        self.ads.show_interstitial()
        self.manager.current = "auth"

    def miner_loop(self, dt):
        global auth_succefull
        # if auth_succefull:

        if auth_succefull:
            th = Thread(target=self.autominer)
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

    def delete_account_confirm(self):
        show_dialog(title="Удалить?", text="Этот аккаунт удалится безвозвратно!", exit=True,
                    command=self.delete_account)

    def delete_account(self):
        name = data['account']['name']
        self.sign_out()
        ref = db.reference(f"/players/{name}")
        ref.delete()

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
                        # self.main_dialog.dismiss()

                        show_dialog(title="Поздравляем!", text=f"Вам выпала видеокарта {bonuse}!")
                    elif item["type"] == "mouse" and item["index"] >= self.mouses[data['data']["mouse"]]["index"]:
                        data['data']["mouse"] = bonuse
                        data["data"]["inventory"][bonuse] = self.store_items[bonuse]
                        # self.main_dialog.dismiss()

                        show_dialog(title="Поздравляем!", text=f"Вам выпала мышь {bonuse}!")
                    else:

                        r = random.randint(30, 100)
                        r /= 100
                        data['data']["TON"] += data['data']["TON"] * r
                        # self.main_dialog.dismiss()
                        show_dialog(title="Поздравляем!",
                                    text=f"Вам выпало {'{0:.6f}'.format(data['data']['TON'] * r)} TON!")
                    self.chest_dialog.dismiss()
                    break
        else:

            r = random.randint(30, 100)
            r /= 100
            data['data']["TON"] += data['data']["TON"] * r
            self.chest_dialog.dismiss()
            show_dialog(title="Поздравляем!",
                        text=f"Вам выпало {'{0:.6f}'.format(data['data']['TON'] * r)} TON!")
        if is_bought:
            data["data"]["TON"] -= data["data"]["chest"]["price"]
            data["data"]["chest"]["price"] += data["data"]["chest"]["price"] * 0.2
        else:
            now = datetime.datetime.now()
            data["data"]["chest"]["last_opened"] = now.isoformat()
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
        #                 show_dialog(title="Поздравляем!", text=f"Вам выпала видеокарта {bonuse}")
        #             elif item["type"] == "mouse" and item["index"] >= self.mouses[data['data']["mouse"]]["index"]:
        #                 data['data']["mouse"] = bonuse
        #                 show_dialog(title="Поздравляем!", text=f"Вам выпала мышь {bonuse}")
        #             data['data']["chest_last_opened"] = datetime.now()
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
        loading = Loading(name="loading")

        # self.screen_manager.add_widget(Navigate_without_account(name="scr"))
        self.screen_manager.add_widget(loading)
        # Logger.info('Loader: Spinner screen has been loaded.')
        self.screen_manager.current = "loading"
        # template = GameTemplate(name="template")
        # self.screen_manager.add_widget(template)
        # print(123)

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
        self.game = Clicker(name="clicker")
        #
        # self.screen_manager.add_widget(self.game)

        # Clock.schedule_interval(self.game.miner_loop, 1)
        Clock.schedule_interval(self.game.main_loop, 1 / 10)
        Clock.schedule_interval(self.game.tired_loop, 1)
        #
        # # self.load_store_items()
        self.screen_manager.add_widget(self.game)
        print("--- %s seconds ---" % (time.time() - start_time))
        # print(list(self.game.store_items))
        # self.lsi = Clock.schedule_interval(self.load_store_items, 1/60)
        # import time
        # start_time = time.time()
        # print(list(self.game.store_items))

        # print(list(self.game.store_items))
        #
        cred_obj = firebase_admin.credentials.Certificate(
            'ton-clicker-firebase-adminsdk-cf1xz-8ad3090323.json')
        app_d = firebase_admin.initialize_app(cred_obj, {
            'databaseURL': "https://ton-clicker-default-rtdb.firebaseio.com/"
        })

        import time
        start_time = time.time()
        # self.start_game()
        # self.load_store_items()
        th = Thread(target=self.load_store_items)
        th.start()

        # self.load_store_items()
        # self.fps_monitor_start()
        # self.load_music()

        # Thread(target=self.load_music).start()
        # self.load_music()
        # print("--- %s seconds ---" % (time.time() - start_time))
        return self.screen_manager

    def load_music(self):
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
        # start_time = time.time()
        # import time
        # start_time = time.time()

        # print("--- %s seconds ---" % (time.time() - start_time))
        # print("--- %s seconds ---" % (time.time() - start_time))
        self.start_game()

        async def ls(bot_shop, mining_shop):

            sleep = asynckivy.sleep
            await sleep(0)

            for i in self.game.store_items:

                name = self.game.store_items[i]["name"]
                price = self.game.store_items[i]["price"]
                # index = self.game.store_items[i]["index"]
                type_item = self.game.store_items[i]["type"]
                texture = self.game.store_items[i]["texture"]
                # print(i, data["data"]["inventory"])
                if i in data["data"]["inventory"]:
                    # print(i)
                    # boost = self.game.store_items[i]["boost"]
                    price = data["data"]["inventory"][i]["price"]
                    # index = self.game.store_items[i]["index"]
                    type_item = data["data"]["inventory"][i]["type"]
                    texture = data["data"]["inventory"][i]["texture"]

                # print(texture)

                # print("list loading")
                start_time = time.time()
                # self.start_game()
                # self.screen_manager.current = "clicker"
                # print("--- %s seconds ---" % (time.time() - start_time))
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

                    if name == data["data"]["bot"]["video card"]:
                        check = Check(group="current_video card", radio_icon_down="check-circle",
                                      radio_icon_normal="check-circle", active=True, on_press=self.game.current_item)
                    else:
                        # if name == data["data"]["mouse"]:
                        check = Check(group="current_video card", radio_icon_down="check-circle",
                                      radio_icon_normal="check-circle", on_press=self.game.current_item)
                    if i in data["data"]["inventory"]:
                        check.opacity = 1

                    else:
                        check.opacity = 0
                        check.disabled = True
                    check.name = name
                    line.add_widget(check)
                    bot_shop.ids[f"choose_current_{name}"] = check
                    bot_shop.add_widget(line)

                elif type_item == "mouse":
                    if name == data["data"]["mouse"]:
                        check = Check(group="current_mouse", radio_icon_down="check-circle",
                                      radio_icon_normal="check-circle", active=True, on_press=self.game.current_item)
                    else:
                        # if name == data["data"]["mouse"]:
                        check = Check(group="current_mouse", radio_icon_down="check-circle",
                                      radio_icon_normal="check-circle", on_press=self.game.current_item)
                    if i in data["data"]["inventory"]:
                        check.opacity = 1
                    else:
                        check.opacity = 0
                        check.disabled = True
                    check.name = name
                    line.add_widget(check)
                    mining_shop.ids[f"choose_current_{name}"] = check
                    mining_shop.add_widget(line)
            self.screen_manager.current = "clicker"
            # self.load_music()

        asynckivy.start(ls(self.game.ids["bot_shop"], self.game.ids["mining_shop"]))
        timer(lambda: self.game.bot_state("off"), 30 * 60)
        self.background_loop_state = True
        while self.background_loop_state:
            time.sleep(1)
            if data["data"]["bot"]["active"]:
                self.game.miner_loop(dt=1)
            if auth_succefull:
                th = Thread(target=self.game.update_data)
                th.start()

    # @cache
    #    def ls(self, i):
    # time.sleep(1)

    def start_game(self):
        global data, auth_succefull, cur_nav

        try:
            with open("data.pickle", "rb") as f:
                data = pickle.load(f)
                check_lost_keys()
                Logger.info('INFO: Account detected')
        except:
            no_data["data"]["inventory"] = {"Oklick 105S": self.game.store_items["Oklick 105S"],
                                            "Celeron Pro": self.game.store_items["Celeron Pro"]}
            data = no_data
            Logger.info('INFO: No account')

        auth_succefull = True

        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")

        try:
            if p != False and p != None and p < max_ping:

                ref = db.reference(f"/lock_app")
                d = ref.get()
                if d == "True":
                    raise BaseException("It is Star Wormwood inc. project!")
        except:
            pass
        # set_data()

        if data["account"]["name"]:
            cur_nav = "nav_drawer1"
        else:
            cur_nav = "nav_drawer2"
        # self.screen_manager.current = "clicker"


# Запуск проекта
if __name__ == "__main__":
    app().run()

up_data = False
