import os
import ast
import time

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from db import DataBase
import common
import global_vars

db = DataBase()
global_vars.db = db


from filtred_list_screen import FiltredListScreen
from add_screen import AddItem
from main_screen import MainScreen
from view_item import ViewItem

sm = ScreenManager()
common.sm = sm
sm.add_widget(MainScreen(name='main'))
sm.add_widget(FiltredListScreen(name='list'))
sm.add_widget(AddItem(name='add_item'))
sm.add_widget(ViewItem(name='view_item'))


class MyApp(App):
    def __init__(self, **kvargs):
        super(MyApp, self).__init__(**kvargs)

    def build(self):
        return sm


if __name__ == '__main__':
    MyApp().run()
