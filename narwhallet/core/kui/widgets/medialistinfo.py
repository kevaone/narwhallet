from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.uix.screenmanager import ScreenManager
from narwhallet.core.kui.widgets.nwimage import Nwimage


class MediaListInfo(BoxLayout):
    name = StringProperty()
    cid = StringProperty()
    pin_date = StringProperty()
    pin_status = StringProperty()
    thumbnail = Nwimage()
    thumbnail_source = StringProperty()
    mouse_hover = BooleanProperty(False)
    background_color = ListProperty([25/255, 27/255, 27/255, 1])
    hover_color = ListProperty([136/255, 136/255, 136/255, 1])
    sm = ScreenManager()
