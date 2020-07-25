from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from datetime import datetime

from common import set_screen
import global_vars as gv

# class MainScreen(Screen):
#     def __init__(self, **kw):
#         super(MainScreen, self).__init__(**kw)
#         box = BoxLayout(orientation='vertical')
#         box.add_widget(Button(text='Дневник питания', on_press=lambda x:
#                                 set_screen('list')))
#         box.add_widget(Button(text='Добавить блюдо в дневник питания',
#                               on_press=lambda x: set_screen('add')))
#         self.add_widget(box)

# TEMP
class MainScreen(Screen):
    def __init__(self, **kw):
        super(MainScreen, self).__init__(**kw)

        super(MainScreen, self).__init__(**kw)
        box = BoxLayout(orientation='vertical')


        self.items_grid = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=10)
        # Make sure the height is such that there is something to scroll.
        self.items_grid.bind(minimum_height=self.items_grid.setter('height'))
                
        scroll_view = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        scroll_view.add_widget(self.items_grid)

        box.add_widget(scroll_view)

        box.add_widget(Button(text='Добавить элемент;)',
                              on_press=lambda x: set_screen('add_item'),
                              size_hint_y=None, height=dp(80)))
        self.add_widget(box)

    def on_enter(self):  # Будет вызвана в момент открытия экрана

        all_items = gv.db.get_all_items()
        
        for (item_id, item_title, item_time_create) in all_items:
            wrapper = BoxLayout(size_hint_y=None, height=dp(40),)
            btn = Button(
                text=item_title,
                on_press=lambda x, item_id=item_id: self._view_item(item_id)
            )
            btn_del = Button(
                text='DEL', size_hint_x=None, width=dp(70),
                on_press=lambda x, item_id=item_id, wrapper=wrapper: self._del_item(item_id, wrapper)
            )
            wrapper.add_widget(btn_del)
            wrapper.add_widget(btn)
            self.items_grid.add_widget(wrapper)

    def on_leave(self):  # Будет вызвана в момент закрытия экрана
        self.items_grid.clear_widgets()

    def _view_item(self, id_item):
        gv.cur_id_item = id_item
        set_screen('view_item')
    
    def _del_item(self, id_item, wrapper):
        gv.db.delete_item(id_item)
        self.items_grid.remove_widget(wrapper)