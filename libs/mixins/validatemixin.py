# -*- coding: utf-8 -*-

from libs.utils import utils


class ValidateMixin(object):
    """Methods for validate input fields , login and
    authorise users."""
    no_connection = 'Ошибка. Нет соединения с сервером.'
    incorrect_data = 'Ошибка. Введены неправильные данные.\nПопробуйте еще раз.'
    user_exist = 'Ошибка. Пользователь с таким email\nуже зарегистрирован.'

    @staticmethod
    def clear_all(error, email, password, confirm_password=None):
        error.text = ''
        error.size_hint_y = None
        error.height = '0dp'

        email.text = ''
        password.text = ''

        if confirm_password is not None:
            confirm_password.text = ''

    @staticmethod
    def clear_input_fields(email, password, confirm_password=None):
        email.text = ''
        password.text = ''

        if confirm_password is not None:
            confirm_password.text = ''

    @staticmethod
    def error(error, text):
        error.text = text
        error.size_hint_y = 0.05

    def validate_fields(self, error, email, password, confirm_password=None):
        try:
            result = utils.validate_values(email.text, password.text, confirm_password.text)

            if result is False:
                self.error(error, self.incorrect_data)
                self.clear_input_fields(email, password, confirm_password)

            else:
                return True

        except AttributeError:
            result = utils.validate_values(email.text, password.text)

            if result is False:
                self.error(error, self.incorrect_data)
                self.clear_input_fields(email, password)

            else:
                return True
