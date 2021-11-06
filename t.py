## Sample Python application demonstrating that
## how to create button using image in kivy 

##################################################      
# import kivy module 
import kivy

# this restrict the kivy version i.e 
# below this kivy version you cannot 
# use the app or software 
kivy.require("1.9.1")

# base Class of your App inherits from the App class. 
# app:always refers to the instance of your application 
from kivy.app import App

# creates the button in kivy 
# if not imported shows the error 
from kivy.uix.button import Button

# this restrict the kivy version i.e   
# below this kivy version you cannot   
# use the app or software   
kivy.require('1.9.0')

# to change the kivy default settings we use this module config 
from kivy.config import Config

# 0 being off 1 being on as in true / false 
# you can use 0 or 1 && True or False 
Config.set('graphics', 'resizable', True)


# class in which we are creating the imagebutton 
class ButtonApp(App):

    def build(self):
        # create a fully styled functional button
        # Adding images normal.png and down.png
        btn = Button(text="Push Me !",
                     background_normal='button_normal.jpg',
                     background_down='button_down.jpg',
                     size_hint=(.9, .1),
                     pos_hint={"x": 0.35, "y": 0.3}
                     )

        # bind() use to bind the button to function callback 
        btn.bind(on_press=self.callback)
        return btn

        # callback function tells when button pressed

    def callback(self, event):
        print("button pressed")
        print('Yoooo !!!!!!!!!!!')

    # creating the object root for ButtonApp() class


root = ButtonApp()

# run function runs the whole program 
# i.e run() method which calls the target 
# function passed to the constructor. 
root.run()