#!/usr/bin/python3
# -*- coding: utf-8 -*-
import base64

import utils

from os.path import join

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.storage.jsonstore import JsonStore

from kivymd.theming import ThemeManager
from kivymd.navigationdrawer import NavigationLayout, MDNavigationDrawer

from mixins.validatemixin import ValidateMixin
from pycryptolab.cryptolabapi import CryptolabApi


Config.set("graphics", "resizable", "1")
Config.set("graphics", "width", "900")
Config.set("graphics", "height", "1700")


class StorageMixin(Screen):
    data_dir = App().user_data_dir
    store = JsonStore(join(data_dir, 'storage.json'))


class LoginScreen(ValidateMixin, StorageMixin, CryptolabApi):
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

        # Check result of validation.
        if result is True:
            try:
                id_ = self.user_login(self.email_.text, self.password_.text, id_)['id'].strip('"')
                key = base64.b64encode(bytes(id_ + id_[0:8], 'utf-8'))
                id_ = base64.b64encode(bytes(id_, 'utf-8')).decode('utf-8')

                email = utils.encrypt_string(self.email_.text, key).decode('utf-8')
                password = utils.encrypt_string(self.password_.text, key).decode('utf-8')

                # Append data to storage.
                LoginScreen().store.put('id', id=id_)
                LoginScreen().store.put('credentials', email=email, password=password)

                # Change screen.
                self.manager.current = "mainScreen"
                self.clear_all(self.error_, self.email_, self.password_)

            except KeyError:
                self.error(self.error_, self.incorrect_data)
                self.clear_input_fields(self.email_, self.password_)

            except TypeError:
                self.error(self.error_, self.no_connection)
                self.clear_input_fields(self.email_, self.password_)


class RegistrationScreen(ValidateMixin, StorageMixin, CryptolabApi):
    error_ = ObjectProperty()
    email_ = ObjectProperty()
    password_ = ObjectProperty()
    confirm_password_ = ObjectProperty()

    def registration(self):
        # Validate input fields.
        result = self.validate_fields(self.error_, self.email_, self.password_, self.confirm_password_)

        # Check result of validation.
        if result is True:
            # Send data to REST API.
            try:
                id_ = (self.user_registration(self.email_.text, self.password_.text,
                                              self.confirm_password_.text)['id']).strip('"')
                id_ = base64.b64encode(bytes(id_, 'utf-8')).decode('utf-8')

                # Add id to cache.
                RegistrationScreen.store.put('id', id=id_)

                # Change screen , clear fields and messages.
                self.manager.current = "loginScreen"
                self.clear_all(self.error_, self.email_, self.password_, self.confirm_password_)

            except KeyError:
                # Display error 'user already exist' and clear input fields.
                self.error(self.error_, self.user_exist)
                self.clear_input_fields(self.email_, self.password_, self.confirm_password_)

            except TypeError:
                # Display error 'no connection with server' and clear input fields.
                self.error(self.error_, self.no_connection)
                self.clear_input_fields(self.email_, self.password_, self.confirm_password_)


class Navigator(NavigationLayout):
    pass


class MainScreen(Screen):
    pass


class Manager(ScreenManager):
    login_screen = ObjectProperty(None)
    registration_screen = ObjectProperty(None)
    main_page = ObjectProperty(None)


class CryptolabApp(App, Screen, CryptolabApi):
    data_dir = App().user_data_dir
    store = JsonStore(join(data_dir, 'storage.json'))
    theme_cls = ThemeManager()
    nav_drawer = ObjectProperty()

    def auth(self):
        # Get user credentials from storage.
        try:
            id_ = self.store.get('id')['id']
            id_ = base64.b64decode(bytes(id_, 'utf-8')).decode('utf-8')
            key = base64.b64encode(bytes(id_ + id_[0:8], 'utf-8'))

            email = utils.decrypt_string(bytes(self.store.get('credentials')['email'], 'utf-8'), key)
            password = utils.decrypt_string(bytes(self.store.get('credentials')['password'], 'utf-8'), key)

            try:
                response = self.user_login(email, password, id_)

                if response['id']:
                    return True

            except TypeError:
                # Create max retries , if don't auth - change screen to LOGIN PAGE.
                print('CREATE MAX RETRIES')

        except KeyError:
            print('KEYERROR WHILE GETTING DATA FROM STORAGE')

    def build(self):
        m = Manager(transition=NoTransition())
        self.theme_cls.theme_style = 'Dark'

        if self.auth() is True:
            m.current = "mainScreen"
            self.nav_drawer = NavigationLayout()

            return m

        else:
            return m


if __name__ == "__main__":
    CryptolabApp().run()
