from kivy.uix.modalview import ModalView
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwlabel import Nwlabel


class NamespaceInfoPopup(ModalView):
    namespaceid = Nwlabel()
    shortcode = Nwlabel()
    creator = Nwlabel()
    namespace_name = Nwlabel()
    owner = Nwlabel()
    header = Header()

    def populate(self):
        pass
