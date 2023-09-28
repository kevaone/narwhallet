from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty


class AuctionInfo(BoxLayout):
    auction_namespace = StringProperty()
    auction_namespace_addr = StringProperty()
    shortcode = StringProperty()
    nsname = StringProperty()
    bid = StringProperty()
    time = StringProperty()
    transaction = StringProperty()
    sm = ObjectProperty(None)

    def sizer(self):
        height = 0
        for child in self.children:
            height += child.texture_size[1]
        self.height = height
