from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.properties import StringProperty

class Nwnsimage(BoxLayout):
    image_path = StringProperty()
    image = Image()

    def __init__(self, **kwargs):
        super(Nwnsimage, self).__init__(**kwargs)
