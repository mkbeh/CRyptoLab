# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


class Ico(Screen):
    icobazaar_ = ObjectProperty()
    noname_ = ObjectProperty()

    def __init__(self, **kwargs):
        super(Ico, self).__init__(**kwargs)
        self.cls_inst = None

    def callback(self, instance, value):
        """Callback method which get instance and value and handle switches magic."""
        self.icobazaar_.bind(active=self.callback)
        self.noname_.bind(active=self.callback)

        # Switches magic.
        attrs_lst = [self.icobazaar_, self.noname_]

        if value is True:
            for attr in attrs_lst:
                if attr.name == instance.name:
                    attrs_lst.remove(attr)
                    self.cls_inst = instance

            for attr in attrs_lst:
                attr.active = False

        if value is False:
            if instance == self.cls_inst:
                instance.active = True
