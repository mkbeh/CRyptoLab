# -*- coding: utf-8 -*-
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.cache import Cache
from kivy.uix.scrollview import ScrollView
from kivy.lang.builder import Builder

from libs.applibs.kivymd.theming import ThemableBehavior

from libs.customwidgets.navdrawericonbuttoncm import NavDrawerIconButtonCM
from libs.utils import utils


Builder.load_string('''
<PopupCMContent>:
    popup_grid_box: popup_grid_box
    do_scroll_y: True

    canvas.before:
        Color:
            rgba: root.theme_cls.bg_dark
        Rectangle:
            size: root.size
            pos: root.pos

    GridLayout:
        cols: 1
        id: popup_grid_box
        size_hint_y: None 
''')


class PopupCMContent(ScrollView, ThemableBehavior):
    popup_grid_box = ObjectProperty(None)
    last_category_btn = None

    def __init__(self, **kwargs):
        super(PopupCMContent, self).__init__(**kwargs)

        self.popup_grid_box.bind(minimum_height=self.popup_grid_box.setter('height'))

        # Get active's category text.
        val = Cache.get('popup', 'cat_text')

        for _ in range(20):
            self.cat_btn = NavDrawerIconButtonCM(text='Artificial Intelligence            ' + '1300',
                                                 _active=False, on_release=lambda x: self.on_event(x))
            if val is not None:
                if utils.coincidence_check(self.cat_btn.text, val) is not None:
                    self.cat_btn._active = True

            self.popup_grid_box.add_widget(self.cat_btn)

    def on_event(self, obj):
        """
        Event method which fired when clicked on category button.
        This method change set active color to button and remove active color from last pressed.
        :param obj:
        :return:
        """
        try:
            self.last_category_btn._active = False
            self.last_category_btn = obj
        except AttributeError:
            pass

        obj._active = True
        self.last_category_btn = obj

        # Add object text to cache.
        Cache.register('popup')
        Cache.append('popup', 'cat_text', obj.text)

        # Get popup obj from cache and dismiss popup.
        popup_obj = Cache.get('main_popup', 'popup_obj')
        popup_obj.dismiss()


class PopupCM(Popup, ThemableBehavior):
    def __init__(self, **kwargs):
        super(PopupCM, self).__init__(**kwargs)

        self.size_hint = (None, None)
        self.auto_dismiss = True
        self.size = (350, 600)

        self.separator_color = self.theme_cls.primary_color

        # Add popup obj to cache.
        Cache.register('main_popup')
        Cache.append('main_popup', 'popup_obj', self)

    def on_dismiss(self):
        popup_cats_lst = self.children[0].children[0].children[0].children[0].children

        for cat in popup_cats_lst:
            if cat._active is True:
                test = Cache.get('menu_cats_box', 'cats_box_obj')

                for child in test.children:
                    child._active = False

                    if child.name == 'categories':
                        child._active = True
