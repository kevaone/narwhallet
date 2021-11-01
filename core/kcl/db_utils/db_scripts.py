from enum import Enum


class Scripts(Enum):
    DROP_TX_CACHE_IDX = 'DROP INDEX tx_cache_idx;'
    DROP_NS_CACHE_IDX = 'DROP INDEX ns_cache_idx;'
    DROP_NFT_CACHE_IDX = 'DROP INDEX nft_cache_idx;'
    CREATE_TX_CACHE_IDX = 'CREATE INDEX tx_cache_idx ON tx_cache (tx, data);'
    CREATE_NS_CACHE_IDX = 'CREATE INDEX ns_cache_idx ON ns_cache (ns, data);'
    CREATE_NFT_CACHE_IDX = 'CREATE INDEX nft_cache_idx ON \
        nft_cache (tx, data);'
    CREATE_TX_CACHE = 'CREATE TABLE tx_cache \
        (txid STRING, hash STRING, version INTEGER, \
            size INTEGER, vsize INTEGER, locktime INTEGER, \
                vin INTEGER, vout INTEGER, blockhash STRING, \
                    confirmations INTEGER, time INTEGER, blocktime INTEGER, \
                        hex STRING);'
    CREATE_TX_VIN_CACHE = 'CREATE TABLE tx_vin_cache \
        (tx STRING, idx INTEGER, txid STRING, vout INTEGER, \
            scriptSig_asm STRING, scriptSig_hex STRING, type STRING, \
                coinbase STRING, txinwitness STRING, sequence INTEGER);'
    CREATE_TX_VOUT_CACHE = 'CREATE TABLE tx_vout_cache \
        (tx STRING, value STRING, n INTEGER, scriptPubKey_asm STRING, \
            scriptPubKey_hex STRING, scriptPubKey_reqSigs INTEGER, \
                scriptPubKey_type STRING, scriptPubKey_addresses TEXT);'
    CREATE_NS_CACHE = 'CREATE TABLE ns_cache \
        (block INTEGER, n INTEGER, txid STRING, ns STRING, op STRING, \
            [key] STRNIG, value STRING, special STRING, address STRING);'
    CREATE_NFT_CACHE = 'CREATE TABLE nft_cache \
        (tx STRING UNIQUE, data STRING);'
    CREATE_ACTION_CACHE = 'CREATE TABLE action_cache \
        (tx STRING UNIQUE, [action] STRING, state INTEGER DEFAULT (0));'
    SELECT_TX = 'SELECT txid FROM tx_cache WHERE txid = ?;'
    SELECT_TX_FULL = 'SELECT txid, hash, version, size, vsize, locktime, \
        vin, vout, blockhash, confirmations, time, blocktime, hex \
            FROM tx_cache WHERE txid = ?;'
    SELECT_TX_VIN = 'SELECT idx, txid, vout, scriptSig_asm, scriptSig_hex, \
        type, coinbase, txinwitness, sequence FROM tx_vin_cache WHERE tx = ?;'
    SELECT_TX_VOUT = 'SELECT value, n, scriptPubKey_asm, scriptPubKey_hex, \
        scriptPubKey_reqSigs, scriptPubKey_type, scriptPubKey_addresses \
            FROM tx_vout_cache WHERE tx = ?;'
    SELECT_NS_ALL = 'SELECT ns, data FROM ns_cache;'
    SELECT_NS = 'SELECT block, n, txid, ns, op, [key], value, special, \
        address FROM ns_cache WHERE ns = ? ORDER BY block desc;'
    SELECT_NS_BY_POS = 'SELECT ns FROM ns_cache WHERE block = ? AND n = ?;'
    SELECT_NS_BY_TXID = 'SELECT ns FROM ns_cache WHERE txid = ? AND ns = ?;'
    SELECT_NS_BY_KEY = 'SELECT ns, [key] FROM ns_cache WHERE ns = ? AND [key] = ?;'
    SELECT_NS_VIEW_1 = 'SELECT DISTINCT ns FROM ns_cache;'
    SELECT_NS_COUNT = 'SELECT COUNT(ns) FROM ns_cache WHERE ns = ?;'
    SELECT_NS_BLOCK = 'SELECT block, n FROM ns_cache WHERE ns = ? \
        ORDER BY block;'
    SELECT_NS_LAST_ADDRESS = 'SELECT address FROM ns_cache WHERE ns = ? \
        ORDER BY block DESC;'
    SELECT_NS_KEY_VALUE = 'SELECT value FROM ns_cache \
        WHERE ns = ? AND [key] = ? ORDER BY block DESC;'
    SELECT_NS_AUCTIONS = 'SELECT block, n, ns, value FROM ns_cache \
        WHERE ns = ? AND special = \'nft_auction\' ORDER BY block DESC;'
    SELECT_NS_BIDS = 'SELECT block, n, ns, value FROM ns_cache \
        WHERE ns = ? AND special = \'nft_bid\' ORDER BY block DESC;'
    SELECT_NS_ROOT_TEST = 'SELECT ns FROM ns_cache \
        WHERE ns = ? AND [key] = "_KEVA_NS_";'
    SELECT_NFT = 'SELECT tx, data FROM nft_cache WHERE tx = ?;'
    SELECT_ACTION_CACHE_ALL = 'SELECT tx, [action], state FROM action_cache;'
    SELECT_ACTION_CACHE_ENTRY = 'SELECT tx, [action], state FROM action_cache WHERE tx = ? AND [action] = ?;'
    INSERT_TX = 'INSERT INTO tx_cache (txid, hash, version, size, vsize, \
        locktime, vin, vout, blockhash, confirmations, time, blocktime, \
            hex) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
    INSERT_TX_VIN = 'INSERT INTO tx_vin_cache (tx, idx, txid, vout, \
        scriptSig_asm, scriptSig_hex, type, coinbase, txinwitness, \
            sequence) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
    INSERT_TX_VOUT = 'INSERT INTO tx_vout_cache (tx, value, n, \
        scriptPubKey_asm, scriptPubKey_hex, scriptPubKey_reqSigs, \
            scriptPubKey_type, scriptPubKey_addresses) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);'
    INSERT_NS = 'INSERT INTO ns_cache (block, n, txid, ns, op, [key] , value, \
        special, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);'
    INSERT_NFT = 'INSERT INTO nft_cache (tx, data) VALUES (?, ?);'
    INSERT_ACTION_CACHE = 'INSERT INTO action_cache (tx, [action]) \
        VALUES (?, ?);'
    UPDATE_TX = 'UPDATE tx_cache SET txid = ?, hash = ?, version = ?, \
        size = ?, vsize = ?, locktime = ?, vin = ?, vout = ?, \
            blockhash = ?, confirmations = ?, time = ?, blocktime = ?, \
                hex = ? WHERE txid = ?;'
    UPDATE_NS_KEY = 'UPDATE ns_cache SET block = ?, n = ?, txid = ?, \
        value = ?, special = ?, address = ? WHERE ns = ? AND [key] = ? \
            AND block < ?;'
    UPDATE_NFT = 'UPDATE nft_cache SET tx = ?, data = ? WHERE tx = ?;'
    UPDATE_ACTION_CACHE = 'UPDATE action_cache SET state = ? \
        WHERE tx = ? AND [action] = ?;'
    DELETE_TX = 'DELETE FROM tx_cache WHERE tx = ?;'
    DELETE_NS = 'DELETE FROM ns_cache WHERE ns = ?;'
    DELETE_NS_KEY = 'DELETE FROM ns_cache WHERE ns = ? AND [key] = ? \
        AND block < ?;'
    DELETE_NFT = 'DELETE FROM nft_cache WHERE tx = ?;'
    DELETE_ACTION_CACHE = 'DELETE FROM action_cache WHERE tx = ? \
        AND [action] = ?;'
