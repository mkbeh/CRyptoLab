# -*- coding: utf-8 -*-
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout


Builder.load_string('''
#:import get_path libs.utils.utils.get_path
#:import Window kivy.core.window.Window

<NoConnectionErrorCM>:
    btn: btn

    orientation: 'vertical'
    pos_hint: {'center_x': .5, 'center_y': .5}
    size_hint_y: None
    size: (400, 400)
    
    Image:
        source: get_path() + '/images/no_connection.png' 
    
    MDLabel:
        font_style: 'Subhead'
        theme_text_color: 'Primary'
        halign: 'center'
        text: 'Нет соединения с сервером. Проверьте подключение к интернету.'
        
    MDRaisedButton:
        id: btn
        
        text: "Попробовать еще раз"
        opposite_colors: True
        size_hint: None, None
        size: 4 * dp(48), dp(48)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        # on_release: app.show_ico()
''')


class NoConnectionErrorCM(BoxLayout):
    btn = ObjectProperty()
