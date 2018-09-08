# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from libs.utils import utils
from libs.customwidgets.ico.cardicobazaar import CardIcoBazaar


class Ico(Screen):
    icobazaar_ = ObjectProperty()
    noname_ = ObjectProperty()
    grid_box = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Ico, self).__init__(**kwargs)
        self.cls_inst = None
        self.config = None

    def on_enter(self, *args):
        # if self.width > dp(1500):
        #     self.test.cols = 2
        #
        # elif self.width > dp(2000):
        #     self.test.cols = 3

        self.grid_box.bind(minimum_height=self.grid_box.setter('height'))

        for _ in range(0, 15):
            card = CardIcoBazaar({'img_src': 'https://icobazaar.com/storage/campaigns/5494/logo.jpg',
                                  'ico_name': 'Hada DBank', 'updated_date': 'updated 01 January 2018',
                                  'ico_text': 'Caring and Personal', 'ico_status': 'upcoming', 'ico_date': 'TBA',
                                  'ico_text_rating': 'A', 'ico_star_rating': 3.5,
                                  'ico_full_desc_link': 'https://icobazaar.com/v2/hada-dbank-1'})
            self.grid_box.add_widget(card)

    def callback(self, instance, value):
        """Callback method which get instance and value and handle switches magic."""
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
        """Method which get config from *.ini file and return."""
        self.config = cfg

        return True if cfg.get('ICO', parser_name) == 'True' else False
