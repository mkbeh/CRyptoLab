# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen


class IcobazaarItem(Screen):
    """
    Full description page of ico project.
    """
    def __init__(self, **kwargs):
        super(IcobazaarItem, self).__init__(**kwargs)
        self.ico_full_desc_link = None

    def foo(self, ico_full_desc_link):
        self.ico_full_desc_link = ico_full_desc_link
        print(self.ico_full_desc_link)
