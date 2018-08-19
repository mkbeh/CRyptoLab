# -*- coding: utf-8 -*-
from kivy.properties import ObjectProperty

from libs.applibs.kivymd.navigationdrawer import NavigationLayout


class NavDrawer(NavigationLayout):
    _app = ObjectProperty()

    def _toggle(self):
        self.toggle_nav_drawer()

    def add_name_previous_screen(self):
        """Добавляет в список имя текущего экрана
        для установки предыдущего при нажатии кнопки Back key."""

        name_current_screen = self._app.manager.current
        if self.state == 'open':
            try:
                if self._app.list_previous_screens[-1] == name_current_screen:
                    return
            except IndexError:
                pass
            self._app.list_previous_screens.append(name_current_screen)

