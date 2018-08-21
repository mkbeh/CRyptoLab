# -*- coding: utf-8 -*-
import base64

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from libs.utils import utils
from libs.mixins.validatemixin import ValidateMixin
from libs.mixins.dialogmixin import DialogMixin
from libs.mixins.snackbarmixin import SnackbarMixin
from libs.pycryptolab.cryptolabapi import CryptolabApi


class Login(Screen, CryptolabApi):
    email_ = ObjectProperty()
    password_ = ObjectProperty()

    def login(self, user_dir):
        store = utils.get_store(user_dir)

        # Get user id from storage.
        try:
            id_ = store.get('id')['id']
            id_ = base64.b64decode(bytes(id_, 'utf-8')).decode('utf-8')
        except KeyError:
            id_ = 'None'

        # Validate input fields.
        result = ValidateMixin().validate_fields(self.email_, self.password_)

        if result is True:
            try:
                id_ = self.user_login(self.email_.text, self.password_.text, id_)['id'].strip('"')
                key = base64.b64encode(bytes(id_ + id_[0:8], 'utf-8'))
                id_ = base64.b64encode(bytes(id_, 'utf-8')).decode('utf-8')

                email = utils.encrypt_string(self.email_.text, key).decode('utf-8')
                password = utils.encrypt_string(self.password_.text, key).decode('utf-8')

                # Append data to storage.
                store.put('id', id=id_)
                store.put('credentials', email=email, password=password, auth=True)

                ValidateMixin().clear_input_fields(self.email_, self.password_)
                SnackbarMixin().show_snackbar(SnackbarMixin().success_auth)

                return True

            except KeyError:
                DialogMixin().show_dialog(DialogMixin().error_title, ValidateMixin().incorrect_data)
                ValidateMixin().clear_input_fields(self.email_, self.password_)

            except TypeError:
                DialogMixin().show_dialog(DialogMixin().error_title, ValidateMixin().no_connection)
                ValidateMixin().clear_input_fields(self.email_, self.password_)

        elif result is False:
            ValidateMixin().clear_input_fields(self.email_, self.password_)
            DialogMixin().show_dialog(DialogMixin().error_title, ValidateMixin().incorrect_data)
