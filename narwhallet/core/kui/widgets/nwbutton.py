from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty


class Nwbutton(Button):
    icon = ObjectProperty(None)
    icon_size = (0,0)
    icon_padding = NumericProperty(0)
    hover = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(Nwbutton, self).__init__(**kwargs)

        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, window, pos):
        if self.collide_point(pos[0], pos[1]):
            if self.hover is False and self.disabled is False:
                self.background_color = [146/255, 149/255, 149/255, 1]
                Window.set_system_cursor('hand')
                self.hover = True
        else:
            if self.hover is True:
                self.background_color = [54/255, 58/255, 59/255, 1]
                Window.set_system_cursor('arrow')
                self.hover = False
