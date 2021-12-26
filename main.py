

from kivy.uix.screenmanager import *

from kivy.clock import Clock

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


import pickle

from kivymd.uix.card import MDCard
from kivymd.uix.tab import MDTabsBase

from kivymd.uix.snackbar import Snackbar
from kivymd.app import MDApp
main_font_size = 20
import os
import firebase_admin
from firebase_admin import db
import random
from ping3 import ping
from threading import Thread

from kivy.uix.screenmanager import NoTransition

up_data = True
auth_succefull = False
offline = False
already_auth = False
data = {}
max_ping = 300


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
                self.manager.current = "clicker"
            except:

                self.manager.current = "auth"


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

    def load_avatar(self, p):
        self.ids["avatar_image"].source = p

    def login(self):
        #self.manager.current = "loading"
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

                self.game = Clicker
                # self.game.test()
                # print(123)

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
        #self.manager.current = "loading"
        th = Thread(target=self.start_login)
        th.start()
    def start_registration(self):
        global data
        if self.ids["avatar"].text:
            avatar = self.ids["avatar"].text
        else:
            avatar = "https://i.ibb.co/zr8HtNr/classic-avatar.png"
        player_name = self.ids["name_r"].text
        player_email = self.ids["email_r"].text
        player_password = self.ids["password_r"].text
        if player_password != "" and player_email != "" and player_name != "":
            ref = db.reference(f"/players/{player_email}")
            account = ref.get()

            if account == None:

                data = {
                    "account": {"name": player_name,
                                "login": player_email,
                                "password": player_password,
                                "avatar": avatar, },
                    "data": {"TON": 0, "doubling": 1, "doubling_price": 0.001,
                             "bot": {"alow_bot": False, "doubling": 1, "doubling_price": 0.001,
                                     "video card": "Celeron Pro", "bot_price": 1,
                                     "summation_price": 0.000001, "summation_num": 0.000001},

                             "summation": {"summation_price": 0.000001, "summation_num": 0.000001}
                             }
                }

                # p = ping('ton-clicker-default-rtdb.firebaseio.com', unit="ms")

                ref = db.reference(f"/players/{player_email}")
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
        global auth_succefull, offline, data

        # c = Clicker()
        # c.set_data()
        auth_succefull = True
        with open("data.pickle", "wb") as f:
            pickle.dump(data, f)
        c = Clicker

        c.account = data["account"]
        c.player_data = data["data"]
        c.bot_data = data["data"]["bot"]
        c.summation_data = data["data"]["summation"]
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
        self.videocards = {
            "Celeron Pro": {"index": 0, "name": "Celeron Pro", "type_card": "processor", "boost": 0.000001,
                            "price": 0.10},
            "Gt 770": {"index": 1, "name": "Gt 770", "type_card": "video card", "boost": 0.00002, "price": 0.50},
            "Gt 870": {"index": 2, "name": "Gt 870", "type_card": "video card", "boost": 0.00003, "price": 0.70},
            "Gtx 970": {"index": 3, "name": "Gtx 970", "type_card": "video card", "boost": 0.00004, "price": 0.90},
            "Rtx 1050": {"index": 4, "name": "Rtx 1050", "type_card": "video card", "boost": 0.00005, "price": 1},
            "Rtx 1070": {"index": 5, "name": "Rtx 1070", "type_card": "video card", "boost": 0.00006, "price": 1.5},
            "Rtx 2060": {"index": 6, "name": "Rtx 2060", "type_card": "video card", "boost": 0.00007, "price": 1.9},
            "Rtx 2070 Super": {"index": 7, "name": "Rtx 2070 Super", "type_card": "video card", "boost": 0.00008,"price": 2.1},
            "Rtx 2080 TI": {"index": 8, "name": "Rtx 2080 TI", "type_card": "video card", "boost": 0.00009,"price": 2.6},
            "Rtx 3060 Super": {"index": 9, "name": "Rtx 3060 Super", "type_card": "video card", "boost": 0.0015,"price": 3.0},
            "Rtx 3090 Super TI": {"index": 10, "name": "Rtx 3090 Super TI", "type_card": "video card", "boost": 0.0095,"price": 3.8},
            "Rtx 8000 Super TI Extreme Edition": {"index": 11, "name": "Rtx 8000 Super TI Extreme Edition","type_card": "video card", "boost": 1.2, "price": 4.5}
        }
        self.n = 0

    # def set_data(self):
    #     global auth_succefull
    #     self.account = data["account"]
    #     self.player_data = data["data"]
    #     self.bot_data = data["data"]["bot"]
    #     self.summation_data = data["data"]["summation"]
    def buy_confirm(self, name):
        self.dialog = None

        if not self.dialog:
            self.dialog = MDDialog(
                title="Покупка",
                text=f'''
Вы действительно хотите купить {name}?                
''',

                buttons=[
                    MDFlatButton(
                        text="Отмена",
                        theme_text_color="Custom",
                        # text_font_name= "main_font.ttf",
                        text_color=(0, 0, 0, 1),
                        font_size="20sp",
                        font_name="main_font.ttf",
                        # text_color=self.theme_cls.primary_color,
                        on_press=lambda event: self.close_dialog()
                    ),
                    MDFlatButton(
                        text="Ок",
                        theme_text_color="Custom",
                        # text_font_name= "main_font.ttf",
                        text_color=(0, 0, 0, 1),
                        font_size="20sp",
                        font_name="main_font.ttf",
                        # text_color=self.theme_cls.primary_color,
                        on_press=lambda x: self.buy(name=name)
                    ),
                ],
            )
        self.dialog.open()

    def buy(self, name):
        self.dialog.dismiss()
        print(self.bot_data)
        video = self.bot_data["video card"]
        index = self.videocards[video]["index"]
        name_video = self.videocards[video]["name"]
        boost = self.videocards[video]["boost"]
        price = self.videocards[video]["price"]
        type_card = self.videocards[video]["type_card"]

        if name in self.videocards:
            if index < self.videocards[name]["index"]:
                if self.player_data["TON"] - price >= 0 and video != name:

                    self.player_data["TON"] -= price
                    self.bot_data["video card"] = name
                elif self.player_data["TON"] - price <= 0:
                    Snackbar(text="У вас не хватает на это средств!").open()
            elif index > self.videocards[name]["index"]:
                Snackbar(text="Эта видеокарта хуже, чем у вас есть!").open()
            elif index == self.videocards[name]["index"]:
                Snackbar(text="У вас уже усть ета видеокарта!").open()
        else:
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

        self.show_alert_dialog(title="Информация о майнинге", text=f'''
Клик: {'{0:.6f}'.format(self.summation_data["summation_num"])} TON
Удвоение майнинга: x{self.player_data["doubling"]}
Бот: {self.bot_data["alow_bot"]}
Текущая видеокарта: {self.bot_data["video card"]}
Майнинг автомайнера: {'{0:.6f}'.format(self.videocards[self.bot_data["video card"]]["boost"])} TON в секунду
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

        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
        #print(p)
        if p != False and p != None and p < max_ping:
            ref = db.reference(f"/players/{self.account['login']}")
            ref.set({"account": self.account, "data": self.player_data})
            # offline = False
        #    self.settings = pickle.load(f)
        #    self.main_font_size = self.settings["font_size"]
        else:

            if offline == False:
                self.manager.current = "error_show"
                offline = True

    def on_tap(self):
        # print('{0:.6f}'.format(self.player_data["TON"]))
        self.player_data["TON"] += self.summation_data["summation_num"] * self.player_data["doubling"]
        # print(App.get_running_app().root.ids['hi'])

    def sign_out(self):
        # print(self.manager.current)
        global offline, auth_succefull
        self.ids["loading"].active = True
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
        self.ids["loading"].active = False
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
        if auth_succefull:

            self.ids["player_name"].text = f'''Имя: {self.account["name"]}'''
            self.ids["player_login"].text = f'''Логин: {self.account["login"]}'''
            self.ids["avatar"].source = self.account["avatar"]
            # print(self.account)
            self.ids[
                'text_doubling'].secondary_text = f'''Цена: {'{0:.6f}'.format(self.player_data["doubling_price"])} TON'''
            # Удвоение майнинга с:{self.player_data["doubling"] } на 30%
            self.ids['TON_num'].text = '{0:.6f}'.format(self.player_data["TON"])
            self.ids[
                'text_summation'].secondary_text = f'''цена: {'{0:.6f}'.format(self.summation_data["summation_price"])} TON'''
            # self.ids['video_shop'].secondary_text = f'''цена: {'{0:.6f}'.format(self.bot_data["doubling_price"])} TON'''
            # self.ids['text_bot_summation'].secondary_text = f'''цена: {self.bot_data["summation_price"]} TON'''
            #
            #             #App.get_running_app().root.ids['TON_num_natural'].text = f"точнее: {self.player_data['TON']}"
            #



    def miner_loop(self, dt):
        global auth_succefull
        if auth_succefull:
            th = Thread(target=self.autominer)
            th.start()
            th = Thread(target=self.update_data)
            th.start()
    def autominer(self):
        if self.bot_data["alow_bot"]:
            video = self.bot_data["video card"]

            name = self.videocards[video]["name"]
            boost = self.videocards[video]["boost"]
            price = self.videocards[video]["price"]
            type_card = self.videocards[video]["type_card"]

            self.player_data["TON"] += boost


class Loading(Screen):
    pass



class app(MDApp):
    def build(self):
        global auth_succefull, already_auth, data
        print(123)
        # Clock.schedule_interval(self.start_loops, 1/30)
        self.screen_manager = ScreenManager()
        self.screen_manager.transition = SwapTransition()
        d = Error_show(name="error_show")

        # d.folder_path = folder_path
        self.screen_manager.add_widget(d)
        self.game = Clicker(name="clicker")

        self.screen_manager.add_widget(self.game)
        Clock.schedule_interval(self.game.main_loop, 1 / 5)
        #Clock.schedule_interval(self.game.bot_loop, 1)
        Clock.schedule_interval(self.game.miner_loop, 1)

#        for i in self.game.videocards:
#            name = self.game.videocards[i]["name"]
#            boost = self.game.videocards[i]["boost"]
#            price = self.game.videocards[i]["price"]
#            type_card = self.game.videocards[i]["type_card"]
#            image = ImageLeftWidget(source=f"{type_card}.png")
#            line = ThreeLineAvatarListItem(
#
#                text=name,
#                # source="",
#
#                secondary_text=f"Цена: {price} TON",
#                tertiary_text=f"Добыча валюты: {'{0:.6f}'.format(boost)} TON в секунду",
#
#                on_press=lambda event: print(name)
#
#            )
#
#            line.add_widget(image)
#
#            self.game.ids["bot_shop"].add_widget(line)

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
        self.screen_manager.add_widget(d)
        auth = Auth(name="auth")
        self.screen_manager.add_widget(auth)
        loading = Loading(name="loading")
        self.screen_manager.add_widget(loading)

        self.screen_manager.current = "loading"

        # self.main_font_size = self.settings["font_size"]
        # self.title = "Tap-Fight"
        # self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "BlueGray"
        print(123)
        # Add the screens to the manager and then supply a name
        # that is used to switch screens

        # self.background_color=(1,0.1,0.1)
        return self.screen_manager



    def on_start(self):
        # d.folder_path = folder_path

        th = Thread(target=self.start_game)
        th.start()
        #self.fps_monitor_start()

    def start_game(self):
        global data,auth_succefull

        cred_obj = firebase_admin.credentials.Certificate('bl-test-671cd-firebase-adminsdk-7uep2-46a3a5832a.json')
        app_d = firebase_admin.initialize_app(cred_obj, {
            'databaseURL': "https://bl-test-671cd-default-rtdb.firebaseio.com/"
        })
        p = ping('ton-clicker-default-rtdb.firebaseio.com', timeout=1, unit="ms")
        # print(p == "False")

        if p != False and p != None and p < max_ping:

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

                    ref = db.reference(f"/players/{data['account']['login']}")
                    ref.set(data)

                auth_succefull = True
                c = Clicker

                c.account = data["account"]
                c.player_data = data["data"]
                c.bot_data = data["data"]["bot"]
                c.summation_data = data["data"]["summation"]
                self.screen_manager.current = "clicker"
            except:

                self.screen_manager.current = "auth"

        else:
            firebase_admin.delete_app(firebase_admin.get_app())
            cred_obj = firebase_admin.credentials.Certificate('ton-clicker-firebase-adminsdk-cf1xz-8ad3090323.json')
            app_d = firebase_admin.initialize_app(cred_obj, {
                'databaseURL': "https://ton-clicker-default-rtdb.firebaseio.com/"
            })
            self.screen_manager.current = "error_show"

# Запуск проекта
if __name__ == "__main__":
    app().run()
up_data = False
