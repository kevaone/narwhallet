from kivy.uix.button import Button
from kivy.properties import (ObjectProperty, NumericProperty)


class Nwbutton(Button):
    icon = ObjectProperty(None)
    icon_size = (0,0)
    icon_padding = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Nwbutton, self).__init__(**kwargs)
