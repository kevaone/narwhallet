from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.label import Label


class Nwlabel(Label):
    _text = StringProperty('')

    def __init__(self, **kwargs):
        super(Nwlabel, self).__init__(**kwargs)

        Clock.schedule_once(self._bind)

    def _bind(self, dt):
        app = App.get_running_app()
        app.bind(lang=self.translate_text)
        self.translate_text()

    def translate_text(self, *args):
        app = App.get_running_app()
        self.text = app.translate_text(self._text)

    def on__text(self, *args):
        # print('args', *args)
        self.translate_text()
