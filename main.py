# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.theming import ThemeManager


class CryptoLabApp(App):
    theme_cls = ThemeManager()
    previous_date = ObjectProperty()
    title = "CRyptoLab"

    def build(self):
        main_widget = Builder.load_file('cryptolab.kv')
        self.theme_cls.theme_style = 'Dark'

        return main_widget


if __name__ == '__main__':
    CryptoLabApp().run()
