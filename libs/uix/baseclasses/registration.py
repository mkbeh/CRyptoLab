# -*- coding: utf-8 -*-
import base64

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from libs.mixins.validatemixin import ValidateMixin
from libs.mixins.dialogmixin import DialogMixin
from libs.mixins.snackbarmixin import SnackbarMixin
from libs.pycryptolab.cryptolabapi import CryptolabApi
from libs.utils import utils


class Registration(Screen, CryptolabApi):
    username_ = ObjectProperty()
    email_ = ObjectProperty()
    password_ = ObjectProperty()
    confirm_password_ = ObjectProperty()

    def registration(self, user_dir):
        store = utils.get_store(user_dir)

        # Validate input fields.
        result = ValidateMixin().validate_fields(self.email_, self.password_, self.confirm_password_, self.username_)

        # Check result of validation.
        if result is True:
            # Send data to REST API.
            try:
                id_ = (self.user_registration(self.email_.text, self.password_.text,
                                              self.confirm_password_.text, self.username_.text)['id']).strip('"')
                id_ = base64.b64encode(bytes(id_, 'utf-8')).decode('utf-8')

                # Add id to cache.
                store.put('id', id=id_)

                # Change screen , clear input fields.
                self.manager.current = "login"
                ValidateMixin().clear_input_fields(self.email_, self.password_, self.confirm_password_, self.username_)
                SnackbarMixin().show_snackbar(SnackbarMixin().success_registration)

            except KeyError:
                # Display error 'user already exist' and clear input fields.
                DialogMixin().show_dialog(DialogMixin().error_title, ValidateMixin().user_exist)
                ValidateMixin().clear_input_fields(self.email_, self.password_, self.confirm_password_, self.username_)

            except TypeError:
                # Display error 'no connection with server' and clear input fields.
                DialogMixin().show_dialog(DialogMixin().error_title, ValidateMixin().no_connection)
                ValidateMixin().clear_input_fields(self.email_, self.password_, self.confirm_password_, self.username_)

        elif result is False:
            ValidateMixin().clear_input_fields(self.email_, self.password_, self.confirm_password_, self.username_)
            DialogMixin().show_dialog(DialogMixin().error_title, ValidateMixin().incorrect_data)
