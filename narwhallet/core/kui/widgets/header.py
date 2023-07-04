from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout

class Header(GridLayout):
    value = StringProperty() #Nwlabel()

    def __init__(self, **kwargs):
        super(Header, self).__init__(**kwargs)
