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
    def __get_batch(batch: list, kex: KEXclient):
        _results = kex.call_batch(batch)
        _results = json.loads(_results)
        _results = MShared.__test_batch_for_error(batch, _results, kex)
        return _results

    @staticmethod
    def __test_batch_for_error(batch, results, kex: KEXclient):
        if not isinstance(results, list):
            print('type error', results)
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

    # @staticmethod
    # def get_balances(wallet: MWallet, kex: KEXclient):
    #     _th: list = []
    #     _tid: dict = {}

    #     _th, _tid = MShared._get_balances_cmds(wallet.addresses,
    #                                            1, _th, _tid, kex)
    #     _th, _tid = MShared._get_balances_cmds(wallet.change_addresses,
    #                                            0, _th, _tid, kex)
    #     _batches = MShared.batch_cmds(_th)
    #     MShared._get_balances(wallet, _batches, _tid, kex)

    # @staticmethod
    # def _get_balances_cmds(addresses: MAddresses, chain: int, _th: list,
    #                        _tid: dict, kex: KEXclient):
    #     for _a in addresses.addresses:
    #         _script_hash = Scripts.AddressScriptHash(_a.address)
    #         _script_hash = Scripts.compileToScriptHash(_script_hash, True)
    #         _th.append(kex.api.blockchain_scripthash
    #                    .get_balance(_script_hash, kex.id))
    #         _tid[str(kex.id)] = {}
    #         _tid[str(kex.id)]['address'] = _a.address
    #         _tid[str(kex.id)]['chain'] = chain
    #         kex.id = kex.id + 1
    #     return _th, _tid

    # @staticmethod
    # def _get_balances(wallet: MWallet, batches: list, _tid: dict,
    #                   kex: KEXclient):
    #     for batch in batches:
    #         _h = []
    #         if batch != b'[]\n':
    #             _h = MShared.__get_batch(batch, kex)

    #         if not isinstance(_h, list):
    #             print('type _get_balances', _h)
    #         else:
    #             for i in _h:
    #                 _res = i['result']['confirmed'] / 100000000
    #                 _ures = i['result']['unconfirmed'] / 100000000
    #                 if _tid[str(i['id'])]['chain'] == 0:
    #                     _a = _tid[str(i['id'])]['address']
    #                     _aidx = (wallet.change_addresses
    #                              .get_address_index_by_name(_a))
    #                     (wallet.change_addresses.addresses[_aidx]
    #                      .set_balance(_res))
    #                     (wallet.change_addresses.addresses[_aidx]
    #                      .set_unconfirmed_balance(_ures))

    #                 elif _tid[str(i['id'])]['chain'] == 1:
    #                     _a = _tid[str(i['id'])]['address']
    #                     _aidx = wallet.addresses.get_address_index_by_name(_a)
    #                     (wallet.addresses.addresses[_aidx]
    #                      .set_balance(_res))
    #                     (wallet.addresses.addresses[_aidx]
    #                      .set_unconfirmed_balance(_ures))

    # @staticmethod
    # def _get_balance(address: str, kex: KEXclient) -> dict:
    #     _script_hash = Scripts.AddressScriptHash(address)
    #     _script_hash = Scripts.compileToScriptHash(_script_hash, True)
    #     _bal = kex.call(kex.api.blockchain_scripthash.get_balance
    #                     (_script_hash, kex.id))
    #     kex.id += 1
    #     if _bal != '':
    #         _bal = json.loads(_bal)['result']
    #     return _bal

    # @staticmethod
    # def list_unspents(wallet: MWallet, kex: KEXclient):
    #     _th: list = []
    #     _tid: dict = {}
    #     _th, _tid = MShared._list_unspents_cmds(wallet.addresses,
    #                                             1, _th, _tid, kex)
    #     _th, _tid = MShared._list_unspents_cmds(wallet.change_addresses,
    #                                             0, _th, _tid, kex)
    #     _batches = MShared.batch_cmds(_th)
    #     MShared._list_unspents(wallet, _batches, _tid, kex)

    # @staticmethod
    # def _list_unspents_cmds(addresses: MAddresses, chain: int, _th: list,
    #                         _tid: dict, kex: KEXclient):
    #     for _a in addresses.addresses:
    #         _script_hash = Scripts.AddressScriptHash(_a.address)
    #         _script_hash = Scripts.compileToScriptHash(_script_hash, True)
    #         _th.append(kex.api.blockchain_scripthash.listunspent
    #                    (_script_hash, kex.id))
    #         _tid[str(kex.id)] = {}
    #         _tid[str(kex.id)]['address'] = _a.address
    #         _tid[str(kex.id)]['chain'] = chain
    #         kex.id = kex.id + 1
    #     return _th, _tid

    # @staticmethod
    # def _list_unspents(wallet: MWallet, batches: list, _tid: dict,
    #                    kex: KEXclient):
    #     for batch in batches:
    #         _h = []
    #         if batch != b'[]\n':
    #             _h = MShared.__get_batch(batch, kex)

    #         if not isinstance(_h, list):
    #             print('type _list_unspents', _h)
    #             continue

    #         for i in _h:
    #             if str(i['id']) not in _tid:
    #                 continue

    #             if _tid[str(i['id'])]['chain'] == 0:
    #                 _a = _tid[str(i['id'])]['address']
    #                 _aidx = (wallet.change_addresses
    #                          .get_address_index_by_name(_a))
    #                 if len(i['result']) > 0:
    #                     (wallet.change_addresses.addresses[_aidx]
    #                      .set_unspent_tx(i['result']))
    #                 else:
    #                     (wallet.change_addresses.addresses[_aidx]
    #                      .set_unspent_tx([]))

    #             elif _tid[str(i['id'])]['chain'] == 1:
    #                 _a = _tid[str(i['id'])]['address']
    #                 _aidx = (wallet.addresses
    #                          .get_address_index_by_name(_a))
    #                 if len(i['result']) > 0:
    #                     (wallet.addresses.addresses[_aidx]
    #                      .set_unspent_tx(i['result']))
    #                 else:
    #                     (wallet.addresses.addresses[_aidx]
    #                      .set_unspent_tx([]))

    # @staticmethod
    # def _list_unspent(address: str, kex: KEXclient) -> dict:
    #     _script_hash = Scripts.AddressScriptHash(address)
    #     _script_hash = Scripts.compileToScriptHash(_script_hash, True)
    #     _bal = kex.call(kex.api.blockchain_scripthash.listunspent
    #                     (_script_hash, kex.id))
    #     kex.id += 1
    #     if _bal != '':
    #         _bal = json.loads(_bal)['result']
    #     return _bal

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

        for _a in _addresses.addresses:
            # _script_hash = Scripts.AddressScriptHash(_a.address)
            # _script_hash = Scripts.compileToScriptHash(_script_hash, True)
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

        # i {'jsonrpc': '2.0', 'result': [{'address': 'VCr5vsD8ga5ua1bj7kWTtzRdVwJPfDFJgL', 'received': 1506.5406293, 'sent': 1504.0406293, 'balance': 2.5}, {'total_results': 39, 'page_results': [{'block
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
        else:
            print('i', i)
            _addresses.addresses[_ax].set_history(i['result'][1]['page_results'])
            _addresses.addresses[_ax].set_namespaces(i['result'][2])
            _addresses.addresses[_ax].set_sent(i['result'][0]['sent'])
            _addresses.addresses[_ax].set_received(i['result'][0]['received'])
            _addresses.addresses[_ax].set_balance(i['result'][0]['balance'])

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

    # @staticmethod
    # def get_histories(wallet: MWallet, kex: KEXclient):
    #     _th: list = []
    #     _tid: dict = {}
    #     _th, _tid = MShared._get_histories_cmds(wallet, 1, _th, _tid, kex)
    #     _th, _tid = MShared._get_histories_cmds(wallet, 0, _th, _tid, kex)
    #     _batches = MShared.batch_cmds(_th)
    #     MShared._get_histories(wallet, _batches, _tid, kex)

    # @staticmethod
    # def _get_histories_cmds(wallet: MWallet, chain: int, _th: list,
    #                         _tid: dict, kex: KEXclient):
    #     if chain == 0:
    #         _addresses = wallet.change_addresses
    #     elif chain == 1:
    #         _addresses = wallet.addresses

    #     for _a in _addresses.addresses:
    #         _script_hash = Scripts.AddressScriptHash(_a.address)
    #         _script_hash = Scripts.compileToScriptHash(_script_hash, True)
    #         _th.append(kex.api.blockchain_scripthash.get_history
    #                    (_script_hash, kex.id))
    #         _tid[str(kex.id)] = {}
    #         _tid[str(kex.id)]['address'] = _a.address
    #         _tid[str(kex.id)]['chain'] = chain
    #         kex.id = kex.id + 1

    #     # NOTE Padding to detect used addresses out of wallets current index's
    #     if len(_addresses.addresses) == 0:
    #         _scan_pad = 100
    #     else:
    #         _scan_pad = 10

    #     if wallet.kind != 3:
    #         for _pad in range(0, _scan_pad):
    #             if chain == 0:
    #                 _pad_value = len(wallet.change_addresses.addresses) + _pad
    #                 _addr = wallet.get_change_address_by_index(_pad_value,
    #                                                            False)
    #             elif chain == 1:
    #                 _pad_value = len(wallet.addresses.addresses) + _pad
    #                 _addr = wallet.get_address_by_index(_pad_value, False)

    #             _script_hash = Scripts.AddressScriptHash(_addr)
    #             _script_hash = Scripts.compileToScriptHash(_script_hash, True)
    #             _th.append(kex.api.blockchain_scripthash.get_history
    #                        (_script_hash, kex.id))
    #             _tid[str(kex.id)] = {}
    #             _tid[str(kex.id)]['address'] = _addr
    #             _tid[str(kex.id)]['chain'] = chain
    #             _tid[str(kex.id)]['pad'] = _pad_value
    #             kex.id = kex.id + 1

    #     return _th, _tid

    # @staticmethod
    # def _process_histories(wallet: MWallet, _tid: dict, i: dict):
    #     _chain = _tid[str(i['id'])]['chain']
    #     if _chain == 0:
    #         _addresses = wallet.change_addresses
    #     else:
    #         _addresses = wallet.addresses

    #     _a = _tid[str(i['id'])]['address']
    #     _ax = _addresses.get_address_index_by_name(_a)
    #     if _ax == -1:
    #         if len(i['result']) <= 0:
    #             return

    #         _p = _tid[str(i['id'])]['pad']
    #         while _addresses.count < _p:
    #             if _chain == 0:
    #                 wallet.get_unused_change_address()
    #             else:
    #                 wallet.get_unused_address()

    #         if _p == _addresses.count:
    #             if _chain == 0:
    #                 wallet.get_change_address_by_index(_p, True)
    #             else:
    #                 wallet.get_address_by_index(_p, True)

    #             _ax = _addresses.get_address_index_by_name(_a)
    #             _addresses.addresses[_ax].set_history(i['result'])
    #     else:
    #         _addresses.addresses[_ax].set_history(i['result'])

    # @staticmethod
    # def _get_histories(wallet: MWallet, batches: list, _tid: dict,
    #                    kex: KEXclient):
    #     for batch in batches:
    #         _h = []
    #         if batch != b'[]\n':
    #             _h = MShared.__get_batch(batch, kex)

    #         if not isinstance(_h, list):
    #             continue

    #         for i in _h:
    #             if str(i['id']) not in _tid:
    #                 continue

    #             MShared._process_histories(wallet, _tid, i)

    # @staticmethod
    # def _get_history(address: str, kex: KEXclient) -> dict:
    #     _script_hash = Scripts.AddressScriptHash(address)
    #     _script_hash = Scripts.compileToScriptHash(_script_hash, True)
    #     _hist = kex.call(kex.api.blockchain_scripthash.get_history
    #                      (_script_hash, kex.id))
    #     kex.id += 1
    #     if _hist != '':
    #         _hist = json.loads(_hist)['result']
    #     else:
    #         _hist = []

    #     return _hist

    # @staticmethod
    # def get_transactions(wallet: MWallet, kex: KEXclient, cache: MCache, _provider):
    #     # _block_count = MShared.get_block_count(kex)
    #     # print('_block_count', _block_count)
    #     wallet.set_balance(0.0)
    #     _tx_h_batch: dict = {}
    #     _tx_in_b: dict = {}
    #     _tx_h_batch = MShared.__get_tx_cmds(_tx_h_batch,
    #                                         wallet.addresses.addresses,
    #                                         kex, cache)
    #     _tx_h_batch = MShared.__get_tx_cmds(_tx_h_batch,
    #                                         wallet.change_addresses.addresses,
    #                                         kex, cache)
    #     _tx_b = list(_tx_h_batch.values())
    #     _tx_b = MShared.btx(_tx_b, kex, cache)
    #     if len(_tx_b) > 0:
    #         _ = MShared.__get_tx_by_batch(_tx_b, kex, cache)

    #     _tx_in_b = MShared.__get_tx_vin_cmds(_tx_in_b,
    #                                          wallet.addresses.addresses,
    #                                          kex, cache)
    #     _tx_in_b = MShared.__get_tx_vin_cmds(_tx_in_b,
    #                                          wallet.change_addresses.addresses,
    #                                          kex, cache)
    #     _intx_b = list(_tx_in_b.values())
    #     _intx_b = MShared.bintx(_intx_b, kex, cache)

    #     if len(_intx_b) > 0:
    #         _ = MShared.__get_tx_by_batch(_intx_b, kex, cache)

    #     _ns_test = []
    #     _ns_test_id = []
    #     _ns_test, _ns_test_id = MShared._get_tx(wallet, wallet.addresses.addresses, kex, cache, _ns_test, _ns_test_id)
    #     _ns_test, _ns_test_id = MShared._get_tx(wallet, wallet.change_addresses.addresses, kex, cache, _ns_test, _ns_test_id)

    #     for _t in _ns_test:
    #         # TODO: move this check to churn through unspents only
    #         MShared._test_for_namespace(_t, kex, cache, _provider)

    # @staticmethod
    # def btx(_tx_h_batch: list, kex: KEXclient, cache: MCache):
    #     _batch = []
    #     for _t in _tx_h_batch:
    #         _trx = cache.tx.get_tx_by_txid(_t)
    #         if _trx is None:
    #             _batch.append(kex.api.bc_tx.get
    #                           (_t, True, kex.id))
    #             kex.id = kex.id + 1
    #         else:
    #             if _trx.blockhash == '':
    #                 _batch.append(kex.api.bc_tx.get
    #                               (_t, True, kex.id))
    #                 kex.id = kex.id + 1
    #             elif _trx.confirmations < 6:
    #                 _batch.append(kex.api.bc_tx.get
    #                               (_t, True, kex.id))
    #                 kex.id = kex.id + 1
    #     return _batch

    # @staticmethod
    # def bintx(_tx_h_batch: list, kex: KEXclient, cache: MCache):
    #     _batch = []
    #     for _t in _tx_h_batch:
    #         # print('_t', _t)
    #         _in_tx = cache.tx.get_tx_by_txid(_t)

    #         if _in_tx is None:
    #             _batch.append(kex.api.bc_tx.get
    #                             (_t, True, kex.id))
    #             kex.id = kex.id + 1
    #         else:
    #             if _in_tx.blockhash != '':
    #                 _batch.append(kex.api.bc_tx.get
    #                                (_t, True, kex.id))
    #                 kex.id = kex.id + 1
    #             elif _in_tx.confirmations < 6:
    #                 _batch.append(kex.api.bc_tx.get
    #                                (_t, True, kex.id))
    #                 kex.id = kex.id + 1
    #     return _batch

    # @staticmethod
    # def __get_tx_cmds(_tx_h_batch: dict, addresses: List[MAddress],
    #                   kex: KEXclient, cache: MCache):
    #     # _tx_batch = {}
    #     _tx_count = 0
    #     for _a in addresses:
    #         _a.set_received(0.0)
    #         _a.set_sent(0.0)
    #         _tx_count += len(_a.history)
    #         for _t in _a.history:
    #             _tx_h_batch[_t['tx_hash']] = _t['tx_hash'] #.encode('utf-8')

    #     return _tx_h_batch # _tx_h_batch

    # @staticmethod
    # def __get_tx_vin_cmds(_tx_i_b: dict, addresses: List[MAddress],
    #                       kex: KEXclient, cache: MCache):
    #     for _a in addresses:
    #         for _t in _a.history:
    #             _trx = cache.tx.get_tx_by_txid(_t['tx_hash'])
    #             if _trx is None:
    #                 continue

    #             for _in in _trx.vin:
    #                 if _in.coinbase != '':
    #                     continue

    #                 _in_tx = cache.tx.get_tx_by_txid(_in.txid)

    #                 if _in_tx is None:
    #                     _tx_i_b[_in.txid] = _in.txid
    #     return _tx_i_b

    # @staticmethod
    # def _get_tx(wallet: MWallet, addresses: List[MAddress], kex: KEXclient,
    #             cache: MCache, _ns_test, _ns_test_id):
    #     for _a in addresses:
    #         for _t in _a.history:
    #             _trx = cache.tx.get_tx_by_txid(_t['tx_hash'])
    #             if _trx is None:
    #                 continue

    #             MShared._process_tx_vin(wallet, _trx.vin, _a, kex, cache)
    #             MShared._process_tx_vout(wallet, _trx.vout, _a)

    #             for _out in _trx.vout:
    #                 if _out.scriptPubKey not in _ns_test:
    #                     _o = _out.scriptPubKey.asm.split(' ')
    #                     if _o[0].startswith('OP_KEVA_') is True:
    #                         if _o[1] not in _ns_test_id:
    #                             _ns_test_id.append(_o[1])
    #                             _ns_test.append(_out.scriptPubKey)

    #     return _ns_test, _ns_test_id

    # @staticmethod
    # def _process_tx_vin(wallet: MWallet, vin: List[MTransactionInput],
    #                     address: MAddress, kex: KEXclient, cache: MCache):

    #     for _in in vin:
    #         if _in.coinbase != '':
    #             continue

    #         _vo = _in.vout
    #         _in_tx = cache.tx.get_tx_by_txid(_in.txid)
    #         if _in_tx is None:
    #             _in_tx = MShared.get_tx(_in.txid, kex, True)
    #         if _in_tx is not None and isinstance(_in_tx, dict):
    #             _in_tx = cache.tx.add_from_json(_in_tx)

    #         if _in_tx is None:
    #             continue

    #         for _out in _in_tx.vout:
    #             if (address.address in _out.scriptPubKey.addresses
    #                     and _out.n == _vo):
    #                 address.set_sent(address.sent + _out.value)
    #                 wallet.set_balance(wallet.balance - _out.value)

    # @staticmethod
    # def _process_tx_vout(wallet: MWallet, vout: List[MTransactionOutput],
    #                      address: MAddress):

    #     for _out in vout:
    #         if address.address in _out.scriptPubKey.addresses:
    #             address.set_received(address.received + _out.value)
    #             wallet.set_balance(wallet.balance + _out.value)

    # @staticmethod
    # def get_merkle(txid: str, height: int, kex: KEXclient) -> str:
    #     _merkle = kex.call(kex.api.bc_tx.get_merkle(txid, height, kex.id))
    #     kex.id += 1
    #     try:
    #         _merkle = json.loads(_merkle)
    #     except Exception:
    #         _merkle = ''

    #     if 'result' not in _merkle:
    #         _merkle = ''
    #     else:
    #         _merkle = _merkle['result']

    #     return _merkle

    # @staticmethod
    # def process_ns_key_reactions(txid: str, kex: KEXclient, cache: MCache):
    #     _reactions = MShared.get_ns_key_reactions(txid, kex)

    #     _tx_h_batch = []
    #     for _reply in _reactions['replies']:
    #         _r_trx = cache.tx.get_tx_by_txid(_reply['tx_hash'])
    #         if _r_trx is None:
    #             _tx_h_batch.append(kex.api.bc_tx.get
    #                                (_reply['tx_hash'], True, kex.id))
    #             kex.id = kex.id + 1
    #     if len(_tx_h_batch) > 0:
    #         _ = MShared.__get_tx_by_batch(_tx_h_batch, kex, cache)

    #     for _reply in _reactions['replies']:
    #         _r_tx = cache.tx.get_tx_by_txid(_reply['tx_hash'])
    #         if _r_tx is None:
    #             _r_tx = MShared.get_tx(_reply['tx_hash'], kex, True)
    #         if _r_tx is not None and isinstance(_r_tx, dict):
    #             _r_tx = cache.tx.add_from_json(_r_tx)
    #         for _ro in _r_tx.vout:
    #             MShared._test_for_namespace(_ro.scriptPubKey, kex, cache)

    # @staticmethod
    # def _test_for_namespace(_out: MScriptPubKey, kex: KEXclient,
    #                         cache: MCache, _provider):
    #     _o = _out.asm.split(' ')
    #     if _o[0].startswith('OP_KEVA_') is False:
    #         return

    #     nsid = cache.ns.convert_to_namespaceid(_o[1])
    #     _ns = MShared.get_namespace(nsid, _provider)
    #     if 'result' not in _ns:
    #         if 'data' not in _ns:
    #             return

    #     _ns = _ns['result']
    #     _dat = _ns['data']

    #     for _kv in _dat:
    #         if _kv['op'] == 'KEVA_NAMESPACE':
    #             _ns_test = cache.ns.get_root_namespace_by_id(_kv['nsid'], True)
    #             if len(_ns_test) != 0:
    #                 continue

    #             _pos = _kv['key_shortcode'][7:]
    #             _ = (cache.ns
    #                 .from_raw(_kv['block'],
    #                         _pos,
    #                         _kv['txid'], _kv['nsid'], 'OP_' + _kv['op'],
    #                         '5f4b4556415f4e535f', _kv['value'],
    #                         _kv['addr']))
    #         else:
    #             if _kv['op'] == 'KEVA_DELETE':
    #                 _ = (cache.ns
    #                     .mark_key_deleted(_kv['block'], _kv['nsid'], _kv['key']))
    #             else:
    #                 _ns = cache.ns.convert_to_namespaceid(_kv['nsid'])
    #                 _key = cache.ns._decode(_kv['key'])
    #                 _k_test = cache.ns.get_namespace_by_key_value(_ns, _key)

    #                 if len(_k_test) != 0:
    #                     if _k_test[0][0] < _kv['block']:
    #                         _pos = _kv['key_shortcode'][7:]
    #                         _ = (cache.ns
    #                             .update_key(_kv['block'],
    #                                         _pos,
    #                                         _kv['txid'], _kv['nsid'], _kv['key'], _kv['value'],
    #                                         _kv['addr']))
    #                 else:
    #                     if _kv['key'][:4] == '0003':
    #                         if isinstance(_kv['dvalue'], int):
    #                             _kv['value'] = str(float(_kv['dvalue']))
    #                         else:
    #                             _kv['value'] = str(_kv['dvalue'])
    #                     _pos = _kv['key_shortcode'][7:]
    #                     _ = (cache.ns
    #                         .from_raw(_kv['block'],
    #                                 _pos,
    #                                 _kv['txid'], _kv['nsid'], 'OP_' + _kv['op'],
    #                                 _kv['key'], _kv['value'],
    #                                 _kv['addr']))

    # @staticmethod
    # def __test_for_namespace(_out: MScriptPubKey, kex: KEXclient,
    #                         cache: MCache):
    #     _o = _out.asm.split(' ')
    #     if _o[0].startswith('OP_KEVA_') is False:
    #         return

    #     _root_ns = cache.ns.get_root_namespace_by_id(_o[1], True)
    #     if len(_root_ns) == 0:
    #         _root_ns = Scripts.KevaRootNamespaceScriptHash(_o[1], b'')
    #         _root_ns = Scripts.compileToScriptHash(_root_ns, True)
    #         # _root_ns = (Scripts.KevaRootNamespaceScriptHash
    #         #             .compileToScriptHash([_o[1], b''], True))
    #         _root_hist = kex.call(kex.api.blockchain_scripthash.get_history
    #                               (_root_ns, kex.id))
    #         kex.id += 1
    #     else:
    #         _root_hist = ''

    #     _nk = cache.ns.convert_to_namespaceid(_o[1])
    #     _keys = MShared.get_namespace_keys(_nk, kex)

    #     if _root_hist != '':
    #         for rh in json.loads(_root_hist)['result']:
    #             _keys.append(rh)

    #     _tx_h_batch = []
    #     _th_h_track = {}
    #     for k in _keys:
    #         if k['tx_hash'] in _th_h_track.values():
    #             continue
    #         _r_trx = cache.tx.get_tx_by_txid(k['tx_hash'])
    #         if _r_trx is None:
    #             _th_h_track[str(kex.id)] = k['tx_hash']
    #             _tx_h_batch.append(kex.api.bc_tx.get
    #                                (k['tx_hash'], True, kex.id))
    #             kex.id = kex.id + 1
    #     if len(_tx_h_batch) > 0:
    #         _ = MShared.__get_tx_by_batch(_tx_h_batch, kex, cache)

    #     _m_batch = []
    #     _m_track = {}
    #     for k in _keys:
    #         if k['tx_hash'] in _m_track.values():
    #             continue

    #         _r_tx = cache.tx.get_tx_by_txid(k['tx_hash'])
    #         if _r_tx is None or _r_tx.blockhash == '':
    #             continue

    #         for _ro in _r_tx.vout:
    #             _tro = _ro.scriptPubKey.asm.split(' ')
    #             if _tro[0].startswith('OP_KEVA_') is True:
    #                 # _key = cache.ns.get_namespace_by_txid(_r_tx.txid, _tro[1])
    #                 # if len(_key) == 0:
    #                 _m_track[str(kex.id)] = k['tx_hash']
    #                 _m_batch.append(kex.api.bc_tx.get_merkle
    #                                 (_r_tx.txid, k['height'], kex.id))
    #                 kex.id += 1
    #     if len(_m_batch) > 0:
    #         _merkles = MShared.__get_merkle_by_batch(_m_batch, _m_track, kex)
    #     else:
    #         _merkles = {}

    #     _ref_batch = []
    #     for k in _keys:
    #         if k['tx_hash'] not in _merkles:
    #             continue
    #         _r_tx = cache.tx.get_tx_by_txid(k['tx_hash'])
    #         if _r_tx is None:
    #             continue

    #         for _ro in _r_tx.vout:
    #             _tro = _ro.scriptPubKey.asm.split(' ')
    #             if _tro[0].startswith('OP_KEVA_') is True:
    #                 # _key = cache.ns.get_namespace_by_txid(_r_tx.txid, _tro[1])
    #                 # if len(_key) != 0:
    #                 #     continue

    #                 MShared._p_namespace(_ro.scriptPubKey, _r_tx,
    #                                      _merkles[k['tx_hash']], _ref_batch,
    #                                      kex, cache)
    #     if len(_ref_batch) > 0:
    #         _ = MShared.__get_tx_by_batch(_ref_batch, kex, cache)

    # @staticmethod
    # def _p_namespace(out: MScriptPubKey, _trx: MTransaction, _merkle: dict,
    #                  _ref_batch: list, kex: KEXclient, cache: MCache):
    #     _o = out.asm.split(' ')
    #     if _o[0].startswith('OP_KEVA_') is False:
    #         return

    #     if _o[0] == 'OP_KEVA_NAMESPACE':
    #         _ns_test = cache.ns.get_root_namespace_by_id(_o[1], True)
    #         if len(_ns_test) != 0:
    #             return
    #         _ = (cache.ns
    #              .from_raw(_merkle['block_height'],
    #                        _merkle['pos'],
    #                        _trx.txid, _o[1], _o[0],
    #                        '5f4b4556415f4e535f', _o[2],
    #                        out.addresses[0]))
    #     else:
    #         if _o[0] == 'OP_KEVA_DELETE':
    #             _ = (cache.ns
    #                  .mark_key_deleted(_merkle['block_height'], _o[1], _o[2]))
    #         else:
    #             _ns = cache.ns.convert_to_namespaceid(_o[1])
    #             _key = cache.ns._decode(_o[2])
    #             _k_test = cache.ns.get_namespace_by_key_value(_ns, _key)
    #             # if (len(_k_test) != 0 and 
    #             #         (_o[2][:4] != '0001' and _o[2][:4] != '0002'
    #             #             and _o[2][:4] != '0003')):
    #             if len(_k_test) != 0:
    #                 if _k_test[0][0] < _merkle['block_height']:
    #                     _ = (cache.ns
    #                          .update_key(_merkle['block_height'],
    #                                      _merkle['pos'],
    #                                      _trx.txid, _o[1], _o[2], _o[3],
    #                                      out.addresses[0]))
    #             else:
    #                 if (_o[2][:4] == '0001' or _o[2][:4] == '0002'
    #                         or _o[2][:4] == '0003'):

    #                     _r_trx = cache.tx.get_tx_by_txid(_o[2][4:])
    #                     if _r_trx is None:
    #                         _ref_batch.append(kex.api.bc_tx.get
    #                                           (_o[2][4:], True, kex.id))
    #                         kex.id += 1
    #                 if _o[2][:4] == '0003':
    #                     # TODO Fix this upstream...type check for now
    #                     if isinstance(_trx.vout[1].value, int):
    #                         _o[3] = str(float(_trx.vout[1].value))
    #                     else:
    #                         _o[3] = str(_trx.vout[1].value)

    #                 _ = (cache.ns
    #                      .from_raw(_merkle['block_height'],
    #                                _merkle['pos'],
    #                                _trx.txid, _o[1], _o[0],
    #                                _o[2], _o[3],
    #                                out.addresses[0]))

    # @staticmethod
    # def _get_referenced_tx(key: str, kex: KEXclient, cache: MCache):
    #     if (key[:4] == '0001' or key[:4] == '0002'
    #             or key[:4] == '0003'):

    #         _r_tx = cache.tx.get_tx_by_txid(key[4:])
    #         if _r_tx is None:
    #             _r_tx = MShared.get_tx(key[4:], kex, True)
    #         if _r_tx is not None and isinstance(_r_tx, dict):
    #             _r_tx = cache.tx.add_from_json(_r_tx)

    # @staticmethod
    # def _test_root(_out: MScriptPubKey, kex: KEXclient, cache: MCache):
    #     _o = _out.asm.split(' ')
    #     _root_ns = cache.ns.get_root_namespace_by_id(_o[1], True)
    #     if len(_root_ns) == 0:
    #         _root_ns = Scripts.KevaRootNamespaceScriptHash(_o[1], b'')
    #         _root_ns = Scripts.compileToScriptHash(_root_ns, True)
    #         _root_hist = kex.call(kex.api.blockchain_scripthash.get_history
    #                               (_root_ns, kex.id))
    #         kex.id += 1

    #         if _root_hist != '':
    #             _root_hist = json.loads(_root_hist)['result']
    #             _tracker: list = []

    #             MShared.scan_history(_o[1], _tracker,
    #                                  _out.addresses[0], _root_hist, kex,
    #                                  cache, False)

    # @staticmethod
    # def __get_merkle_by_batch(_th: list, _track: dict, kex: KEXclient):
    #     _batches = MShared.batch_cmds(_th)
    #     _merkles = {}
    #     for batch in _batches:
    #         _h = []
    #         if batch != b'[]\n':
    #             _h = MShared.__get_batch(batch, kex)

    #         if not isinstance(_h, list):
    #             continue

    #         for h in _h:
    #             _merkles[_track[h['id']]] = {}
    #             _merkles[_track[h['id']]]['block_height'] = h['result']['block_height']
    #             _merkles[_track[h['id']]]['pos'] = h['result']['pos']

    #     return _merkles

    # @staticmethod
    # def __get_tx_by_batch(_th: list, kex: KEXclient, cache: MCache):
    #     _batches = MShared.batch_cmds(_th)

    #     for batch in _batches:
    #         _h = []
    #         if batch != b'[]\n':
    #             _h = MShared.__get_batch(batch, kex)

    #         if not isinstance(_h, list):
    #             print('type __get_tx_by_batch', _h)
    #             continue

    #         MShared._process_tx_batch(_h, cache)

    #     return True

    # @staticmethod
    # def _process_tx_batch(batch_results: list, cache: MCache):
    #     for g in batch_results:
    #         _i_tx = None
    #         if 'result' in g:
    #             _i_tx = cache.tx.get_tx_by_txid(g['result']['txid'])

    #         if _i_tx is None:
    #             if 'result' in g:
    #                 _i_tx = cache.tx.add_from_json(g['result'])
    #         else:
    #             if _i_tx.blockhash == '':
    #                 if 'blockhash' not in g['result']:
    #                     continue

    #                 _gcf = g['result']['confirmations']
    #                 _ = cache.tx.update(g['result'])
    #                 _i_tx.set_blockhash(g['result']['blockhash'])
    #                 _i_tx.set_time(g['result']['time'])
    #                 _i_tx.set_blocktime(g['result']['blocktime'])
    #                 _i_tx.set_confirmations(_gcf)
    #             elif _i_tx.confirmations < 6:
    #                 _gcf = g['result']['confirmations']
    #                 _ = cache.tx.update(g['result'])
    #                 _i_tx.set_confirmations(_gcf)

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

    # @staticmethod
    # def get_K(shortcode: int, cache: MCache, kex: KEXclient):
    #     # TODO Clean this up
    #     _bs = str(shortcode)
    #     _b = int(_bs[1:int(_bs[0])+1])
    #     if int(_bs[0])+1 < len(_bs):
    #         _p = int(_bs[int(_bs[0])+1:])
    #     else:
    #         return

    #     _hist = kex.call(kex.api.bc_tx.id_from_pos
    #                      (_b, _p, False, kex.id))
    #     kex.id += 1
    #     _tracker = []

    #     if _hist != '' and 'error' not in _hist:
    #         _hist = json.loads(_hist)['result']

    #         _trx = cache.tx.get_tx_by_txid(_hist)
    #         if _trx is None:
    #             _tx = MShared.get_tx(_hist, kex, True)
    #             if _tx is not None:
    #                 _trx = cache.tx.add_from_json(_tx)
    #         if _trx is not None:
    #             for _o in _trx.vout:
    #                 _ok = _o.scriptPubKey.asm.split(' ')
    #                 # _a_hist: list = []
    #                 if _ok[0].startswith('OP_KEVA'):
    #                     _a = _o.scriptPubKey.addresses[0]
    #                     _a_hist = MShared._get_history(_a, kex)
    #                     _tracker.append(_a)
    #                     MShared.scan_history(_ok[1], _tracker,
    #                                          _a, _a_hist, kex, cache, False)

    # @staticmethod
    # def scan_history(_ns, _tracker: list, _a, _a_hist,
    #                  kex: KEXclient, cache: MCache, deep: bool = True):
    #     _ns_test = []
    #     for _h in _a_hist:
    #         if not isinstance(_h, dict):  # TODO refine upstream to rm check
    #             _btrx = None
    #         else:
    #             _btrx = cache.tx.get_tx_by_txid(_h['tx_hash'])
    #         if _btrx is None:
    #             _tx = MShared.get_tx(_h['tx_hash'], kex, True)
    #             if _tx is not None:
    #                 _btrx = cache.tx.add_from_json(_tx)
    #         if _btrx is not None:
    #             for _bo in _btrx.vout:
    #                 _ok = _bo.scriptPubKey.asm.split(' ')
    #                 if _ok[1] == _ns:
    #                     if _bo.scriptPubKey.addresses[0] not in _tracker:
    #                         _boa = _bo.scriptPubKey.addresses[0]
    #                         _b_hist = MShared._get_history(_boa, kex)
    #                         _tracker.append(_boa)
    #                         MShared.scan_history(_ns, _tracker, _boa,
    #                                              _b_hist, kex, cache, deep)
    #                 if _bo.scriptPubKey not in _ns_test:
    #                     _ns_test.append(_bo.scriptPubKey)

    #     for _t in _ns_test:
    #         MShared._test_for_namespace(_t, kex, cache)

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

    # @staticmethod
    # def check_if_bid_valid(bid: keva_psbt, kex: KEXclient,
    #                        cache: MCache) -> bool:
    #     _valid_usxo = []
    #     for vin in bid.tx.vin:
    #         _tx = cache.tx.get_tx_by_txid(vin.txid)
    #         if _tx is None:
    #             _tx = MShared.get_tx(vin.txid, kex, True)
    #             _tx = cache.tx.add_from_json(_tx)

    #         _a = _tx.vout[vin.vout].scriptPubKey.addresses[0]
    #         _a_usxo = MShared._list_unspent(_a, kex)

    #         for _i in _a_usxo:
    #             if _i['tx_hash'] == vin.txid and _i['tx_pos'] == vin.vout:
    #                 _valid_usxo.append(1)
    #             else:
    #                 _valid_usxo.append(0)

    #     if sum(_valid_usxo) != len(bid.tx.vin):
    #         return False

    #     return True

    # @staticmethod
    # def check_tx_is_auction(tx: str, kex: KEXclient, cache: MCache) -> tuple:
    #     if len(tx) != 64:
    #         return (False, '', '')

    #     _tx = cache.tx.get_tx_by_txid(tx)

    #     if _tx is None:
    #         _tx = MShared.get_tx(tx, kex, True)

    #     if _tx is not None and isinstance(_tx, dict):
    #         _tx = cache.tx.add_from_json(_tx)
    #     elif _tx is None:
    #         return (False, '', '')

    #     _asm = _tx.vout[0].scriptPubKey.asm.split(' ')
    #     if _asm[0] != 'OP_KEVA_PUT':
    #         return (False, '', '')

    #     _key = cache.ns._decode(_asm[2])
    #     _value = cache.ns._decode(_asm[3])
    #     if cache.ns.get_key_type(_key, _value) != 'nft_auction':
    #         return (False, '', '')

    #     _ns = cache.ns.convert_to_namespaceid(_asm[1])

    #     return (True, _ns, json.loads(_value))

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

    # @staticmethod
    # def check_tx_is_ns_key(tx: str, kex: KEXclient, cache: MCache) -> tuple:
    #     _tx = cache.tx.get_tx_by_txid(tx)

    #     if _tx is None:
    #         _tx = MShared.get_tx(tx, kex, True)
    #         _tx = cache.tx.add_from_json(_tx)

    #     _ns_test = _tx.vout[0].scriptPubKey.asm.split(' ')

    #     if _ns_test[0] != 'OP_KEVA_PUT':
    #         return (False, '', '', '', '')

    #     _ns = cache.ns.convert_to_namespaceid(_ns_test[1])
    #     _key = cache.ns._decode(_ns_test[2])
    #     _value = cache.ns._decode(_ns_test[3])
    #     _address = cache.ns.last_address(_ns)

    #     if len(_address) == 0:
    #         return (False, '', '', '', '')

    #     return (True, _ns, _key, _value, _address[0][0])

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