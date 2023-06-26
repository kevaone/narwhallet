from kivy.uix.floatlayout import FloatLayout
# from kivy.animation import Animation
from kivy.properties import NumericProperty, BooleanProperty


class LoadingSpinner(FloatLayout):
    angle = NumericProperty(0)
    rotating = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(LoadingSpinner, self).__init__(**kwargs)

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.parent.parent.parent.update_wallet()
            return
        return super(LoadingSpinner, self).on_touch_down(touch)
