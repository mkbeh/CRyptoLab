# -*- coding: utf-8 -*-
import base64

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from libs.utils import utils
from libs.mixins.validatemixin import ValidateMixin


class Login(Screen):
    error_ = ObjectProperty()
    email_ = ObjectProperty()
    password_ = ObjectProperty()

    def login(self):
        # Get user id from storage.
        try:
            id_ = self.store.get('id')['id']
            id_ = base64.b64decode(bytes(id_, 'utf-8')).decode('utf-8')
        except KeyError:
            id_ = 'None'

        # Validate input fields.
        result = self.validate_fields(self.error_, self.email_, self.password_)


