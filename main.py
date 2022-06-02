
from kivy.base import EventLoop

from kivymd.uix.list import IconLeftWidget
from kivy.uix.screenmanager import *

from kivy.core.audio import SoundLoader

from kivymd.app import MDApp


main_font_size = 20

from kivy.logger import Logger

from kivy.config import Config
from MainScreen import *
from LoadingScreen import *
from AutScreen import *
from Account_info import *

if plyer.utils.platform == "win":
    Config.set('graphics', 'width', '562')
    Config.set('graphics', 'height', '995')
    Config.set('graphics', 'resizable', False)
    Config.write()



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
        # data = Account
        self.screen_manager.add_widget(auth)
        account_info = Account_info(name="account_info")
        # data = Account
        self.screen_manager.add_widget(account_info)
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
                    line = ShopItem(

                        text=f"[color=e3680a]{name}[/color]",

                        # source="",
                        secondary_text=f"[color=e3680a]Можно найти в сундуке[/color]",
                        icon=texture,
                        # font_style="Custom",
                        # font_name="main_font.ttf",
                        # font_style="Subtitle1",
                        # type=type_card,
                        on_press=self.game.buy_confirm
                    )
                else:
                    line = ShopItem(

                        text=name,

                        # source="",
                        secondary_text=f"Цена: {'{0:.6f}'.format(price)} TON",
                        icon=texture,
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
                # line.add_widget(image)

                # self.game.ids["bot_shop"].add_widget(MDLabel(text="hi"))
                if type_item == "video card" or type_item == "processor":

                    if name == Account.data["data"]["bot"]["video card"]:
                        check = Check(group="current_video card", radio_icon_down="check-circle", pos_hint={"right": 1},
                                      radio_icon_normal="check-circle", active=True, on_press=self.game.current_item)

                    else:
                        # if name == Account.data["data"]["mouse"]:
                        check = Check(group="current_video card", radio_icon_down="check-circle", pos_hint={"right": 1},
                                      radio_icon_normal="check-circle", on_press=self.game.current_item)
                    if name in Account.data["data"]["inventory"]:
                        check.opacity = 1

                    else:
                        check.opacity = 0
                        check.disabled = True
                    check.name = name

                    # line.add_widget(check)
                    # print(name)
                    line.ids["check"].add_widget(check)
                    self.game.ids["bot_shop"].ids[f"choose_current_{name}"] = check
                    self.game.ids["bot_shop"].ids[name] = line
                    self.game.ids["bot_shop"].add_widget(line)

                elif type_item == "mouse":
                    if name == Account.data["data"]["mouse"]:
                        check = Check(group="current_mouse", radio_icon_down="check-circle", pos_hint={"right": 1},
                                      radio_icon_normal="check-circle", active=True, on_press=self.game.current_item)
                    else:
                        # if name == Account.data["data"]["mouse"]:
                        check = Check(group="current_mouse", radio_icon_down="check-circle", pos_hint={"right": 1},
                                      radio_icon_normal="check-circle", on_press=self.game.current_item)
                    if name in Account.data["data"]["inventory"]:
                        check.opacity = 1
                    else:
                        check.opacity = 0
                        check.disabled = True
                    check.name = name
                    # line.add_widget(check)
                    line.ids["check"].add_widget(check)
                    self.game.ids["mining_shop"].ids[f"choose_current_{name}"] = check
                    self.game.ids["mining_shop"].ids[name] = line
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
            th = Thread(target=player.update_data)
            th.start()
            now = datetime.datetime.now()
            last_opened = datetime.datetime.fromisoformat(
                Account.data["data"]["chest"].setdefault("last_opened", datetime.datetime.now().isoformat()))
            # print(now - last_opened > datetime.timedelta(hours=24))

            if now - last_opened > datetime.timedelta(hours=24):
                if plyer.utils.platform == "win":
                    Clock.schedule_once(
                        lambda a: show_notify(title="TON кликер",
                                              message="Вы снова вы можете открыть сундук!",
                                              app_icon="images/chest_normal.ico", name="open_chest_info"))
                else:
                    Clock.schedule_once(
                        lambda a: show_notify(title="TON кликер",
                                              message="Вы снова вы можете открыть сундук!",
                                              app_icon="images/blue.png", name="open_chest_info"))

        # ak.start(background_loop(e))

    # @cache
    #    def ls(self, i):
    # time.sleep(1)

    def start_game(self):
        global data, auth_succefull, cur_nav
        no_data["data"]["inventory"] = {"Oklick 105S": store_items["Oklick 105S"],
                                        "Celeron Pro": store_items["Celeron Pro"]}
        data = Account.data
        try:
            with open("data.pickle", "rb") as f:
                Account.data = pickle.load(f)
                # check_lost_keys()

                # print(data)
                Logger.info('INFO: Account detected')
                # print(Account.data)


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
