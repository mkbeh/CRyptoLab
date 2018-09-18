# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from libs.utils import utils
from libs.uix.baseclasses.ico_dir.icobazaar import Icobazaar


class Ico(Screen):
    icobazaar_ = ObjectProperty()
    noname_ = ObjectProperty()
    ico_list_tab = ObjectProperty(None)
    scrl_view = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Ico, self).__init__(**kwargs)
        self.cls_inst = None
        self.config = None
        self.parser_names = ['icobazaar', 'noname']
        self.icobazaar = Icobazaar()

        self.parser = None

        from kivy.uix.widget import Widget  # just for test
        self.test = {'icobazaar': Icobazaar(), 'noname': Widget()}

    def on_enter(self, *args):
        """
        Event fired when the screen is displayed: the entering animation is complete.
        Method which load parser data from dependencies of parser config state.
        :param args:
        :return:
        """
        for parser_name in self.parser_names:
            if self.config.get('ICO', parser_name) == 'True':
                self.parser = self.test[parser_name]

        try:
            self.scrl_view.clear_widgets()
            self.scrl_view.add_widget(self.parser)
        except Exception as e:
            print(e)

    def callback(self, instance, value):
        """
        Callback method which get instance and value and handle switches magic in section 'Catalog'.
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

    def load_data(self):
        self.on_enter(self.__class__)

