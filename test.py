from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch

KV = '''    
RecycleView:
    #size_hint: 1,1
    #pos_hint: {"center_x": .5}
    #Удвоение майнинга
    MDList:
        ThreeLineAvatarIconListItem:
            text: str(app.d)
            on_press: app.callback()
            IconLeftWidget:
                icon: "cog"
        
            YourContainer:
                id: container
        
                MDIconButton:
                    icon: "minus"
        
                MDIconButton:
                    icon: "plus"
'''


class YourContainer(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True


class MainApp(MDApp):
    def build(self):
        self.d = 0
        return Builder.load_string(KV)
    def callback(self):
        self.d +=1
MainApp().run()