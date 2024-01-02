from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.gridlayout import GridLayout
from narwhallet.core.kui.widgets.nwimage import Nwimage

class Header(GridLayout):
    value = StringProperty()
    logo = Nwimage()
    is_popup = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(Header, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.logo.collide_point(touch.x, touch.y) and touch.is_mouse_scrolling is False and self.is_popup is False:
            if self.value == '':
                self.parent.parent.manager.about_screen.populate()
            else:
                self.parent.parent.manager.home_screen.populate()
                self.parent.parent.manager.current = 'home_screen'
            return
        return super(Header, self).on_touch_down(touch)
