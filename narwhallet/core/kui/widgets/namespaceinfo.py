from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty


class NamespaceInfo(BoxLayout):
    key = StringProperty()
    data = StringProperty()
    sm = ObjectProperty(None)

    def sizer(self):
        height = 0
        for child in self.children:
            height += child.texture_size[1]
        self.height = height
