from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

# our main window class
class Player(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.music = SoundLoader.load('test.mp3')
    def play(self):
        self.music.play()
    def pause(self):
        self.music.pause()
class MusicWindow(App):

    def build(self):
        # load the mp3 music


        # check the exisitence of the music

        return Player()


if __name__ == "__main__":
    window = MusicWindow()
    window.run()