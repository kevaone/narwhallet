from narwhallet.core.kex.cmd_base import _cmd
from narwhallet.core.kex.param import ElXparams


class _server(_cmd):
    version = 'server.version', [ElXparams.client_name,
                                 ElXparams.protocol_version]
    banner = 'server.banner', []
    features = 'server.features', []
    ping = 'server.ping', []
    add_peer = 'server.add_peer', [ElXparams.features]
    donation_address = 'server.donation_address', []
    peers_subscribe = 'server.peers.subscribe', []


class _mempool(_cmd):
    get_fee_histogram = 'mempool.get_fee_histogram', []


class _address(_cmd):
    get_proof = 'blockchain.address.getproof', [ElXparams.address]


class _block(_cmd):
    header = 'blockchain.block.header', [ElXparams.height,
                                         ElXparams.chk_height]
    headers = 'blockchain.block.headers', [ElXparams.start_height,
                                           ElXparams.count,
                                           ElXparams.chk_height]
    count = 'blockchain.block.count', []


class _headers(_cmd):
    subscribe = 'blockchain.headers.subscribe', [ElXparams.raw]


class _masternode(_cmd):
    subscribe = 'blockchain.masternode.subscribe', ['interface{}{collateral}']


class _scripthash(_cmd):
    get_balance = 'blockchain.scripthash.get_balance', [ElXparams.scripthash]
    get_history = 'blockchain.scripthash.get_history', [ElXparams.scripthash]
    get_mempool = 'blockchain.scripthash.get_mempool', [ElXparams.scripthash]
    listunspent = 'blockchain.scripthash.listunspent', [ElXparams.scripthash]
    subscribe = 'blockchain.scripthash.subscribe', [ElXparams.scripthash]


class _transaction(_cmd):
    broadcast = 'blockchain.transaction.broadcast', [ElXparams.rawtx]
    get = 'blockchain.transaction.get', [ElXparams.tx_hash, ElXparams.verbose]
    get_merkle = 'blockchain.transaction.get_merkle', [ElXparams.tx_hash,
                                                       ElXparams.height]
    id_from_pos = 'blockchain.transaction.id_from_pos', [ElXparams.height,
                                                         ElXparams.tx_pos,
                                                         ElXparams.merkle]


class _keva(_cmd):
    # Kevacoin specific APIs
    get_hashtag = 'blockchain.keva.get_hashtag', [ElXparams.scripthash,
                                                  ElXparams.min_tx_num]
    get_keyvalues = 'blockchain.keva.get_keyvalues', [ElXparams.scripthash,
                                                      ElXparams.min_tx_num]
    get_keyvalue_reactions = ('blockchain.keva.get_keyvalue_reactions',
                              [ElXparams.tx_hash, ElXparams.min_tx_num])
    get_transactions_info = ('blockchain.keva.get_transactions_info',
                             [ElXparams.tx_hashes, ElXparams.namespace_info])


class _blockchain(_cmd):
    estimatefee = 'blockchain.estimatefee', [ElXparams.number]
    relayfee = 'blockchain.relayfee', []
