# -*- coding: utf-8 -*-
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from libs.utils import utils


class News(Screen):
    bits_media = ObjectProperty()
    noname_ = ObjectProperty()
    scrl_view = ObjectProperty(None)
    ico_list = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(News, self).__init__(**kwargs)

        self.cls_inst = None
        self.config = None

    def callback(self, instance, value):
        """
        Callback method which get instance and value and handle switches magic in section 'Catalog'.
        :param instance:
        :param value:
        :return:
        """
        self.bits_media.bind(active=self.callback)
        self.noname_.bind(active=self.callback)

        # Switches magic.
        attrs_lst = [self.bits_media, self.noname_]

        if value is True:
            for attr in attrs_lst:
                if attr.name == instance.name:
                    utils.write_into_cfg(self.config, 'News', attr.name, value)
                    attrs_lst.remove(attr)
                    self.cls_inst = instance

            for attr in attrs_lst:
                utils.write_into_cfg(self.config, 'News', attr.name, False)
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

        return True if cfg.get('News', parser_name) == 'True' else False
