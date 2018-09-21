# -*- coding: utf-8 -*-
import functools

import requests

from requests.exceptions import ConnectionError
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from libs.utils import utils
from libs.uix.baseclasses.ico_dir.icobazaar import Icobazaar
from libs.customwidgets.noconnectionerrorcm import NoConnectionErrorCM


class Ico(Screen):
    icobazaar_ = ObjectProperty()
    noname_ = ObjectProperty()
    scrl_view = ObjectProperty(None)
    ico_list = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Ico, self).__init__(**kwargs)
        self.cls_inst = None
        self.config = None
        self.no_connection_error = None
        self.parser = None

        from kivy.uix.widget import Widget  # just for test
        self.parsers_dict = {'icobazaar': Icobazaar, 'noname': Widget}

    def on_enter(self, *args):
        """
        Event fired when the screen is displayed: the entering animation is complete.
        Method which Check connection with server and load parser data from dependencies of parser config state if
        connection establish , else display widget error.
        :param args:
        :return:
        """
        # Check connection.
        try:
            requests.get('http://127.0.0.1:8000/api', timeout=(3.05, 27), stream=True)

            for parser_name in self.parsers_dict:
                if self.config.get('ICO', parser_name) == 'True':
                    self.parser = self.parsers_dict[parser_name]

            # Add parser data.
            if self.no_connection_error is not None:
                self.ico_list.remove_widget(self.no_connection_error)
                self.no_connection_error = None

            self.scrl_view.clear_widgets()
            self.scrl_view.add_widget(self.parser())

        except ConnectionError:
            self.scrl_view.clear_widgets()

            if self.no_connection_error is None:
                self.no_connection_error = NoConnectionErrorCM()
                self.no_connection_error.btn.on_release = functools.partial(self.on_enter, self.__class__)
                self.ico_list.add_widget(self.no_connection_error, index=0)

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

