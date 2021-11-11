from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.label import Label

kv = '''
BoxLayout:
    ScrollView:
        GridLayout:
            cols: 1
            id: target
            size_hint: 1, None
            height: self.minimum_height
    Button:
        text: 'add 100'
        on_press: app.consumables.extend(range(100))
'''

class ProdConApp(App):
    consumables = ListProperty([])

    def build(self):
        Clock.schedule_interval(self.consume, 0)
        return Builder.load_string(kv)

    def consume(self, *args):
        if self.consumables:
            item = self.consumables.pop(0)
            label = Label(text='%s' % item)
            self.root.ids.target.add_widget(label)

if __name__ == '__main__':
    ProdConApp().run()