# -*- coding: utf-8 -*-
import base64

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from libs.mixins.validatemixin import ValidateMixin


class Registration(Screen):
    error_ = ObjectProperty()
    email_ = ObjectProperty()
    password_ = ObjectProperty()
    confirm_password_ = ObjectProperty()

