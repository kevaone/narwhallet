from copy import deepcopy
from functools import partial
import json
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
# from narwhallet.core.kcl.file_utils import ConfigLoader
from kivy.properties import StringProperty
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.nwpasswordpopup import Nwpasswordpopup
from narwhallet.core.kui.widgets.nwtogglebutton import Nwtogglebutton
from narwhallet.core.kui.widgets.nwseparator import Nwseparator


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
    wallets = Spinner()
    namespaces = Spinner()
    btn_save = Nwbutton()
    btn_home = Nwbutton()
    lock_timeout = TextInput()

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def load_settings(self):
        self.settings = deepcopy(self.app.ctrl.settings)
        self.owners = {}
        self.btn_save.disabled = True
        self.btn_save.icon = 'narwhallet/core/kui/assets/disabled_save.png'
        self.btn_home._text = 'Home'

        if self.settings.show_change:
            self.show_change.state = 'down'
        else:
            self.show_change.state = 'normal'

        _alang = []
        for _lang in self.app.ctrl.lang_dat.data['available']:
            _alang.append(_lang[0])

        self.lang.values = _alang
        self.lang.text = self.app.ctrl.lang_dat.data['available'][self.app.ctrl.lang_dat.data['active']][0]

        self.lock_timeout.text = str(self.settings.auto_lock_timer)
        self.app.ctrl.kex.active_peer = self.settings.primary_peer

        for _p in self.settings.electrumx_peers:
            self.app.ctrl.kex.add_peer(_p[1], _p[2], _p[3], _p[4])

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

        _wallets = ['']
        for _w in self.app.ctrl.wallets.wallets:
            _wallets.append(_w.name)

        self.wallets.values = _wallets
        self.wallets.text = self.settings.default_wallet

        if self.wallets.text == '':
            self.namespaces.disabled = True
        else:
            self.owners[self.settings.default_namespace[0]] = self.settings.default_namespace[1]
            self.namespaces.text = self.settings.default_namespace[0]
            self.namespaces.disabled = False

    def wallet_changed(self):
        if self.wallets.text == '':
            self.settings.set_default_wallet(self.wallets.text)
            self.namespaces.values = ['']
            self.namespaces.disabled = True
            self.namespaces.text = ''
            self.settings.set_default_namespace(['', ''])
            self._save_settings()
            return

        self.wallet = self.app.ctrl.wallets.get_wallet_by_name(self.wallets.text)

        if self.wallet is None:
            return

        if self.wallet.state_lock == 1:
            if self.wallet.locked is True:
                pass_popup = Nwpasswordpopup(wallet=self.wallet)
                pass_popup.bind(next=partial(self._wallet_changed))
                pass_popup.open()
                return
        
        self._wallet_changed()

    def _wallet_changed(self, *args):
        self.owners = {}
        self.wallet = self.app.ctrl.wallets.get_wallet_by_name(self.wallets.text)
        if self.wallet is None:
            return

        _ns_list = ['']

        for address in self.wallet.addresses.addresses:
            for ns in address.namespaces:
                _ns_list.append(ns['namespaceid'])
                self.owners[ns['namespaceid']] = address.address

        for address in self.wallet.change_addresses.addresses:
            for ns in address.namespaces:
                _ns_list.append(ns['namespaceid'])
                self.owners[ns['namespaceid']] = address.address

        self.namespaces.values = _ns_list
        self.namespaces.disabled = False
        self.namespaces.text = ''
        self.settings.set_default_wallet(self.wallets.text)
        self._save_settings()

    def ns_changed(self):
        if self.namespaces.text != '':
            self.settings.set_default_namespace([self.namespaces.text, self.owners[self.namespaces.text]])
        else:
            self.settings.set_default_namespace(['', ''])
        self._save_settings()

    def update_host(self):
        self.settings.electrumx_peers[0][1] = self.iserver_host.text
        self._save_settings()

    def update_port(self):
        self.settings.electrumx_peers[0][2] = self.iserver_port.text
        self._save_settings()

    def update_althost(self):
        self.settings.electrumx_peers[1][1] = self.iserver_althost.text
        self._save_settings()

    def update_altport(self):
        self.settings.electrumx_peers[1][2] = self.iserver_altport.text
        self._save_settings()

    def update_ipfs(self):
        self.settings.ipfs_providers[0] = self.ipfs_gateway.text
        self._save_settings()

    def update_altipfs(self):
        self.settings.ipfs_providers[1] = self.ipfs_gateway_alt.text
        self._save_settings()

    def update_active(self, value):
        self.settings.set_primary_peer(value)
        self._save_settings()
        self.connection_status = self.app.ctrl.kex.peers[value].connect()

    def update_ipfs_active(self, value):
        self.settings.set_primary_ipfs_provider(value)
        self._save_settings()

    def update_lock_timeout(self):
        try:
            self.settings.set_auto_lock_timer(int(self.lock_timeout.text))
            self._save_settings()
        except ValueError as Ex:
            # TODO Set font color to red
            pass

    def update_ssl_option(self, server, option, setting):
        if option not in (3, 4):
            return

        if isinstance(setting, bool) is False:
            return

        self.settings.electrumx_peers[server][option] = setting
        self._save_settings()

    def update_show_change_option(self):
        if self.show_change.state == 'down':
            self.settings.set_show_change(True)
        else:
            self.settings.set_show_change(False)
        
        self._save_settings()

    def _save_settings(self):
        if self.settings.to_dict() == self.app.ctrl.settings.to_dict() and self.app.ctrl.lang_dat.data['active'] == self.lang.values.index(self.lang.text):
            self.btn_home._text = 'Home'
            self.btn_save.disabled = True
            self.btn_save.icon = 'narwhallet/core/kui/assets/disabled_save.png'
            return
        
        self.btn_home._text = 'Cancel'
        self.btn_save.disabled = False
        self.btn_save.icon = 'narwhallet/core/kui/assets/save.png'

    def save_settings(self):
        self.app.ctrl.set_dat.save(json.dumps(self.settings.to_dict()))
        self.app.ctrl.set_dat.load()
        self.app.ctrl.settings.from_dict(self.app.ctrl.set_dat.data)

        self.app.ctrl.lang_dat.data['active'] = self.lang.values.index(self.lang.text)
        self.app.ctrl.lang_dat.save(json.dumps(self.app.ctrl.lang_dat.data, ensure_ascii=False))
        self.btn_home._text = 'Home'
        self.btn_save.disabled = True

    def update_lang(self):
        self.app.lang = self.lang.values.index(self.lang.text)
        self._save_settings()

    def cancel(self):
        self.app.lang = self.app.ctrl.lang_dat.data['active']
        self.lang.text = self.app.ctrl.lang_dat.data['available'][self.app.ctrl.lang_dat.data['active']][0]
        self.manager.current = 'home_screen'
