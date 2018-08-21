# -*- coding: utf-8 -*-

from libs.utils import utils


class ValidateMixin(object):
    """Methods for validate input fields , login and
    authorise users."""
    no_connection = 'Ошибка. Нет соединения с сервером.'
    incorrect_data = 'Ошибка. Введены неправильные данные.\nПопробуйте еще раз.'
    user_exist = 'Ошибка. Пользователь с таким email\nуже зарегистрирован.'

    @staticmethod
    def clear_input_fields(email, password, confirm_password=None, username=None):
        email.text = ''
        password.text = ''

        if confirm_password is not None:
            confirm_password.text = ''
            username.text = ''

    def validate_fields(self, email, password, confirm_password=None, username=None):
        try:
            result = utils.validate_values(email.text, password.text, confirm_password.text, username.text)

            if result is False:
                self.clear_input_fields(email, password, confirm_password, username)
                return False

            else:
                return True

        except AttributeError:
            result = utils.validate_values(email.text, password.text)

            if result is False:
                self.clear_input_fields(email, password)
                return False

            else:
                return True
