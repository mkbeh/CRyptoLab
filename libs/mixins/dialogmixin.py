# -*- coding: utf-8 -*-

import os

from os.path import join

from kivy.metrics import dp

from libs.applibs.kivymd.dialog import MDDialog
from libs.applibs.kivymd.label import MDLabel
from libs.mixins.snackbarmixin import SnackbarMixin


class DialogMixin:
    def __init__(self):
        self.dialog = None
        self.error_title = 'Соощение об ошибке.'

    @staticmethod
    def foo(data_dir, dialog):
        os.remove(join(data_dir, 'creds.json'))
        dialog.dismiss()
        SnackbarMixin().show_snackbar(SnackbarMixin().success_logout)

    def show_dialog(self, dialog_title, dialog_text):
        content = MDLabel(font_style='Body1', theme_text_color='Secondary', text=dialog_text,
                          size_hint_y=None, valign='top')

        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title=dialog_title, content=content, size_hint=(.8, None),
                               height=dp(200), auto_dismiss=False)

        self.dialog.add_action_button("Закрыть",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    def show_logout_dialog(self, dialog_title, dialog_text, data_dir):
        content = MDLabel(font_style='Body1', theme_text_color='Secondary', text=dialog_text,
                          size_hint_y=None, valign='top')

        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title=dialog_title, content=content, size_hint=(.8, None),
                               height=dp(200), auto_dismiss=False)

        self.dialog.add_action_button("Да", action=lambda *x: self.foo(data_dir, self.dialog))
        self.dialog.add_action_button("Нет", action=lambda *x: self.dialog.dismiss())

        self.dialog.open()
