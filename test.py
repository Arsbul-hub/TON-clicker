

from kivy.uix.screenmanager import *

from kivy.clock import Clock

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.audio import SoundLoader

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
from kivy.logger import Logger
from kivy.uix.screenmanager import NoTransition
from kivymd.uix.list import TwoLineIconListItem

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
class app(MDApp):


    def build(self):
        b = BoxLayout()
        for i in range(5):
            b.add_widget(Image(source="blue.png"))
        return b



# Запуск проекта
if __name__ == "__main__":
    app().run()

