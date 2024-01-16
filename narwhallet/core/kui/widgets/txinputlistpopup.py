from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty


class Txinputlistpopup(ModalView):
    vin = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Txinputlistpopup, self).__init__(**kwargs)
