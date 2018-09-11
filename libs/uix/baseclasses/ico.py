# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from libs.utils import utils
from libs.customwidgets.ico.cardicobazaar import CardIcoBazaar

# Temp
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.lang.builder import Builder

from libs.applibs.kivymd.navigationdrawer import NavigationDrawerIconButton

from libs.applibs.kivymd.theming import ThemableBehavior


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


class ModifiedNavDrawerIconButton(NavigationDrawerIconButton):

    def on_icon(self, instance, value):
        pass


class PopupCMContent(ScrollView, ThemableBehavior):
    popup_grid_box = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PopupCMContent, self).__init__(**kwargs)

        self.popup_grid_box.bind(minimum_height=self.popup_grid_box.setter('height'))

        for _ in range(20):
            self.cat_btn = ModifiedNavDrawerIconButton(text='Artificial Intelligence            ' + '1300',
                                                       _active=True)
            self.popup_grid_box.add_widget(self.cat_btn)


class PopupCM(Popup, ThemableBehavior):
    def __init__(self, **kwargs):
        super(PopupCM, self).__init__(**kwargs)

        self.size_hint = (None, None)
        self.auto_dismiss = True
        self.size = (350, 600)

        self.separator_color = self.theme_cls.primary_color


class Ico(Screen):
    icobazaar_ = ObjectProperty()
    noname_ = ObjectProperty()
    grid_box = ObjectProperty(None)

    last_category_btn = None                            # Last menu button , which was pressed.
    upcoming = ObjectProperty()

    @staticmethod
    def open_categories_popup():
        popup = PopupCM(title='Категории', content=PopupCMContent())
        popup.open()

    def __init__(self, **kwargs):
        super(Ico, self).__init__(**kwargs)
        self.cls_inst = None
        self.config = None

    def on_event(self, obj):
        """
        Event method which fired when clicked on category button.
        This method change set active color to button and remove active color from last pressed.
        :param obj:
        :return:
        """
        try:
            self.upcoming._active = False
            self.last_category_btn._active = False
            self.last_category_btn = obj
        except AttributeError:
            pass

        obj._active = True
        self.last_category_btn = obj

    def on_enter(self, *args):
        self.upcoming._active = True
        self.grid_box.bind(minimum_height=self.grid_box.setter('height'))

        for _ in range(0, 15):
            card = CardIcoBazaar({'img_src': 'https://icobazaar.com/storage/campaigns/5494/logo.jpg',
                                  'ico_name': 'Hada DBank', 'updated_date': 'updated 01 January 2018',
                                  'ico_text': 'Caring and Personal', 'ico_status': 'upcoming', 'ico_date': 'TBA',
                                  'ico_text_rating': 'A', 'ico_star_rating': 3.5,
                                  'ico_full_desc_link': 'https://icobazaar.com/v2/hada-dbank-1'})
            self.grid_box.add_widget(card)

    def callback(self, instance, value):
        """
        Callback method which get instance and value and handle switches magic.
        :param instance:
        :param value:
        :return:
        """
        self.icobazaar_.bind(active=self.callback)
        self.noname_.bind(active=self.callback)

        # Switches magic.
        attrs_lst = [self.icobazaar_, self.noname_]

        if value is True:
            for attr in attrs_lst:
                if attr.name == instance.name:
                    utils.write_into_cfg(self.config, 'ICO', attr.name, value)
                    attrs_lst.remove(attr)
                    self.cls_inst = instance

            for attr in attrs_lst:
                utils.write_into_cfg(self.config, 'ICO', attr.name, False)
                attr.active = False

        if value is False:
            if instance == self.cls_inst:
                instance.active = True

    def get_switch_val(self, cfg, parser_name):
        """
        Method which get config from *.ini file and return.
        :param cfg:
        :param parser_name:
        :return:
        """
        self.config = cfg

        return True if cfg.get('ICO', parser_name) == 'True' else False
