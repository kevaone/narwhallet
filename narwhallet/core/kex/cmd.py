from typing import Tuple
from narwhallet.core.kex.cmd_base import _cmd
from narwhallet.core.kex.param import ElXparams

_CMDT = Tuple[str, list]


class _server(_cmd):
    version: _CMDT = 'server.version', [ElXparams.client_name,
                                        ElXparams.protocol_version]
    banner: _CMDT = 'server.banner', []
    features: _CMDT = 'server.features', []
    ping: _CMDT = 'server.ping', []
    add_peer: _CMDT = 'server.add_peer', [ElXparams.features]
    donation_address: _CMDT = 'server.donation_address', []
    peers_subscribe: _CMDT = 'server.peers.subscribe', []


class _mempool(_cmd):
    get_fee_histogram: _CMDT = 'mempool.get_fee_histogram', []


class _address(_cmd):
    get_proof: _CMDT = 'blockchain.address.getproof', [ElXparams.address]


class _block(_cmd):
    header: _CMDT = ('blockchain.block.header',
                     [ElXparams.height, ElXparams.chk_height])
    headers: _CMDT = ('blockchain.block.headers',
                      [ElXparams.start_height, ElXparams.count,
                       ElXparams.chk_height])
    count: _CMDT = 'blockchain.block.count', []


class _headers(_cmd):
    subscribe: _CMDT = 'blockchain.headers.subscribe', [ElXparams.raw]


class _masternode(_cmd):
    subscribe: _CMDT = ('blockchain.masternode.subscribe',
                        ['interface{}{collateral}'])


class _scripthash(_cmd):
    get_balance: _CMDT = ('blockchain.scripthash.get_balance',
                          [ElXparams.scripthash])
    get_history: _CMDT = ('blockchain.scripthash.get_history',
                          [ElXparams.scripthash])
    get_mempool: _CMDT = ('blockchain.scripthash.get_mempool',
                          [ElXparams.scripthash])
    listunspent: _CMDT = ('blockchain.scripthash.listunspent',
                          [ElXparams.scripthash])
    subscribe: _CMDT = ('blockchain.scripthash.subscribe',
                        [ElXparams.scripthash])


class _transaction(_cmd):
    broadcast: _CMDT = ('blockchain.transaction.broadcast',
                        [ElXparams.rawtx])
    get: _CMDT = ('blockchain.transaction.get',
                  [ElXparams.tx_hash, ElXparams.verbose])
    get_merkle: _CMDT = ('blockchain.transaction.get_merkle',
                         [ElXparams.tx_hash, ElXparams.height])
    id_from_pos: _CMDT = ('blockchain.transaction.id_from_pos',
                          [ElXparams.height, ElXparams.tx_pos,
                           ElXparams.merkle])


class _keva(_cmd):
    # Kevacoin specific APIs
    get_hashtag: _CMDT = ('blockchain.keva.get_hashtag',
                          [ElXparams.scripthash, ElXparams.min_tx_num])
    get_keyvalues: _CMDT = ('blockchain.keva.get_keyvalues',
                            [ElXparams.scripthash, ElXparams.min_tx_num])
    get_keyvalue_reactions: _CMDT = ('blockchain.keva.get_keyvalue_reactions',
                                     [ElXparams.tx_hash,
                                      ElXparams.min_tx_num])
    get_transactions_info: _CMDT = ('blockchain.keva.get_transactions_info',
                                    [ElXparams.tx_hashes,
                                     ElXparams.namespace_info])


class _blockchain(_cmd):
    estimatefee: _CMDT = 'blockchain.estimatefee', [ElXparams.number]
    relayfee: _CMDT = 'blockchain.relayfee', []
