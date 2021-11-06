# Program to explain how to use scroll view in kivy

# import kivy module
import kivy

# base Class of your App inherits from the App class.
# app:always refers to the instance of your application
from kivy.app import App

# this restrict the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require('1.9.0')

# The Label widget is for rendering text
from kivy.uix.label import Label

# The ScrollView widget provides a scrollable view
from kivy.uix.scrollview import ScrollView

# Property that represents a string value
from kivy.properties import StringProperty

# Static main function that starts the application loop.
from kivy.base import runTouchApp

# Builder is a global Kivy instance used in
# widgets that you can use to load other
# kv files in addition to the default ones.
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
# Build the .kv file
Builder.load_string('''

# Define the scroll view
<ScrollableLabel>:
    BoxLayout:
        ScrollView:
            
            Label:
                text: "root.textroot.textroot.textroot.textroot.textroot.textroot.textroot.textroot.textroot.textroot.textroot.textroot.textroot.textroot.text"
                #font_size: 50
                #text_size: self.width, None
                size_hint_y: None
                #height: self.texture_size[1]
''')


# Define scrollview class
class ScrollableLabel(BoxLayout):
    text = StringProperty('ScrollViewScrollViewScrollViewScrollViewScrollViewScrollViewScrollViewScrollViewScrollViewScrollViewScrollViewScrollViewScrollViewScrollViewScrollViewScrollViewScrollViewScrollViewScrollViewScrollView')


# run the App
runTouchApp(ScrollableLabel())