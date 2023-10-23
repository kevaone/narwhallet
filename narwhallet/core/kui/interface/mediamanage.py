import os
from kivy.uix.screenmanager import Screen
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwgrid import Nwgrid


class MediaManageScreen(Screen):
    media_list = Nwgrid()
    header = Header()
    home_directory = os.path.expanduser('~')

    def populate(self):
        self.header.value = 'My Media'
        self.media_list.data = []

        for media in self.manager.mymedia.to_dict_list():
            _ns = {
                'name': str(media['name']),
                'cid': str(media['cid']),
                'pin_date': str(media['pin_date']),
                'pin_status': str(media['pin_status']),
                'sm': self.manager}
            self.media_list.data.append(_ns)

        self.manager.current = 'mediamanage_screen'
