from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, StringProperty


class Spbutton(Button):
    icon = ObjectProperty(None)
    icon_size = (dp(51), dp(25))
    icon_padding = NumericProperty(0)
    hover = BooleanProperty(False)
    _text = StringProperty('')
    _sort = StringProperty('')

    def __init__(self, **kwargs):
        super(Spbutton, self).__init__(**kwargs)

        Window.bind(mouse_pos=self.on_mouse_pos)
        Clock.schedule_once(self._bind)
        self.texture_size = (0, 0)

    def on_mouse_pos(self, window, pos):
        if self.collide_point(pos[0], pos[1]):
            if self.hover is False and self.disabled is False:
                self.background_color = [146/255, 149/255, 149/255, 1]
                self.hover = True
        else:
            if self.hover is True and self.disabled is False:
                self.background_color = [54/255, 58/255, 59/255, 1]
                self.hover = False

    # def on_hover(self, *args):
    #     if self.hover is True:
    #         Window.set_system_cursor('hand')
    #     else:
    #         Window.set_system_cursor('arrow')

    def _bind(self, dt):
        app = App.get_running_app()
        app.bind(lang=self.translate_text)
        self.translate_text()

    def translate_text(self, *args):
        app = App.get_running_app()
        self.text = app.translate_text(self._text)

    def on__text(self, *args):
        self.translate_text()
