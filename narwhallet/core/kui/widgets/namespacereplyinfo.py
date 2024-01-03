from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty


class NamespaceReplyInfo(BoxLayout):
    key = StringProperty()
    data = StringProperty()
    background_color = ListProperty()
    hover = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(NamespaceReplyInfo, self).__init__(**kwargs)

        # Window.bind(mouse_pos=self.on_mouse_pos)

    def sizer(self):
        height = 0
        for child in self.children:
            height += child.size[1]
        self.height = height

    def on_mouse_pos(self, window, pos):
        if self.collide_point(pos[0], pos[1]):
            if self.hover is False:
                self.background_color = [146/255, 149/255, 149/255, 1]
                self.hover = True
        else:
            if self.hover is True:
                self.background_color = [54/255, 58/255, 59/255, 1]
                self.hover = False
