from narwhallet.core.kex.cmd import (_server, _mempool, _blockchain, _address,
                                     _block, _headers, _masternode,
                                     _scripthash, _transaction, _keva)


class _api():
    server = _server
    mempool = _mempool
    blockchain = _blockchain
    blockchain_address = _address
    blockchain_block = _block
    blockchain_headers = _headers
    blockchain_masternode = _masternode
    blockchain_scripthash = _scripthash
    bc_tx = _transaction
    keva = _keva
