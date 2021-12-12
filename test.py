from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine
from kivymd import images_path
from kivymd.uix.expansionpanel import TwoLineAvatarIconListItem
KV = '''
<Content>
    adaptive_height: True
    MDList:
        id: g
        TwoLineIconListItem:
            text: "(050)-123-45-67"
            secondary_text: "Mobile"
    
            IconLeftWidget:
                icon: 'phone'
    
        TwoLineIconListItem:
            text: "(050)-123-45-67"
            secondary_text: "Mobile"
    
            IconLeftWidget:
                icon: 'phone'
        TwoLineIconListItem:
            text: "(050)-d-45-67"
            secondary_text: "Mobile"
            on_press: root.git()
            IconLeftWidget:
                icon: 'phone'

ScrollView:

    MDGridLayout:
        id: box
        cols: 1
        adaptive_height: True
'''


class Content(MDBoxLayout):
    def git(self):

        self.ids["g"].add_widget(
            TwoLineAvatarIconListItem(
                text="hello!"
            )
        )


class Test(MDApp):
    def build(self):
        for i in range(10):
            g = Content()
            g.ids["g"].add_widget(
                                        TwoLineAvatarIconListItem(
                                            text="hello!"
                                        )
                                    )
        return Builder.load_string(KV)

    def on_start(self):

        self.root.ids.box.add_widget(

            MDExpansionPanel(
                icon=f"{images_path}kivymd.png",
                content=Content(),
                panel_cls=MDExpansionPanelThreeLine(
                    text="Text",
                    secondary_text="Secondary text",
                    tertiary_text="Tertiary text",
                )
            )
        )


Test().run()