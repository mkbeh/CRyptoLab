# -*- coding: utf-8 -*-
from libs.applibs.kivymd.snackbar import Snackbar


class SnackbarMixin:
    def __init__(self):
        self.success_auth = 'Вы успешно авторизировались'
        self.success_registration = 'Вы успешно зарегистрировались'
        self.success_logout = 'Вы успешно вышли'

    @staticmethod
    def show_snackbar(snackbar_text):
        Snackbar(text=snackbar_text).show()
