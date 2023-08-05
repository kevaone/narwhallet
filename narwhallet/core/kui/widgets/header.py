from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from narwhallet.core.kui.widgets.nwimage import Nwimage

class Header(GridLayout):
    value = StringProperty()
    logo = Nwimage()

    def __init__(self, **kwargs):
        super(Header, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.logo.collide_point(touch.x, touch.y) and touch.is_mouse_scrolling is False:
            if self.value == '':
                self.parent.parent.manager.about_screen.populate()
            else:
                self.parent.parent.manager.home_screen.populate()
                self.parent.parent.manager.current = 'home_screen'
            return
        return super(Header, self).on_touch_down(touch)