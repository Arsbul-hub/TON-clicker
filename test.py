# import kivy module
import kivy

# this restricts the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require("1.9.1")

# base Class of your App inherits from the App class.
# app:always refers to the instance of your application
from kivy.app import App

# To work with Animation you must have to import it
from kivy.animation import Animation

# The Button is a Label with associated
# actions that are triggered when the button
# is pressed (or released after a click/touch).
from kivy.uix.button import Button

# Create the App class
class TestApp(App):

   # Defining the function in which animations are added

    def animate(self, instance):
        # create an animation object. This object could be stored
        # and reused each call or reused across different widgets.
        # += is a sequential step, while &= is in parallel
        animation = Animation(pos =(100, 100), t ='out_bounce')
        animation += Animation(pos =(200, 100), t ='out_bounce')
        animation &= Animation(size =(500, 500))
        animation += Animation(size =(100, 50))

        # apply the animation on the button, passed in the "instance" argument
        # Notice that default 'click' animation (changing the button
        # color while the mouse is down) is unchanged.
        animation.start(instance)

    def build(self):
        # create a button, and  attach animate()
        # method as a on_press handler
        button = Button(size_hint =(None, None), text ='plop',
                        on_press = self.animate)
        return button

# run the App
if __name__ == '__main__':
    TestApp().run()