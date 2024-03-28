from kivy.uix.modalview import ModalView
from kivy.uix.filechooser import FileChooserListView
from kivy.properties import StringProperty


class Mediabrowsepopup(ModalView):
    file_chooser = FileChooserListView()
    home_directory = StringProperty('')
    psbt = StringProperty(None)

    def __init__(self, **kwargs):
        super(Mediabrowsepopup, self).__init__(**kwargs)

    def popen(self, initial_path):
        self.home_directory = initial_path
        self.open()

    def load(self, path, selection):
        self.psbt = selection[0]
        self.dismiss()
