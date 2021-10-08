from kivy.config import Config

Config.set('graphics', 'width', '850')
Config.set('graphics', 'height', '530')
Config.set('graphics', 'minimum_width', '850')
Config.set('graphics', 'minimum_height', '530')
from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivymd.uix.tab import MDTabsBase
from kivymd.app import MDApp


class SettingsTab(MDCard, MDTabsBase):
    pass

class bbar(MDApp):

    def __init__(self, **kwargs):
        super(bbar, self).__init__(**kwargs)
        self.kv = Builder.load_file("bbar.kv")

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Teal"
        return self.kv


if __name__ == '__main__':
    bbar().run()