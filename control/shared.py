import base64  # TODO Check and add if missing to ConvUtils
import datetime
import json
import math
import time

from typing import List

from core.kex import KEXclient
from core.ksc import Scripts
from core.kcl.models.cache import MCache
from core.kcl.models.wallet import MWallet
from core.kcl.models.wallet_kind import EWalletKind
from core.kcl.models.addresses import MAddresses
from core.kcl.models.address import MAddress
from core.kcl.models.transaction import MTransaction
from core.kcl.models.script_pubkey import MScriptPubKey

from core.kcl.bip_utils.utils import ConvUtils
from core.kcl.bip_utils.base58 import Base58Decoder


class MShared():
    @staticmethod
    def get_timestamp(timestamp: float = None):
        if timestamp is None:
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
    def _load_message_file(file_path: str):
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
            if _batch_counter == 5:
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
    def __get_batch(batch: str, KEX: KEXclient):
        _results = KEX.call_batch(batch)
        _results = json.loads(_results)
        _results = MShared.__test_batch_for_error(batch, _results, KEX)
        return _results

    @staticmethod
    def __test_batch_for_error(batch, results, KEX: KEXclient):
        if not isinstance(results, list):
            print('type error', results)
            time.sleep(5)
            results = MShared.__get_batch(batch, KEX)
        else:
            if len(results) > 0:
                # HACK 1 and done test for excessive useage
                if 'error' in results[0]:
                    if 'excessive' in results[0]['error']['message']:
                        time.sleep(5)
                        results = MShared.__get_batch(batch, KEX)

        return results

    @staticmethod
    def get_block_count(KEX: KEXclient):
        _block_count = KEX.call(KEX.api.blockchain_block.count, [])
        if _block_count != '':
            _block_count = json.loads(_block_count)['result']
        return _block_count

    @staticmethod
    def get_fee_rate(KEX: KEXclient) -> int:
        _fee = KEX.call(KEX.api.blockchain.estimatefee, [2])
        if _fee != '':
            _fee = json.loads(_fee)['result']
            _fee = math.ceil((_fee*100000000)/1024)
        else:
            _fee = -1

        return _fee

    @staticmethod
    def broadcast(tx: str, KEX: KEXclient) -> tuple:
        _result = KEX.call(KEX.api.bc_tx.broadcast, [tx])
        if _result != '':
            _result = json.loads(_result)

            if 'error' in _result.keys():
                _msg = _result['error']
                _msg_t = 1
            else:
                _msg = 'TX Sent!'
                _msg_t = 2
        else:
            _msg = 'Call Error'
            _msg_t = 1

        return (_msg_t, _msg)

    @staticmethod
    def get_balances(wallet: MWallet, KEX: KEXclient):
        _th = []
        _tid = {}

        _th, _tid = MShared._get_balances_cmds(wallet.addresses,
                                               1, _th, _tid, KEX)
        _th, _tid = MShared._get_balances_cmds(wallet.change_addresses,
                                               0, _th, _tid, KEX)
        _batches = MShared.batch_cmds(_th)
        MShared._get_balances(wallet, _batches, _tid, KEX)

    @staticmethod
    def _get_balances_cmds(addresses: MAddresses, chain: int, _th: list,
                           _tid: dict, KEX: KEXclient):
        for _a in addresses.addresses:
            _script_hash = (Scripts.P2SHAddressScriptHash
                            .compileToScriptHash([_a.address], True))
            _th.append(KEX.api.blockchain_scripthash.get_balance
                       .build_command([_script_hash], KEX.id))
            _tid[str(KEX.id)] = {}
            _tid[str(KEX.id)]['address'] = _a.address
            _tid[str(KEX.id)]['chain'] = chain
            KEX.id = KEX.id + 1
        return _th, _tid

    @staticmethod
    def _get_balances(wallet: MWallet, batches: list, _tid: dict,
                      KEX: KEXclient):
        for batch in batches:
            _h = []
            if batch != b'[]\n':
                _h = MShared.__get_batch(batch, KEX)

            if not isinstance(_h, list):
                print('type _get_balances', _h)
            else:
                for i in _h:
                    _res = i['result']['confirmed'] / 100000000
                    _ures = i['result']['unconfirmed'] / 100000000
                    if _tid[str(i['id'])]['chain'] == 0:
                        _a = _tid[str(i['id'])]['address']
                        _aidx = (wallet.change_addresses
                                 .get_address_index_by_name(_a))
                        (wallet.change_addresses.addresses[_aidx]
                         .set_balance(_res))
                        (wallet.change_addresses.addresses[_aidx]
                         .set_unconfirmed_balance(_ures))

                    elif _tid[str(i['id'])]['chain'] == 1:
                        _a = _tid[str(i['id'])]['address']
                        _aidx = wallet.addresses.get_address_index_by_name(_a)
                        (wallet.addresses.addresses[_aidx]
                         .set_balance(_res))
                        (wallet.addresses.addresses[_aidx]
                         .set_unconfirmed_balance(_ures))

    @staticmethod
    def _get_balance(address: str, KEX: KEXclient) -> dict:
        _script_hash = (Scripts.P2SHAddressScriptHash
                        .compileToScriptHash([address], True))
        _bal = KEX.call(KEX.api.blockchain_scripthash.get_balance,
                        [_script_hash])
        if _bal != '':
            _bal = json.loads(_bal)['result']
        return _bal

    @staticmethod
    def list_unspents(wallet: MWallet, KEX: KEXclient):
        _th = []
        _tid = {}
        _th, _tid = MShared._list_unspents_cmds(wallet.addresses,
                                                1, _th, _tid, KEX)
        _th, _tid = MShared._list_unspents_cmds(wallet.change_addresses,
                                                0, _th, _tid, KEX)
        _batches = MShared.batch_cmds(_th)
        MShared._list_unspents(wallet, _batches, _tid, KEX)

    @staticmethod
    def _list_unspents_cmds(addresses: MAddresses, chain: int, _th: list,
                            _tid: dict, KEX: KEXclient):
        for _a in addresses.addresses:
            _script_hash = (Scripts.P2SHAddressScriptHash
                            .compileToScriptHash([_a.address], True))
            _th.append(KEX.api.blockchain_scripthash.listunspent
                       .build_command([_script_hash], KEX.id))
            _tid[str(KEX.id)] = {}
            _tid[str(KEX.id)]['address'] = _a.address
            _tid[str(KEX.id)]['chain'] = chain
            KEX.id = KEX.id + 1
        return _th, _tid

    @staticmethod
    def _list_unspents(wallet: MWallet, batches: list, _tid: dict,
                       KEX: KEXclient):
        for batch in batches:
            _h = []
            if batch != b'[]\n':
                _h = MShared.__get_batch(batch, KEX)

            if not isinstance(_h, list):
                print('type _list_unspents', _h)
            else:
                for i in _h:
                    if str(i['id']) in _tid:
                        if _tid[str(i['id'])]['chain'] == 0:
                            _a = _tid[str(i['id'])]['address']
                            _aidx = (wallet.change_addresses
                                     .get_address_index_by_name(_a))
                            if len(i['result']) > 0:
                                (wallet.change_addresses.addresses[_aidx]
                                 .set_unspent_tx(i['result']))
                            else:
                                (wallet.change_addresses.addresses[_aidx]
                                 .set_unspent_tx([]))

                        elif _tid[str(i['id'])]['chain'] == 1:
                            _a = _tid[str(i['id'])]['address']
                            _aidx = (wallet.addresses
                                     .get_address_index_by_name(_a))
                            if len(i['result']) > 0:
                                (wallet.addresses.addresses[_aidx]
                                 .set_unspent_tx(i['result']))
                            else:
                                (wallet.addresses.addresses[_aidx]
                                 .set_unspent_tx([]))

    @staticmethod
    def _list_unspent(address: str, KEX: KEXclient) -> dict:
        _script_hash = (Scripts.P2SHAddressScriptHash
                        .compileToScriptHash([address], True))
        _bal = KEX.call(KEX.api.blockchain_scripthash.listunspent,
                        [_script_hash])
        if _bal != '':
            _bal = json.loads(_bal)['result']
        return _bal

    @staticmethod
    def get_histories(wallet: MWallet, KEX: KEXclient):
        _th = []
        _tid = {}
        _th, _tid = MShared._get_histories_cmds(wallet, 1, _th, _tid, KEX)
        _th, _tid = MShared._get_histories_cmds(wallet, 0, _th, _tid, KEX)
        _batches = MShared.batch_cmds(_th)
        MShared._get_histories(wallet, _batches, _tid, KEX)

    @staticmethod
    def _get_histories_cmds(wallet: MWallet, chain: int, _th: list,
                            _tid: dict, KEX: KEXclient):
        if chain == 0:
            _addresses = wallet.change_addresses
        elif chain == 1:
            _addresses = wallet.addresses

        for _a in _addresses.addresses:
            _script_hash = (Scripts.P2SHAddressScriptHash
                            .compileToScriptHash([_a.address], True))
            _th.append(KEX.api.blockchain_scripthash.get_history
                       .build_command([_script_hash], KEX.id))
            _tid[str(KEX.id)] = {}
            _tid[str(KEX.id)]['address'] = _a.address
            _tid[str(KEX.id)]['chain'] = chain
            KEX.id = KEX.id + 1

        # NOTE Padding to detect used addresses out of wallets current index's
        if wallet.kind != 3:
            for _pad in range(0, 10):
                if chain == 0:
                    _pad_value = len(wallet.change_addresses.addresses) + _pad
                    _a = wallet.get_change_address_by_index(_pad_value, False)
                elif chain == 1:
                    _pad_value = len(wallet.addresses.addresses) + _pad
                    _a = wallet.get_address_by_index(_pad_value, False)

                _script_hash = (Scripts.P2SHAddressScriptHash
                                .compileToScriptHash([_a], True))
                _th.append(KEX.api.blockchain_scripthash.get_history
                           .build_command([_script_hash], KEX.id))
                _tid[str(KEX.id)] = {}
                _tid[str(KEX.id)]['address'] = _a
                _tid[str(KEX.id)]['chain'] = chain
                _tid[str(KEX.id)]['pad'] = _pad_value
                KEX.id = KEX.id + 1

        return _th, _tid

    @staticmethod
    def _get_histories(wallet: MWallet, batches: list, _tid: dict,
                       KEX: KEXclient):
        for batch in batches:
            _h = []
            if batch != b'[]\n':
                _h = MShared.__get_batch(batch, KEX)

            if not isinstance(_h, list):
                print('type _get_histories', _h)
            else:
                for i in _h:
                    if str(i['id']) in _tid:
                        if _tid[str(i['id'])]['chain'] == 0:
                            _a = _tid[str(i['id'])]['address']
                            _ax = (wallet.change_addresses
                                   .get_address_index_by_name(_a))
                            if _ax == -1:
                                if len(i['result']) > 0:
                                    _p = _tid[str(i['id'])]['pad']
                                    while wallet.change_addresses.count < _p:
                                        wallet.get_unused_change_address()

                                    if _p == wallet.change_addresses.count:
                                        (wallet
                                         .get_change_address_by_index(_p,
                                                                      True))
                                        _ax = (wallet.change_addresses
                                               .get_address_index_by_name(_a))
                                        (wallet.change_addresses.addresses[_ax]
                                         .set_history(i['result']))
                            else:
                                (wallet.change_addresses.addresses[_ax]
                                 .set_history(i['result']))
                        elif _tid[str(i['id'])]['chain'] == 1:
                            _a = _tid[str(i['id'])]['address']
                            _ax = (wallet.addresses
                                   .get_address_index_by_name(_a))
                            if _ax == -1:
                                _pd = _tid[str(i['id'])]['pad']
                                if len(i['result']) > 0:
                                    while wallet.addresses.count < _pd:
                                        wallet.get_unused_address()

                                    if _pd == wallet.addresses.count:
                                        wallet.get_address_by_index(_pd, True)
                                        _ax = (wallet.addresses
                                               .get_address_index_by_name(_a))
                                        (wallet.addresses.addresses[_ax]
                                         .set_history(i['result']))
                            else:
                                (wallet.addresses.addresses[_ax]
                                 .set_history(i['result']))

    @staticmethod
    def _get_history(address: str, KEX: KEXclient) -> dict:
        _script_hash = (Scripts.P2SHAddressScriptHash
                        .compileToScriptHash([address], True))
        _hist = KEX.call(KEX.api.blockchain_scripthash.get_history,
                         [_script_hash])
        if _hist != '':
            _hist = json.loads(_hist)['result']
        else:
            _hist = []

        return _hist

    @staticmethod
    def get_transactions(wallet: MWallet, KEX: KEXclient, cache: MCache):
        _block_count = MShared.get_block_count(KEX)
        # print('_block_count', _block_count)
        wallet.set_balance(0.0)
        _tx_h_batch = []
        _tx_in_b = []
        _tx_h_batch = MShared.__get_tx_cmds(_tx_h_batch,
                                            wallet.addresses.addresses,
                                            KEX, cache)
        _tx_h_batch = MShared.__get_tx_cmds(_tx_h_batch,
                                            wallet.change_addresses.addresses,
                                            KEX, cache)
        if len(_tx_h_batch) > 0:
            _ = MShared.__get_tx_by_batch(_tx_h_batch, KEX, cache)

        _tx_in_b = MShared.__get_tx_vin_cmds(_tx_in_b,
                                             wallet.addresses.addresses,
                                             KEX, cache)
        _tx_in_b = MShared.__get_tx_vin_cmds(_tx_in_b,
                                             wallet.change_addresses.addresses,
                                             KEX, cache)
        if len(_tx_in_b) > 0:
            _ = MShared.__get_tx_by_batch(_tx_in_b, KEX, cache)

        MShared._get_tx(wallet, wallet.addresses.addresses, KEX, cache)
        MShared._get_tx(wallet, wallet.change_addresses.addresses, KEX, cache)

    @staticmethod
    def __get_tx_cmds(_tx_h_batch: list, addresses: List[MAddress],
                      KEX: KEXclient, cache: MCache):
        for _a in addresses:
            _a.set_received(0.0)
            _a.set_sent(0.0)
            for _t in _a.history:
                _trx = cache.tx.get_tx_by_txid(_t['tx_hash'])
                if _trx is None:
                    _tx_h_batch.append(KEX.api.bc_tx.get
                                       .build_command([_t['tx_hash'], True],
                                                      KEX.id))
                    KEX.id = KEX.id + 1
                else:
                    if _trx.blockhash is None:
                        _tx_h_batch.append(KEX.api.bc_tx.get
                                           .build_command([_t['tx_hash'],
                                                           True], KEX.id))
                        KEX.id = KEX.id + 1
                    elif _trx.confirmations < 6:
                        _tx_h_batch.append(KEX.api.bc_tx.get
                                           .build_command([_t['tx_hash'],
                                                           True], KEX.id))
                        KEX.id = KEX.id + 1
        return _tx_h_batch

    @staticmethod
    def __get_tx_vin_cmds(_tx_i_b: list, addresses: List[MAddress],
                          KEX: KEXclient, cache: MCache):
        for _a in addresses:
            for _t in _a.history:
                _trx = cache.tx.get_tx_by_txid(_t['tx_hash'])
                if _trx is not None:
                    for _in in _trx.vin:
                        _in_tx = cache.tx.get_tx_by_txid(_in.txid)
                        if _in_tx is None:
                            _tx_i_b.append(KEX.api.bc_tx.get
                                           .build_command([_in.txid, True],
                                                          KEX.id))
                            KEX.id = KEX.id + 1
                        else:
                            if _in_tx.blockhash is None:
                                _tx_i_b.append(KEX.api.bc_tx.get
                                               .build_command([_in.txid, True],
                                                              KEX.id))
                                KEX.id = KEX.id + 1
                            elif _in_tx.confirmations < 6:
                                _tx_i_b.append(KEX.api.bc_tx.get
                                               .build_command([_in.txid, True],
                                                              KEX.id))
                                KEX.id = KEX.id + 1
        return _tx_i_b

    @staticmethod
    def _get_tx(wallet: MWallet, addresses: List[MAddress], KEX: KEXclient,
                cache: MCache):
        for _a in addresses:
            for _t in _a.history:
                _trx = cache.tx.get_tx_by_txid(_t['tx_hash'])
                if _trx is not None:
                    for _in in _trx.vin:
                        _vo = _in.vout
                        _in_tx = cache.tx.get_tx_by_txid(_in.txid)
                        for _out in _in_tx.vout:
                            if (_a.address in _out.scriptPubKey.addresses
                                    and _out.n == _vo):
                                _a.set_sent(_a.sent + _out.value)
                                wallet.set_balance(wallet.balance - _out.value)

                    for _out in _trx.vout:
                        if _a.address in _out.scriptPubKey.addresses:
                            _a.set_received(_a.received + _out.value)
                            wallet.set_balance(wallet.balance + _out.value)
                        MShared._test_for_namespace(wallet, _trx, _a, _t,
                                                    _out.scriptPubKey, KEX,
                                                    cache)

    @staticmethod
    def _test_for_namespace(wallet: MWallet, _trx: MTransaction, _a: MAddress,
                            _t: dict, _out: MScriptPubKey, KEX: KEXclient,
                            cache: MCache, test_root=True):
        _o = _out.asm.split(' ')
        if _o[0].startswith('OP_KEVA_'):
            _ns = cache.ns._get_namespace_by_id(_trx.txid, _o[1])
            if len(_ns) == 0:
                _merkle = KEX.call(KEX.api.bc_tx.get_merkle,
                                   [_trx.txid, _t['height']])
                if _merkle != '':
                    _merkle = json.loads(_merkle)
                    if 'result' in _merkle:
                        _merkle = _merkle['result']
                        # TODO Get dates and key types;
                        if _o[0] == 'OP_KEVA_NAMESPACE':
                            _ = (cache.ns
                                 ._fromRawValues(_merkle['block_height'],
                                                 _merkle['pos'],
                                                 _trx.txid, _o[1], _o[0],
                                                 '5f4b4556415f4e535f', _o[2],
                                                 _out.addresses[0]))
                        else:
                            if _o[0] == 'OP_KEVA_DELETE':
                                _ = cache.ns.delete_key(_o[1], _o[2], _merkle['block_height'])
                            else:
                                _key = cache.ns.get_namespace_by_key(_o[1], _o[2])
                                if len(_key) > 0 and _o[2][:4] != '0001':
                                    _ = (cache.ns
                                        .update_key(_merkle['block_height'],
                                                    _merkle['pos'],
                                                    _trx.txid, _o[1],
                                                    _o[2], _o[3],
                                                    _out.addresses[0]))
                                else:
                                    _ = (cache.ns
                                         ._fromRawValues(_merkle['block_height'],
                                                         _merkle['pos'],
                                                         _trx.txid, _o[1], _o[0],
                                                         _o[2], _o[3],
                                                         _out.addresses[0]))

                                    if test_root is True:
                                        MShared._test_root(wallet, _out, KEX,
                                                           cache)

    @staticmethod
    def _test_root(wallet: MWallet, _out: MScriptPubKey, KEX: KEXclient,
                   cache: MCache):
        _o = _out.asm.split(' ')
        _rootNS = cache.ns.get_root_namespace_by_id(_o[1], True)
        if len(_rootNS) == 0:
            _rootNS = (Scripts.KevaRootNamespaceScriptHash
                       .compileToScriptHash([_o[1], b''], True))
            _root_hist = KEX.call(KEX.api.blockchain_scripthash.get_history,
                                  [_rootNS])

            if _root_hist != '':
                _root_hist = json.loads(_root_hist)['result']
                _tracker = []

                if wallet.kind == EWalletKind.WATCH:
                    MShared.scan_history(_o[1], _tracker, wallet,
                                         _out.addresses[0], _root_hist, KEX,
                                         cache, False)
                else:
                    MShared.scan_history(_o[1], _tracker, wallet,
                                         _out.addresses[0], _root_hist, KEX,
                                         cache, False)

    @staticmethod
    def __get_tx_by_batch(_th: list, KEX: KEXclient, cache: MCache):
        _batches = MShared.batch_cmds(_th)

        for batch in _batches:
            _h = []
            if batch != b'[]\n':
                _h = MShared.__get_batch(batch, KEX)

            if not isinstance(_h, list):
                print('type __get_tx_by_batch', _h)
            else:
                for g in _h:
                    _i_tx = None
                    if 'result' in g:
                        _i_tx = cache.tx.get_tx_by_txid(g['result']['txid'])

                    if _i_tx is None:
                        if 'result' in g:
                            _i_tx = cache.tx.add_fromJson(g['result'])
                    else:
                        if _i_tx.blockhash is None:
                            if 'blockhash' in g['result']:
                                _gcf = g['result']['confirmations']
                                _ = cache.tx.update(g['result'])
                                _i_tx.set_blockhash(g['result']['blockhash'])
                                _i_tx.set_time(g['result']['time'])
                                _i_tx.set_blocktime(g['result']['blocktime'])
                                _i_tx.set_confirmations(_gcf)
                        elif _i_tx.confirmations < 6:
                            _gcf = g['result']['confirmations']
                            _ = cache.tx.update(g['result'])
                            _i_tx.set_confirmations(_gcf)

        return True

    @staticmethod
    def __get_tx(tx_hash: str, KEX: KEXclient, verbose=False):
        _tx = None
        ret = b''
        ret = KEX.call(KEX.api.bc_tx.get, [tx_hash, verbose])
        if ret != '':
            _tx = json.loads(ret)['result']

        return _tx

    @staticmethod
    def get_K(shortcode: int, wallet_name: str, cache: MCache,
              KEX: KEXclient) -> dict:
        # TODO Clean this up
        _bs = str(shortcode)
        _b = int(_bs[1:int(_bs[0])+1])
        if int(_bs[0])+1 < len(_bs):
            _p = int(_bs[int(_bs[0])+1:])
        else:
            return

        _hist = KEX.call(KEX.api.bc_tx.id_from_pos,
                         [_b, _p, False])
        _tracker = []

        if _hist != '' and b'error' not in _hist:
            _hist = json.loads(_hist)['result']

            _trx = cache.tx.get_tx_by_txid(_hist)
            if _trx is None:
                _tx = MShared.__get_tx(_hist, KEX, True)
                if _tx is not None:
                    _trx = cache.tx.add_fromJson(_tx)
            if _trx is not None:
                for _o in _trx.vout:
                    _ok = _o.scriptPubKey.asm.split(' ')
                    _a_hist = []
                    if _ok[0].startswith('OP_KEVA'):
                        _a = _o.scriptPubKey.addresses[0]
                        _a_hist = MShared._get_history(_a, KEX)
                        _tracker.append(_a)
                        MShared.scan_history(_ok[1], _tracker, wallet_name,
                                             _a, _a_hist, KEX, cache, False)

    @staticmethod
    def scan_history(_ns, _tracker: list, wallet_name, _a, _a_hist,
                     KEX: KEXclient, cache: MCache, deep: bool = True):
        for _h in _a_hist:
            if not isinstance(_h, dict):  # TODO refine upstream to remove check
                _btrx = None
            else:
                _btrx = cache.tx.get_tx_by_txid(_h['tx_hash'])
            if _btrx is None:
                _tx = MShared.__get_tx(_h['tx_hash'], KEX, True)
                if _tx is not None:
                    _btrx = cache.tx.add_fromJson(_tx)
            if _btrx is not None:
                for _bo in _btrx.vout:
                    MShared._test_for_namespace(wallet_name, _btrx,
                                                _bo.scriptPubKey.addresses[0],
                                                _h, _bo.scriptPubKey, KEX,
                                                cache,
                                                deep)

                    _ok = _bo.scriptPubKey.asm.split(' ')
                    if _ok[1] == _ns:
                        if _bo.scriptPubKey.addresses[0] not in _tracker:
                            _boa = _bo.scriptPubKey.addresses[0]
                            _b_hist = MShared._get_history(_boa, KEX)
                            _tracker.append(_bo.scriptPubKey.addresses[0])
                            MShared.scan_history(_ns, _tracker, wallet_name,
                                                 _bo.scriptPubKey.addresses[0],
                                                 _b_hist, KEX, cache, deep)

    @staticmethod
    def _get_namespace_keys(_ns, KEX: KEXclient,):
        try:
            _ns = ConvUtils.BytesToHexString(Base58Decoder.CheckDecode(_ns))
        except Exception:
            pass
        k_script_hash = (Scripts.KevaNamespaceScriptHash
                         .compileToScriptHash([_ns, b''], True))
        k_hist = KEX.call(KEX.api.keva.get_keyvalues, [k_script_hash, -1])
        _keys = []
        if k_hist != '':
            k_hist = json.loads(k_hist)
            k_hist = k_hist['result']

            for _i in range(0, len(k_hist['keyvalues'])):
                try:
                    _k = k_hist['keyvalues'][_i]['key']
                    _k = base64.b64decode(_k).decode()
                except Exception:
                    _k = base64.b64decode(k_hist['keyvalues'][_i]['key'])
                    _k = ConvUtils.BytesToHexString(_k)

                if k_hist['keyvalues'][_i]['type'] == 'REG':
                    _v = _k
                    _k = '_KEVA_NS_'
                else:
                    try:
                        _v = k_hist['keyvalues'][_i]['value']
                        _v = base64.b64decode(_v).decode()
                    except Exception:
                        _v = base64.b64decode(k_hist['keyvalues'][_i]['value'])
                        _v = ConvUtils.BytesToHexString(_v)
                _keys.append([_k, _v, k_hist['keyvalues'][_i]['time']])
        return _keys
