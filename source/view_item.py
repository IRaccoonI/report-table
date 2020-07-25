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
from kivy.app import App

from common import set_screen
import global_vars as gv
import ast
import time



def is_lambda(v):
  LAMBDA = lambda:0
  return isinstance(v, type(LAMBDA)) and v.__name__ == LAMBDA.__name__



class ViewItem(Screen):
    def __init__(self, **kw):
        super(ViewItem, self).__init__(**kw)

        self.fields = []
        self.title_item = None

        box = BoxLayout(orientation='vertical')

        back_button = Button(text='< Назад в главное меню', on_press=lambda x:
                             set_screen('main'), size_hint_y=None, height=dp(60))
        box.add_widget(back_button)

        scroll_view = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        self.layout_fields = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.layout_fields.bind(minimum_height=self.layout_fields.setter('height'))


        scroll_view.add_widget(self.layout_fields)
        box.add_widget(scroll_view)

        self.lbl_total = Label(text="Итог: ", size_hint_y=None, height=dp(40))
        box.add_widget(self.lbl_total)

        wrapper = BoxLayout(size_hint_y=None, height=dp(60))
        btn_add = Button(text="Добавить поле")
        btn_add.bind(on_press = lambda x: self._add_item(None, None, None, 'Sum'))

        btn_submit = Button(text="Сохранить")
        btn_submit.bind(on_press = self.submit_click)

        wrapper.add_widget(btn_submit)
        wrapper.add_widget(btn_add)
        box.add_widget(wrapper)

        self.add_widget(box)


    def submit_click(self, btn):
        res_fields = []

        for field in self.fields:
            a = {}
            for (k, v) in field.items():
                if is_lambda(v):
                    a[k] = v()
                else:
                    a[k] = v
            res_fields.append(a)

        gv.db.update_item(self.id_item, self.title_item.text, res_fields)
        set_screen('main')

    def on_enter(self):  # Будет вызвана в момент открытия экрана
        # self.layout_fields

        self.id_item = gv.cur_id_item

        (item, item_fields) = gv.db.get_item_by_id(self.id_item)

        self.title_item = TextInput(text=item[1], multiline=False, height=dp(40),
                                size_hint_y=None, hint_text="Название")

        self.layout_fields.add_widget(self.title_item)

        for field in item_fields:
            self._add_item(field[0], field[1], field[3], field[2])

    def _ping4total(self, *_):
        sum_val = 0
        for field in self.fields:
            if field['type'] == 'notSum':
                continue
            str_val = field['val']()

            if not str_val:
                continue

            try:
                float_val = float(str_val)
            except ValueError:
                self.lbl_total.text = 'Error'
                return
            sum_val += float_val
        self.lbl_total.text = 'Итог: ' + str(sum_val)

    def _add_item(self, id_item, title, val, item_type):
        box = BoxLayout(size_hint_y=None, height=dp(40))

        if title:
            title = TextInput(text=title, multiline=False, height=dp(40),
                                    size_hint_y=None, hint_text="Название")
        else:
            title = TextInput(multiline=False, height=dp(40),
                                    size_hint_y=None, hint_text="Название")


        if val:
            val = TextInput(text=val, multiline=False, height=dp(40),
                                    size_hint_y=None, hint_text="Значение")
        else:
            val = TextInput(multiline=False, height=dp(40),
                                    size_hint_y=None, hint_text="Значение")
        val.bind(text = self._ping4total)

        box.add_widget(title)
        box.add_widget(val)

        self.layout_fields.add_widget(box)

        self.fields.append({'id': id_item, 'title': lambda: title.text, 'val': lambda: val.text, 'type': item_type})
        self._ping4total()

    def on_leave(self):  # Будет вызвана в момент закрытия экрана
        self.layout_fields.clear_widgets()
        self.fields = []
        self.title_item = None