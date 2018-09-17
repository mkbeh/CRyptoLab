# -*- coding: utf-8 -*-
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.cache import Cache
from kivy.uix.boxlayout import BoxLayout

from libs.customwidgets.ico.cardicobazaar import CardIcoBazaar
from libs.customwidgets.popupcm import PopupCM, PopupCMContent


Builder.load_string('''
<Icobazaar>:
    cats_box: cats_box
    upcoming: upcoming
    categories: categories
    grid_box: grid_box
    
    orientation: 'vertical'
    size_hint_y: None
    height: self.minimum_height

    GridLayout:
        id: cats_box
        size_hint_y: None
        cols: 3
        rows: 2

        NavigationDrawerIconButton:
            text: "Upcoming"
            badge_text: '12'

            id: upcoming
            name: 'upcoming'
            on_release: root.on_event(upcoming)

        NavigationDrawerIconButton:
            text: "Ongoing"
            badge_text: '12'

            id: ongoing
            name: 'ongoing'
            on_release: root.on_event(ongoing)

        NavigationDrawerIconButton:
            text: "Ended"
            badge_text: '12'

            id: ended
            name: 'ended'
            on_release: root.on_event(ended)

        NavigationDrawerIconButton:
            text: "New"
            badge_text: '12'

            id: new
            name: 'new'
            on_release: root.on_event(new)

        NavigationDrawerIconButton:
            text: "All"
            badge_text: '12'

            id: all
            name: 'all'
            on_release: root.on_event(all)

        NavigationDrawerIconButton:
            id: categories
            name: 'categories'

            text: "Open Categories"
            icon: 'menu-down'

            on_release:
                root.open_categories_popup();
                root.on_event(categories)

    GridLayout:
        id: grid_box

        cols: 1
        spacing: dp(20)
        pos_hint: {'center_x':.5}
        size_hint: (.95, None)
''')


class Icobazaar(BoxLayout):
    cats_box = ObjectProperty(None)
    grid_box = ObjectProperty(None)

    categories = ObjectProperty()
    upcoming = ObjectProperty()
    last_category_btn = None            # Last menu button , which was pressed.

    def __init__(self, **kwargs):
        super(Icobazaar, self).__init__(**kwargs)
        self.popup = PopupCM(title='Категории', content=PopupCMContent())
        self.gen_cards()

    def open_categories_popup(self):
        """
        Method which open popup which contains ico list of categories.
        :return:
        """
        self.popup.open()

    def on_event(self, obj):
        """
        Event method which fired when clicked on category button.
        This method change set active color to button and remove active color from last pressed.
        :param obj:
        :return:
        """
        if obj.name != 'categories':
            self.upcoming._active = False
            self.categories._active = False

            try:
                self.last_category_btn._active = False
            except AttributeError:
                pass

            obj._active = True
            self.last_category_btn = obj

            # Remove active state for all items in categories popup.
            cat_items_lst = self.popup.children[0].children[0].children[0].children[0].children

            for cat in cat_items_lst:
                cat._active = False

    def gen_cards(self):
        """
        Method which generate cards with ico projects description.
        :return:
        """
        # Check for active category button.
        if self.last_category_btn is None:
            self.upcoming._active = True

        self.grid_box.bind(minimum_height=self.grid_box.setter('height'))

        for _ in range(0, 15):
            card = CardIcoBazaar({'img_src': 'https://icobazaar.com/storage/campaigns/5494/logo.jpg',
                                  'ico_name': 'Hada DBank', 'updated_date': 'updated 01 January 2018',
                                  'ico_text': 'Caring and Personal', 'ico_status': 'upcoming', 'ico_date': 'TBA',
                                  'ico_text_rating': 'A', 'ico_star_rating': 3.5,
                                  'ico_full_desc_link': 'https://icobazaar.com/v2/hada-dbank-1'})
            self.grid_box.add_widget(card)

        #
        Cache.register('menu_cats_box')
        Cache.append('menu_cats_box', 'cats_box_obj', self.cats_box)
