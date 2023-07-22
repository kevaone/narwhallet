from narwhallet.core.kex.cmd_base import _cmd


class _server(_cmd):
    @staticmethod
    def version(client_name, protocol_version, eid: int):
        return _cmd.build_command('server.version',
                                  [client_name, protocol_version], eid)

    @staticmethod
    def banner(eid: int):
        return _cmd.build_command('server.banner', [], eid)

    @staticmethod
    def features(eid: int):
        return _cmd.build_command('server.features', [], eid)

    @staticmethod
    def ping(eid: int):
        return _cmd.build_command('server.ping', [], eid)

    @staticmethod
    def add_peer(features, eid: int):
        return _cmd.build_command('server.add_peer', [features], eid)

    @staticmethod
    def donation_address(eid: int):
        return _cmd.build_command('server.donation_address', [], eid)

    @staticmethod
    def peers_subscribe(eid: int):
        return _cmd.build_command('server.peers.subscribe', [], eid)


class _mempool(_cmd):
    @staticmethod
    def get_fee_histogram(eid: int):
        return _cmd.build_command('mempool.get_fee_histogram', [], eid)


class _address(_cmd):
    @staticmethod
    def get_proof(address, eid: int):
        return _cmd.build_command('blockchain.address.getproof',
                                  [address], eid)


class _block(_cmd):
    @staticmethod
    def header(height, chk_height, eid: int):
        return _cmd.build_command('blockchain.block.header',
                                  [height, chk_height], eid)

    @staticmethod
    def headers(start_height, count, chk_height, eid: int):
        return _cmd.build_command('blockchain.block.headers',
                                  [start_height, count, chk_height], eid)

    @staticmethod
    def count(eid: int):
        return _cmd.build_command('blockchain.block.count', [], eid)


class _headers(_cmd):
    @staticmethod
    def subscribe(raw, eid: int):
        return _cmd.build_command('blockchain.headers.subscribe', [raw], eid)


class _masternode(_cmd):
    @staticmethod
    def subscribe(eid: int):
        return _cmd.build_command('blockchain.masternode.subscribe',
                                  [], eid)


class _scripthash(_cmd):
    @staticmethod
    def get_balance(scripthash, eid: int):
        return _cmd.build_command('blockchain.scripthash.get_balance',
                                  [scripthash], eid)

    @staticmethod
    def get_history(scripthash, eid: int):
        return _cmd.build_command('blockchain.scripthash.get_history',
                                  [scripthash], eid)

    @staticmethod
    def get_mempool(scripthash, eid: int):
        return _cmd.build_command('blockchain.scripthash.get_mempool',
                                  [scripthash], eid)

    @staticmethod
    def listunspent(scripthash, eid: int):
        return _cmd.build_command('blockchain.scripthash.listunspent',
                                  [scripthash], eid)

    @staticmethod
    def subscribe(scripthash, eid: int):
        return _cmd.build_command('blockchain.scripthash.subscribe',
                                  [scripthash], eid)


class _transaction(_cmd):
    @staticmethod
    def broadcast(rawtx, eid: int):
        return _cmd.build_command('blockchain.transaction.broadcast',
                                  [rawtx], eid)

    @staticmethod
    def get(tx_hash, verbose, eid: int):
        return _cmd.build_command('blockchain.transaction.get',
                                  [tx_hash, verbose], eid)

    @staticmethod
    def get_merkle(tx_hash, height, eid: int):
        return _cmd.build_command('blockchain.transaction.get_merkle',
                                  [tx_hash, height], eid)

    @staticmethod
    def id_from_pos(height, tx_pos, merkle, eid: int):
        return _cmd.build_command('blockchain.transaction.id_from_pos',
                                  [height, tx_pos, merkle], eid)


class _keva(_cmd):
    # Kevacoin specific APIs
    @staticmethod
    def get_hashtag(scripthash, min_tx_num, eid: int):
        return _cmd.build_command('blockchain.keva.get_hashtag',
                                  [scripthash, min_tx_num], eid)

    @staticmethod
    def get_keyvalues(scripthash, min_tx_num, eid: int):
        return _cmd.build_command('blockchain.keva.get_keyvalues',
                                  [scripthash, min_tx_num], eid)

    @staticmethod
    def get_keyvalue_reactions(tx_hash, min_tx_num, eid: int):
        return _cmd.build_command('blockchain.keva.get_keyvalue_reactions',
                                  [tx_hash, min_tx_num], eid)

    @staticmethod
    def get_transactions_info(tx_hashes, namespace_info, eid: int):
        return _cmd.build_command('blockchain.keva.get_transactions_info',
                                  [tx_hashes, namespace_info], eid)


class _blockchain(_cmd):
    @staticmethod
    def estimatefee(in_blocks: int, eid: int):
        return _cmd.build_command('blockchain.estimatefee', [in_blocks], eid)

    @staticmethod
    def relayfee(eid: int):
        return _cmd.build_command('blockchain.relayfee', [], eid)

class _custom(_cmd):
    @staticmethod
    def get_nft_auctions(eid: int):
        return _cmd.build_command('get_nft_auctions', [], eid)

    @staticmethod
    def get_web_content(host, path, eid:int):
        return _cmd.build_web_command('GET', [host, path], eid)