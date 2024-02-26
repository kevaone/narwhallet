import base64  # TODO Check and add if missing to ConvUtils
import datetime
import json
import os
import math
import sys
import time

from typing import List, Optional
from narwhallet.core.kcl.bip_utils.base58.base58 import Base58Encoder

from narwhallet.core.kex import KEXclient
from narwhallet.core.kex.cmd import _custom, _transaction
from narwhallet.core.ksc import Scripts
from narwhallet.core.ksc.utils import Ut
# from narwhallet.core.kcl.cache import MCache
from narwhallet.core.kcl.wallet import MAddress, MAddresses, MWallet
from narwhallet.core.kcl.transaction import (keva_psbt,
                                             MTransaction,
                                             MTransactionInput,
                                             MTransactionOutput,
                                             MScriptPubKey)
from narwhallet.core.kcl.bip_utils.base58 import Base58Decoder


class MShared():
    @staticmethod
    def get_resource_path(file):
        if hasattr(sys, "_MEIPASS"):
            _path = os.path.join(sys._MEIPASS, 'assets')
        else:
            _path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 '../core/kui/ux/assets')
        _path = os.path.join(_path, file)

        return _path

    @staticmethod
    def get_timestamp(timestamp: float = 0.0):
        if timestamp == 0.0:
            _now = time.time()
        else:
            _now = timestamp
        _dt = (datetime.datetime
               .fromtimestamp(_now)
               .strftime('%Y-%m-%d %H:%M:%S'))
        return (_now, _dt)

    @staticmethod
    def sort_dict(item):
        return item['time']

    # TODO Remove this, should come from file_uitls
    @staticmethod
    def load_message_file(file_path: str):
        _data = b''
        with open(file_path, mode='rb') as _file:
            _data = _file.read()
        return _data

    @staticmethod
    def batch_cmds(commands: list) -> list:
        _batches = []
        _batch_counter = 0
        _bd = b'['
        for i in commands:
            if _bd != b'[':
                _bd = _bd + b','
            _bd = _bd + i.replace(b'\n', b'')
            # NOTE 5 seems stable for verbose tx batch
            if _batch_counter == 50:
                _batch_counter = 0
                _bd = _bd + b']\n'
                _batches.append(_bd)
                _bd = b'['
            else:
                _batch_counter += 1
        _bd = _bd + b']\n'
        _batches.append(_bd)
        return _batches

    @staticmethod
    def __get_batch(batch: bytes, kex: KEXclient):
        _results = kex.call_batch(batch)
        _results = json.loads(_results)
        _results = MShared.__test_batch_for_error(batch, _results, kex)
        return _results

    @staticmethod
    def __test_batch_for_error(batch, results, kex: KEXclient):
        if not isinstance(results, list):
            # print('type error', results)
            time.sleep(5)
            results = MShared.__get_batch(batch, kex)
        else:
            if len(results) > 0:
                # HACK 1 and done test for excessive useage
                if 'error' in results[0]:
                    if 'excessive' in results[0]['error']['message']:
                        time.sleep(5)
                        results = MShared.__get_batch(batch, kex)

        return results

    @staticmethod
    def get_block_count(kex: KEXclient):
        _ = kex.peers[kex.active_peer].connect()
        _block_count = kex.call(kex.api.blockchain_block.count(kex.id))
        kex.peers[kex.active_peer].disconnect()
        kex.id += 1
        if _block_count != '':
            _block_count = json.loads(_block_count)['result']
        return _block_count

    @staticmethod
    def get_fee_rate(kex: KEXclient) -> int:
        _ = kex.peers[kex.active_peer].connect()
        _fee = kex.call(kex.api.blockchain.estimatefee(2, kex.id))
        kex.peers[kex.active_peer].disconnect()
        kex.id += 1
        if _fee != '':
            _fee = json.loads(_fee)['result']
            _fee = math.ceil((_fee*100000000)/1024)
        else:
            _fee = -1

        return _fee

    @staticmethod
    def broadcast(tx: str, kex: KEXclient) -> tuple:
        _ = kex.peers[kex.active_peer].connect()
        _result = kex.call(kex.api.bc_tx.broadcast(tx, kex.id))
        kex.peers[kex.active_peer].disconnect()
        kex.id += 1
        if _result != '':
            _result = json.loads(_result)['result']
            if 'error' in _result:
                if _result['error'] != None:
                    # {error:{code, message}}
                    _msg = _result['error']
                    _msg_t = 1
                else:
                    _msg = 'TX Sent!'
                    _msg_t = 2
            else:
                _msg = 'TX Sent!'
                _msg_t = 2
        else:
            _msg = 'Call Error'
            _msg_t = 1

        return (_msg_t, _msg)

    @staticmethod
    def get_addresses(wallet: MWallet, kex: KEXclient):
        _th: list = []
        _tid: dict = {}
        _th, _tid = MShared._get_addresses_cmds(wallet, 1, _th, _tid, kex)
        _th, _tid = MShared._get_addresses_cmds(wallet, 0, _th, _tid, kex)
        _batches = MShared.batch_cmds(_th)
        MShared._get_addresses(wallet, _batches, _tid, kex)
        # NOTE Clip off unused addresses
        MShared._clip_unused_addresses(wallet, 1)
        MShared._clip_unused_addresses(wallet, 0)

    @staticmethod
    def _clip_unused_addresses(wallet: MWallet, chain: int):
        if chain == 1:
            _addrs = wallet.addresses
        elif chain == 0:
            _addrs = wallet.change_addresses

        while True:
            _t = _addrs._addresses[-1].history
            if _t == []:
                del _addrs._addresses[-1]
            else:
                break

            if len(_addrs._addresses) == 0:
                break

        _len = len(_addrs._addresses)
        _addrs._names = {}
        for _idx, _a in enumerate(_addrs._addresses):
            _addrs._names[_a.address] = _idx
        
        if chain == 0:
            wallet.set_change_index(_len)
        elif chain == 1:
            wallet.set_account_index(_len)

    @staticmethod
    def _get_addresses_cmds(wallet: MWallet, chain: int, _th: list,
                            _tid: dict, kex: KEXclient):
        if chain == 0:
            _addresses = wallet.change_addresses
        elif chain == 1:
            _addresses = wallet.addresses

        _idx = -1
        for _a in _addresses.addresses:
            # _script_hash = Scripts.AddressScriptHash(_a.address)
            # _script_hash = Scripts.compileToScriptHash(_script_hash, True)
            _idx = _idx + 1
            # NOTE Filter out spent change addresses
            if chain == 0 and _a.balance == 0 and _idx < wallet.change_index - 5:
                continue
            _th.append(kex.api.custom.get_address
                       (_a.address, kex.id))
            _tid[str(kex.id)] = {}
            _tid[str(kex.id)]['address'] = _a.address
            _tid[str(kex.id)]['chain'] = chain
            kex.id = kex.id + 1

        # NOTE Padding to detect used addresses out of wallets current index's
        if len(_addresses.addresses) == 0:
            _scan_pad = 100
        else:
            _scan_pad = 10

        if wallet.kind != 3:
            for _pad in range(0, _scan_pad):
                if chain == 0:
                    _pad_value = len(wallet.change_addresses.addresses) + _pad
                    _addr = wallet.get_change_address_by_index(_pad_value,
                                                               False)
                elif chain == 1:
                    _pad_value = len(wallet.addresses.addresses) + _pad
                    _addr = wallet.get_address_by_index(_pad_value, False)

                # _script_hash = Scripts.AddressScriptHash(_addr)
                # _script_hash = Scripts.compileToScriptHash(_script_hash, True)
                _th.append(kex.api.custom.get_address
                           (_addr, kex.id))
                _tid[str(kex.id)] = {}
                _tid[str(kex.id)]['address'] = _addr
                _tid[str(kex.id)]['chain'] = chain
                _tid[str(kex.id)]['pad'] = _pad_value
                kex.id = kex.id + 1

        return _th, _tid

    @staticmethod
    def _process_addresses(wallet: MWallet, _tid: dict, i: dict):
        _chain = _tid[str(i['id'])]['chain']
        if _chain == 0:
            _addresses = wallet.change_addresses
        else:
            _addresses = wallet.addresses

        _a = _tid[str(i['id'])]['address']
        _ax = _addresses.get_address_index_by_name(_a)
        if _ax == -1:
            if len(i['result']) <= 0:
                return

            _p = _tid[str(i['id'])]['pad']
            while _addresses.count < _p:
                if _chain == 0:
                    wallet.get_unused_change_address()
                else:
                    wallet.get_unused_address()

            if _p == _addresses.count:
                if _chain == 0:
                    wallet.get_change_address_by_index(_p, True)
                else:
                    wallet.get_address_by_index(_p, True)

                _ax = _addresses.get_address_index_by_name(_a)
                _addresses.addresses[_ax].set_history(i['result'][1]['page_results'])
                _addresses.addresses[_ax].set_namespaces(i['result'][2])
                _addresses.addresses[_ax].set_sent(i['result'][0]['sent'])
                _addresses.addresses[_ax].set_received(i['result'][0]['received'])
                _addresses.addresses[_ax].set_balance(i['result'][0]['balance'])
                _addresses.addresses[_ax]._unconfirmed_receive_balance = 0.0
                _addresses.addresses[_ax]._unconfirmed_send_balance = 0.0
                for _r in i['result'][1]['page_results']:
                    if _r['block'] == 'unconfirmed':
                        if 'received' in _r:
                            _addresses.addresses[_ax]._unconfirmed_send_balance = _addresses.addresses[_ax]._unconfirmed_send_balance + Ut.from_sats(_r['value'])
                        else:
                            _addresses.addresses[_ax]._unconfirmed_receive_balance = _addresses.addresses[_ax]._unconfirmed_receive_balance + Ut.from_sats(_r['value'])
        else:
            _addresses.addresses[_ax].set_history(i['result'][1]['page_results'])
            _addresses.addresses[_ax].set_namespaces(i['result'][2])
            _addresses.addresses[_ax].set_sent(i['result'][0]['sent'])
            _addresses.addresses[_ax].set_received(i['result'][0]['received'])
            _addresses.addresses[_ax].set_balance(i['result'][0]['balance'])
            _addresses.addresses[_ax]._unconfirmed_receive_balance = 0.0
            _addresses.addresses[_ax]._unconfirmed_send_balance = 0.0
            for _r in i['result'][1]['page_results']:
                if _r['block'] == 'unconfirmed':
                    if 'received' in _r:
                        _addresses.addresses[_ax]._unconfirmed_send_balance = _addresses.addresses[_ax]._unconfirmed_send_balance + Ut.from_sats(_r['value'])
                    else:
                        _addresses.addresses[_ax]._unconfirmed_receive_balance = _addresses.addresses[_ax]._unconfirmed_receive_balance + Ut.from_sats(_r['value'])

    @staticmethod
    def _get_addresses(wallet: MWallet, batches: list, _tid: dict,
                       kex: KEXclient):
        for batch in batches:
            _h = []
            if batch != b'[]\n':
                _h = MShared.__get_batch(batch, kex)

            if not isinstance(_h, list):
                continue

            for i in _h:
                if str(i['id']) not in _tid:
                    continue

                MShared._process_addresses(wallet, _tid, i)

    @staticmethod
    def _get_address(address: str, kex: KEXclient) -> dict:
        # _script_hash = Scripts.AddressScriptHash(address)
        # _script_hash = Scripts.compileToScriptHash(_script_hash, True)
        _ = kex.peers[kex.active_peer].connect()
        _hist = kex.call(kex.api.custom.get_address
                         (address, kex.id))
        kex.peers[kex.active_peer].disconnect()
        kex.id += 1
        if _hist != '':
            _hist = json.loads(_hist)['result']
        else:
            _hist = []

        return _hist

    @staticmethod
    def get_tx(tx_hash: str, kex: KEXclient, verbose=False):
        _tx = None
        ret = b''
        _ = kex.peers[kex.active_peer].connect()
        ret = kex.call(kex.api.bc_tx.get(tx_hash, verbose, kex.id))
        kex.peers[kex.active_peer].disconnect()
        kex.id += 1
        if ret != '':
            _tx = json.loads(ret)['result']

        return _tx

    @staticmethod
    def get_namespace(_ns, kex: KEXclient) -> dict:
        _ = kex.peers[kex.active_peer].connect()
        _ns_data = kex.call(_custom.get_namespace(_ns, 1))
        kex.peers[kex.active_peer].disconnect()

        if _ns_data != b'':
            _keys = json.loads(_ns_data)
        else:
            _keys = {}

        return _keys

    @staticmethod
    def get_transaction(_tx, kex: KEXclient) -> dict:
        _ = kex.peers[kex.active_peer].connect()
        _tx_data = kex.call(_transaction.get(_tx, True, 1))
        kex.peers[kex.active_peer].disconnect()

        if _tx_data != b'':
            return json.loads(_tx_data)['result']
        
        return {}

    @staticmethod
    def get_shortcode(_shortcode, kex: KEXclient) -> dict:
        _ = kex.peers[kex.active_peer].connect()
        _ns_data = kex.call(_custom.get_shortcode(_shortcode, 1))
        kex.peers[kex.active_peer].disconnect()

        if _ns_data != '':
            _keys = json.loads(_ns_data)
        else:
            _keys = {}

        return _keys

    @staticmethod
    def get_namespace_keys(_ns, kex: KEXclient) -> list:
        try:
            _ns = Ut.bytes_to_hex(Base58Decoder.CheckDecode(_ns))
        except Exception:
            return []

        k_script_hash = Scripts.KevaNamespaceScriptHash(_ns, b'')
        k_script_hash = Scripts.compileToScriptHash(k_script_hash, True)
        _ = kex.peers[kex.active_peer].connect()
        k_hist = kex.call(kex.api.keva.get_keyvalues(k_script_hash,
                                                     -1, kex.id))
        kex.peers[kex.active_peer].disconnect()
        kex.id += 1

        if k_hist != '':
            _keys = json.loads(k_hist)['result']['keyvalues']
        else:
            _keys = []

        return _keys

    @staticmethod
    def _get_namespace_keys(_ns, kex: KEXclient):
        _keys: list = []
        try:
            _ns = Ut.bytes_to_hex(Base58Decoder.CheckDecode(_ns))
        except Exception:
            return _keys

        k_script_hash = Scripts.KevaNamespaceScriptHash(_ns, b'')
        k_script_hash = Scripts.compileToScriptHash(k_script_hash, True)
        _ = kex.peers[kex.active_peer].connect()
        k_hist = kex.call(kex.api.keva.get_keyvalues(k_script_hash,
                                                     -1, kex.id))
        kex.peers[kex.active_peer].disconnect()
        kex.id += 1

        if k_hist == '':
            return _keys

        k_hist = json.loads(k_hist)
        k_hist = k_hist['result']

        for _i in range(0, len(k_hist['keyvalues'])):
            try:
                _k = k_hist['keyvalues'][_i]['key']
                _k = base64.b64decode(_k).decode()
            except Exception:
                _k = base64.b64decode(k_hist['keyvalues'][_i]['key'])
                _k = Ut.bytes_to_hex(_k)

            if k_hist['keyvalues'][_i]['type'] == 'REG':
                _v = _k
                _k = '_KEVA_NS_'
            else:
                try:
                    _v = k_hist['keyvalues'][_i]['value']
                    _v = base64.b64decode(_v).decode()
                except Exception:
                    if k_hist['keyvalues'][_i]['type'] == 'DEL':
                        _v = 'DEL'
                    else:
                        _v = base64.b64decode(k_hist['keyvalues'][_i]['value'])
                        _v = Ut.bytes_to_hex(_v)
            _keys.append([_k, _v, k_hist['keyvalues'][_i]['time']])
        return _keys

    @staticmethod
    def get_ns_key_reactions(txid: str, kex: KEXclient):
        _ = kex.peers[kex.active_peer].connect()
        _responses = kex.call(kex.api.keva.get_keyvalue_reactions(txid, -1,
                                                                  kex.id))
        kex.peers[kex.active_peer].disconnect()
        kex.id += 1
        if _responses == '':
            return []

        _responses = json.loads(_responses)
        _responses = _responses['result']['result']

        for _i in range(0, len(_responses['replies'])):
            try:
                _k = _responses['replies'][_i]['key']
                _k = base64.b64decode(_k).decode()
            except Exception:
                _k = base64.b64decode(_responses['replies'][_i]['key'])
                _k = Ut.bytes_to_hex(_k)

            try:
                _v = _responses['replies'][_i]['value']
                _v = base64.b64decode(_v).decode()
            except Exception:
                if _responses['replies'][_i]['type'] == 'DEL':
                    _v = 'DEL'
                else:
                    _v = base64.b64decode(_responses['replies'][_i]['value'])
                    _v = Ut.bytes_to_hex(_v)

            _responses['replies'][_i]['key'] = _k
            _responses['replies'][_i]['value'] = _v

        return _responses

    # TODO Move types to own class; stubbing as strings here for now
    @staticmethod
    def get_key_type(key, value) -> Optional[str]:
        _type = None
        if key == '_KEVA_NS_':
            _type = 'root_ns'
        elif key == '\x01_KEVA_NS_':
            if 'displayName' in value and 'price' in value and 'addr' in value:
                _type = 'nft_auction'
            else:
                _type = 'root_ns_update'
        elif key[:4] == '0001' and len(key) == 68:
            if value[:10] == '70736274ff':
                _type = 'nft_bid'
            else:
                _type = 'reply'
        elif key[:4] == '0002' and len(key) == 68:
            _type = 'repost'
        elif key[:4] == '0003' and len(key) == 68:
            _type = 'reward'
        elif key[:4] == '0004' and len(key) == 68:
            _type = 'nft_auction'
        elif key[:4] == '0005' and len(key) == 68:
            _type = 'nft_confirm_sell'
        # elif key in self.special_keys:
        #     _type = self.special_keys[key]['tooltip']

        return _type

    @staticmethod
    def convert_to_namespaceid(nsid: str):
        try:
            _id = Base58Encoder.CheckEncode(Ut.hex_to_bytes(nsid))
            return _id
        except Exception:
            return Exception('Invailid Namespaceid')
            
    @staticmethod
    def _decode(value):
        try:
            _d2 = Ut.int_to_bytes(int(value), None, 'little').decode()
        except Exception:
            try:
                _d2 = Ut.hex_to_bytes(value).decode()
            except Exception:
                _d2 = value
                # print('error', _d2, value)
        return _d2

    @staticmethod
    def check_tx_is_bid(tx: str, kex: KEXclient) -> tuple:
        if len(tx) != 64:
            return (False, '', '')

        _tx = MShared.get_tx(tx, kex, True)

        if _tx is None:
            return (False, '', '')

        _asm = _tx['vout'][0]['scriptPubKey']['asm'].split(' ')
        if _asm[0] != 'OP_KEVA_PUT':
            return (False, '', '')

        _key = MShared._decode(_asm[2])
        _value = MShared._decode(_asm[3])
        if MShared.get_key_type(_key, _value) != 'nft_bid':
            return (False, '', '')

        _ns = MShared.convert_to_namespaceid(_asm[1])

        return (True, _ns, _value)

    @staticmethod
    def ipfs_upload(file: str, data: str, kex: KEXclient) -> dict:
        _ = kex.peers[kex.active_peer].connect()
        _file_hash = kex.call(kex.api.custom.ipfs_upload(file, data, kex.id))
        kex.peers[kex.active_peer].disconnect()
        kex.id += 1
        if _file_hash != '':
            _file_hash = json.loads(_file_hash)['result']
        else:
            _file_hash = {'error': 'file_hash error'}

        return _file_hash

    @staticmethod
    def ipfs_payment(file_cid: str, payment_tx: str, kex: KEXclient) -> tuple:
        _ = kex.peers[kex.active_peer].connect()
        _payment_status = kex.call(kex.api.custom.ipfs_payment(file_cid, payment_tx, kex.id))
        kex.peers[kex.active_peer].disconnect()
        kex.id += 1
        if _payment_status != '':
            _payment_status = json.loads(_payment_status)['result']
            if 'error' in _payment_status:
                if _payment_status['error'] != None:
                    # {error:{code, message}}
                    _msg = _payment_status['error']
                    _msg_t = 1
                else:
                    _msg = 'Payment Sent!'
                    _msg_t = 2
            else:
                _msg = 'Payment Sent!'
                _msg_t = 2
        else:
            _msg = 'Payment Error'
            _msg_t = 1
            

        return (_msg_t, _msg) #_payment_status
