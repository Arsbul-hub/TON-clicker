from kivy.base import runTouchApp
from kivy.lang import Builder


kv = '''
<ButImage@ButtonBehavior+AsyncImage>

FloatLayout:
    ButImage:
        id: but
        size_hint: .5, .5
        size_hint: (.49,.49) if self.state == 'down' else (.5,.5)
        allow_stretch: True
        keep_ratio: True
        source: 'doubling.png'
        Label:
            center: but.center
            text: "Normal" if but.state == 'normal' else 'down'


'''

if __name__ == '__main__':
    runTouchApp(Builder.load_string(kv))