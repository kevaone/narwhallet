import json
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
# from narwhallet.core.kcl.file_utils import ConfigLoader
from kivy.properties import StringProperty
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwtogglebutton import Nwtogglebutton


class SettingsScreen(Screen):
    iserver_host = TextInput()
    iserver_port = TextInput()
    iserver_althost = TextInput()
    iserver_altport = TextInput()
    iserver_ssl_0 = Nwtogglebutton()
    iserver_verify_0 = Nwtogglebutton()
    iserver_altssl_0 = Nwtogglebutton()
    iserver_altverify_0 = Nwtogglebutton()
    iserver_ssl_1 = Nwtogglebutton()
    iserver_verify_1 =Nwtogglebutton()
    iserver_altssl_1 = Nwtogglebutton()
    iserver_altverify_1 = Nwtogglebutton()
    ipfs_gateway = TextInput()
    ipfs_gateway_alt = TextInput()
    iserver_ipfs_0 = TextInput()
    iserver_ipfs_1 = TextInput()
    iserver_active_0 = Nwtogglebutton()
    iserver_active_1 = Nwtogglebutton()
    header = Header()
    show_change = Nwtogglebutton()
    connection_status = StringProperty()
    lang = Spinner()

    def load_settings(self):
        self.app = App.get_running_app()
        self.settings = self.app.ctrl.settings

        if self.settings.show_change:
            self.show_change.state = 'down'
        else:
            self.show_change.state = 'normal'

        _alang = []
        for _lang in self.app.ctrl.lang_dat.data['available']:
            _alang.append(_lang[0])

        self.lang.values = _alang
        self.lang.text = self.app.ctrl.lang_dat.data['available'][self.app.ctrl.lang_dat.data['active']][0]

        self.manager.kex.active_peer = self.settings.primary_peer

        for _p in self.settings.electrumx_peers:
            self.manager.kex.add_peer(_p[1], _p[2], _p[3], _p[4])

        self.iserver_host.text = self.settings.electrumx_peers[0][1]
        self.iserver_port.text = self.settings.electrumx_peers[0][2]
        self.iserver_althost.text = self.settings.electrumx_peers[1][1]
        self.iserver_altport.text = self.settings.electrumx_peers[1][2]

        if bool(self.settings.electrumx_peers[0][3]) is True:
            self.iserver_ssl_0.state = 'down'
            self.iserver_ssl_1.state = 'normal'
        else:
            self.iserver_ssl_0.state = 'normal'
            self.iserver_ssl_1.state = 'down'

        if bool(self.settings.electrumx_peers[0][4]) is True:
            self.iserver_verify_0.state = 'down'
            self.iserver_verify_1.state = 'normal'
        else:
            self.iserver_verify_0.state = 'normal'
            self.iserver_verify_1.state = 'down'

        if self.settings.primary_peer == 0:
            self.iserver_active_0.state = 'down'
            self.iserver_active_1.state = 'normal'
        else:
            self.iserver_active_0.state = 'normal'
            self.iserver_active_1.state = 'down'

        if bool(self.settings.electrumx_peers[1][3]) is True:
            self.iserver_altssl_0.state = 'down'
            self.iserver_altssl_1.state = 'normal'
        else:
            self.iserver_altssl_0.state = 'normal'
            self.iserver_altssl_1.state = 'down'

        if bool(self.settings.electrumx_peers[1][4]) is True:
            self.iserver_altverify_0.state = 'down'
            self.iserver_altverify_1.state = 'normal'
        else:
            self.iserver_altverify_0.state = 'normal'
            self.iserver_altverify_1.state = 'down'

        self.ipfs_gateway.text = self.settings.ipfs_providers[0]
        self.ipfs_gateway_alt.text = self.settings.ipfs_providers[1]

        if self.settings.primary_ipfs_provider == 0:
            self.iserver_ipfs_0.state = 'down'
            self.iserver_ipfs_1.state = 'normal'
        else:
            self.iserver_ipfs_0.state = 'normal'
            self.iserver_ipfs_1.state = 'down'

        # _special_keys = ConfigLoader(os.path.join(self.user_path,
        #                                           'special_keys.json'))
        # _special_keys.load()

    def update_host(self):
        self.settings.electrumx_peers[0][1] = self.iserver_host.text
        self.save_settings()

    def update_port(self):
        self.settings.electrumx_peers[0][2] = self.iserver_port.text
        self.save_settings()

    def update_althost(self):
        self.settings.electrumx_peers[1][1] = self.iserver_althost.text
        self.save_settings()

    def update_altport(self):
        self.settings.electrumx_peers[1][2] = self.iserver_altport.text
        self.save_settings()

    def update_ipfs(self):
        self.settings.ipfs_providers[0] = self.ipfs_gateway.text
        self.save_settings()

    def update_altipfs(self):
        self.settings.ipfs_providers[1] = self.ipfs_gateway_alt.text
        self.save_settings()

    def update_active(self, value):
        self.settings.set_primary_peer(value)
        self.save_settings()
        self.connection_status = self.manager.kex.peers[value].connect()

    def update_ipfs_active(self, value):
        self.settings.set_primary_ipfs_provider(value)
        self.save_settings()

    def update_ssl_option(self, server, option, setting):
        if option not in (3, 4):
            return

        if isinstance(setting, bool) is False:
            return

        self.settings.electrumx_peers[server][option] = setting
        self.save_settings()

    def update_show_change_option(self):
        if self.show_change.state == 'down':
            self.settings.set_show_change(True)
        else:
            self.settings.set_show_change(False)
        
        self.save_settings()

    def save_settings(self):
        self.app.ctrl.set_dat.save(json.dumps(self.settings.to_dict()))

    def update_lang(self):
        self.app.ctrl.lang_dat.data['active'] = self.lang.values.index(self.lang.text)
        self.app.ctrl.lang_dat.save(json.dumps(self.app.ctrl.lang_dat.data))
        self.app.lang = self.app.ctrl.lang_dat.data['active']
