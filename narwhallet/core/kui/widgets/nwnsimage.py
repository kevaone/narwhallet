from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.properties import StringProperty

class Nwnsimage(BoxLayout):
    image_path = StringProperty()
    image = AsyncImage()

    def __init__(self, **kwargs):
        super(Nwnsimage, self).__init__(**kwargs)

    def on_size(self, *args):
        if args[1][0] < 512:
            self.height = args[1][0]
        else:
            self.height = 512
