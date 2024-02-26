from kivy.uix.image import AsyncImage
from kivy.properties import StringProperty

class Nwmarketimage(AsyncImage):
    image_path = StringProperty()

    def __init__(self, **kwargs):
        super(Nwmarketimage, self).__init__(**kwargs)

    def _on_source_load(self, value):
        if self._coreimage is None:
            return
        image = self._coreimage.image
        if not image:
            return
        self.texture = image.texture
        self.dispatch('on_load')
