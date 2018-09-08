# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.image import Image, AsyncImage

from libs.applibs.kivymd.card import MDCard

from libs.utils import utils


Builder.load_string('''
#:import MDCard libs.applibs.kivymd.card.MDCard
#:import MDSeparator libs.applibs.kivymd.card.MDSeparator
#:import MDLabel libs.applibs.kivymd.label.MDLabel

    
<FieldLabel@MDLabel>:
    font_style: 'Caption'
    theme_text_color: 'Primary'


<CardIcoBazaar>:
    stars_box: stars_box
    image_box: image_box

    size_hint: .95, None
    pos_hint: {'center_x': 0.5}
    size_hint_y: None
    height: dp(120)
    
    on_touch_down: root.switch_to_card_screen(app.manager, app.screen, app)
                    
    BoxLayout:
        padding: (dp(10), dp(10), dp(10), dp(10))
        spacing: dp(20)
        id: main_box
        
        BoxLayout:
            id: image_box   
            size_hint_x: 0.0     
                
        GridLayout:  
            cols: 3
            height: dp(120)
                
            size_hint_x: 0.4
            pos_hint: {'center_x': 0.5}
                    
            GridLayout:
                rows: 3
                size_hint_x: .5
                
                BoxLayout:
                    orientation: 'vertical'
                        
                    MDLabel:
                        text: root.get_val('ico_name')
                        font_style: 'Subhead'
                        theme_text_color: 'Primary'
                        
                    GridLayout:
                        size_hint_y: 0.4
                        cols: 2
                        spacing: dp(5)
                        
                        Image:
                            size_hint_x: 0.05
                            source: root.img_updated_src
                                
                        MDLabel:
                            text: root.get_val('updated_date')
                            font_style: 'Body1'
                            theme_text_color: 'Primary'
    
                FieldLabel:
                    text: root.get_val('ico_text')
                
            BoxLayout:
                size_hint_x: .6
                
                GridLayout:  
                    rows: 3
                    
                    BoxLayout:
                        orientation: 'vertical'
                        
                        Widget:
                            
                        GridLayout:
                            size_hint_y: 0.4
                            cols: 2
                            spacing: dp(5)
                        
                            Image:
                                size_hint_x: 0.05
                                source: root.get_status_img_path()
                                                        
                            FieldLabel:
                                text: root.get_val('ico_status')
                                
                    FieldLabel:
                        text: root.get_val('ico_date')
                        
                GridLayout:  
                    rows: 3
                    size_hint_y: .8
                    
                    BoxLayout:
                        orientation: 'vertical'
                        padding: (dp(45), 0, 0, 0)
                                                     
                        FieldLabel:
                            text: root.get_val('ico_text_rating')
                            size_hint_y: .3
                            bold: True
                                
                    GridLayout:
                        id: stars_box
                        rows: 1
                        size_hint_y: .3
                        size_hint_x: None
                                
                    Widget:
                        size_hint_y: .4           
''')


class CardIcoBazaar(MDCard):
    image_box = ObjectProperty(None)
    stars_box = ObjectProperty(None)
    img_updated_src = utils.get_path() + '/images/ico/icobazaar/updated.png'

    def __init__(self, *args, **kwargs):
        self.data = args
        super(CardIcoBazaar, self).__init__(**kwargs)

        self.add_stars()                                # get stars amount and add to card.
        self.img_status = self.get_status_img_path()    # get status image and add to card.
        self.get_logo()                                 # add downloaded logo images from web to card.

    def switch_to_card_screen(self, scr_mgr, scr, app_obj):
        """
        This method call when the event on touch of card was fired.
        This method switch to the screen named icobazaar.
        :param scr_mgr:
        :param scr:
        :param app_obj:
        :return:
        """
        if 'ico' not in app_obj.list_previous_screens:
            app_obj.list_previous_screens.append('ico')

        scr_mgr.current = 'icobazaar'
        scr.ids.action_bar.left_action_items = [['chevron-left', lambda x: app_obj.back_screen(27)]]

        scr.ids.action_bar.title, app_obj.temp_data = self.get_val('ico_name'), self.get_val('ico_full_desc_link')

    def get_val(self, key):
        """
        Method which get key name as param and return data value.
        :param key:
        :return:
        """
        return self.data[0][key]

    def add_stars(self):
        """
        Method which get stars amount from data and add them to card.
        :return:
        """
        stars_amount = self.get_val('ico_star_rating')
        star_src = utils.get_path() + '/images/ico/icobazaar/star.png'
        half_star_src = utils.get_path() + '/images/ico/icobazaar/half_star.png'

        try:
            [self.stars_box.add_widget(Image(source=star_src)) for _ in range(0, stars_amount)]
        except TypeError:
            new_starts_amount = int(round(stars_amount, 0))

            for i in range(0, new_starts_amount - 1):
                self.stars_box.add_widget(Image(source=star_src))

                if i == new_starts_amount - 2:
                    self.stars_box.add_widget(Image(source=half_star_src))

    def get_status_img_path(self):
        """
        Method which return status image path depending of the status value from data.
        :return:
        """
        status = self.get_val('ico_status')

        return utils.get_path() + '/images/ico/icobazaar/{}.png'.format(status)

    def get_logo(self):
        """
        Method which add downloaded images from web to BoxLayout.
        :return:
        """
        source = self.get_val('img_src')
        self.image_box.add_widget(AsyncImage(source=source, size_hint_x=None, mipmap=True))
