from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivymd.theming import ThemeManager

from kivymd.uix.navigationdrawer import MDNavigationDrawer
# from navigationdrawer import NavigationDrawer

main_widget_kv = '''


BoxLayout:
    orientation: 'vertical'
    MDToolbar:
        id: toolbar
        title: 'Welcome'
        background_color: app.theme_cls.primary_dark
        left_action_items: [['menu', lambda x: app.nav_drawer.toggle()]]
        right_action_items: [['more-vert', lambda x: app.raised_button.open(self.parent)]]

    NavigationDrawerIconButton:
        icon: 'face'
        text: 'Kuldeep Singh'
    NavigationDrawerIconButton:
        icon: 'email'
        text: 'kuldeepbb.grewal@gmail.com'
        on_release: app.root.ids.scr_mngr.current = 'bottomsheet'
    NavigationDrawerIconButton:
        icon: 'phone'
        text: '+91-7727XXXXXX'
    NavigationDrawerIconButton:
        icon: 'cake'
        text: '26/11/1994'
    NavigationDrawerIconButton:
        icon: 'city-alt'
        text: 'Rohtak'
    NavigationDrawerIconButton:
        icon: 'settings'
        text: 'Settings'
    '''

class Navigator(MDNavigationDrawer):
    image_source = StringProperty('images/me.png')

class NavigateApp(MDApp):
    theme_cls = ThemeManager()
    nav_drawer = ObjectProperty()

    def build(self):
        main_widget = Builder.load_string(main_widget_kv)
        self.nav_drawer = Navigator()
        return main_widget
if __name__ == "__main__":
    NavigateApp().run()

