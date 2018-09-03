# -*- coding: utf-8 -*-
import os

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty

from libs.applibs.kivymd.theming import ThemeManager

from libs.uix.baseclasses.startscreen import StartScreen
from libs.mixins.dialogmixin import DialogMixin
from libs.utils import utils


class CryptoLabApp(App):
    theme_cls = ThemeManager()
    title = "CRyptoLabX"
    nav_drawer = ObjectProperty()

    def __init__(self, **kwargs):
        super(CryptoLabApp, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.events_program)
        Window.soft_input_mode = 'below_target'

        self.window = Window
        self.screen = None
        self.manager = None
        self.list_previous_screens = ['last']

    def build(self):
        self.load_all_kv_files(os.path.join(self.directory, 'libs', 'uix', 'kv'))
        self.theme_cls.theme_style = 'Dark'

        self.screen = StartScreen()
        self.manager = self.screen.ids.manager
        self.nav_drawer = self.screen.ids.nav_drawer

        return self.screen

    def initialize_storage(self):
        user_dir = self.user_data_dir

        return user_dir

    @staticmethod
    def load_all_kv_files(directory_kv_files):
        for kv_file in os.listdir(directory_kv_files):
            kv_file = os.path.join(directory_kv_files, kv_file)

            if os.path.isfile(kv_file):
                Builder.load_file(kv_file)

    def events_program(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.nav_drawer.state == 'open':
                self.nav_drawer.toggle_nav_drawer()

            self.back_screen(event=keyboard)

        elif keyboard in (282, 319):
            pass

        return True

    def back_screen(self, event=None):
        if event in (1001, 27):
            if self.manager.current == 'last':
                return
            try:
                self.manager.current = self.list_previous_screens.pop()
            except Exception as e:
                print(e)
                self.manager.current = 'last'

            self.screen.ids.action_bar.title = self.title
            self.screen.ids.action_bar.left_action_items = [['menu', lambda x: self.nav_drawer._toggle()]]

    def show_login(self, *args):
        store = utils.get_store(self.user_data_dir)
        auth = None

        if store.exists('credentials'):
            auth = store.get('credentials')['auth']

        if auth is True:
            DialogMixin().show_logout_dialog("", "Вы уверены , что хотите выйти из вашего аккаунта?"
                                             " Часть функций может быть недоступна после этого.", self.user_data_dir)
            self.nav_drawer._toggle()
        else:
            self.nav_drawer.toggle_nav_drawer()
            self.manager.current = 'login'
            self.screen.ids.action_bar.left_action_items = [['chevron-left', lambda x: self.back_screen(27)]]
            self.screen.ids.action_bar.title = 'Войти'

    def show_cryptoteka(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.manager.current = 'cryptoteka'
        self.screen.ids.action_bar.left_action_items = [['chevron-left', lambda x: self.back_screen(27)]]
        self.screen.ids.action_bar.title = 'Криптотека'

    def watch_history(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.manager.current = 'watch_history'
        self.screen.ids.action_bar.left_action_items = [['chevron-left', lambda x: self.back_screen(27)]]
        self.screen.ids.action_bar.title = 'История просмотров'

    def show_news(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.manager.current = 'news'
        self.screen.ids.action_bar.left_action_items = [['chevron-left', lambda x: self.back_screen(27)]]
        self.screen.ids.action_bar.title = 'Новости'

    def show_ico(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.manager.current = 'ico'
        self.screen.ids.action_bar.left_action_items = [['chevron-left', lambda x: self.back_screen(27)]]
        self.screen.ids.action_bar.title = 'ICO'

    def show_airdrops(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.manager.current = 'airdrops'
        self.screen.ids.action_bar.left_action_items = [['chevron-left', lambda x: self.back_screen(27)]]
        self.screen.ids.action_bar.title = 'Аирдропы'

    def show_btt(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.manager.current = 'btt'
        self.screen.ids.action_bar.left_action_items = [['chevron-left', lambda x: self.back_screen(27)]]
        self.screen.ids.action_bar.title = 'BTT'

    def show_events(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.manager.current = 'events'
        self.screen.ids.action_bar.left_action_items = [['chevron-left', lambda x: self.back_screen(27)]]
        self.screen.ids.action_bar.title = 'События'

    def show_last(self, *args):
        self.screen.ids.action_bar.left_action_items = [['menu', lambda x: self.nav_drawer._toggle()]]
        self.manager.current = 'last'
        self.screen.ids.action_bar.title = 'Последние'

    def show_lucky(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.manager.current = 'lucky'
        self.screen.ids.action_bar.left_action_items = [['chevron-left', lambda x: self.back_screen(27)]]
        self.screen.ids.action_bar.title = 'Мне повезет'

    def show_settings(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.manager.current = 'settings'
        self.screen.ids.action_bar.left_action_items = [['chevron-left', lambda x: self.back_screen(27)]]
        self.screen.ids.action_bar.title = 'Настройки'

    def show_search(self, *args):
        if self.nav_drawer.state == 'open':
            self.nav_drawer.toggle_nav_drawer()

        self.manager.current = 'search'
        self.screen.ids.action_bar.left_action_items = [['chevron-left', lambda x: self.back_screen(27)]]
        self.screen.ids.action_bar.title = 'Поиск'

    def on_pause(self):
        return True


if __name__ == '__main__':
    CryptoLabApp().run()
