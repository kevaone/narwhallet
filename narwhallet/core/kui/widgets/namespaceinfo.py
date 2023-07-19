from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty)


class NamespaceInfo(BoxLayout):
    key = StringProperty()
    data = StringProperty()
    sm = ObjectProperty(None)

    def sizer(self):
        height = 0
        for child in self.children:
            height += child.texture_size[1]
            height += 2 * child.padding_y
        self.height = height
