from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty


class Txoutputlistpopup(ModalView):
    vout = ObjectProperty()

    def __init__(self, **kwargs):
        super(Txoutputlistpopup, self).__init__(**kwargs)
