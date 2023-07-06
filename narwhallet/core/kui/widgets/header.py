from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout

class Header(GridLayout):
    value = StringProperty()

    def __init__(self, **kwargs):
        super(Header, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.parent.parent.manager.home_screen.populate()
            self.parent.parent.manager.current = 'home_screen'
            return
        return super(Header, self).on_touch_down(touch)