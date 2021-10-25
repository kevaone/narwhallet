from core.kcl.bip_utils.base58 import Base58Encoder
from core.kcl.bip_utils.utils import ConvUtils
from core.kcl.models.namespace import MNamespace
from core.kcl.db_utils import SQLInterface
from core.kcl.db_utils import Scripts


class MNamespaces():
    # @property
    # def count(self) -> int:
    #     return len(self.namespaces)

    @staticmethod
    def sort(item):
        return item[0]

    @staticmethod
    def sort_dict(item):
        return item['date']

    @staticmethod
    def convert_to_namespaceid(nsid: str) -> str:
        try:
            _id = Base58Encoder.CheckEncode(ConvUtils.HexStringToBytes(nsid))
            return _id
        except Exception:
            raise Exception('Invailid Namespaceid')

    @staticmethod
    def _decode(value):
        try:
            _d2 = ConvUtils.IntegerToBytes(int(value), None, 'little').decode()
        except Exception:
            try:
                _d2 = ConvUtils.HexStringToBytes(value).decode()
            except Exception:
                _d2 = value
                # print('error', _d2, value)
        return _d2

    def _fromRawValues(self, block: int, n: int, tx: str,
                       namespaceid: str, op: str, key: str, value: str,
                       special: str, address: str,
                       cache_interface: SQLInterface):

        _ns = self.convert_to_namespaceid(namespaceid)
        _row = cache_interface.execute_sql(Scripts.INSERT_NS,
                                           (block, n, tx, _ns, op,
                                            self._decode(key),
                                            self._decode(value),
                                            special, address), 2)
        return _row

    def _get_namespace_by_id(self, txid: str, namespaceid: str,
                             cache_interface: SQLInterface) -> MNamespace:
        _ns = self.convert_to_namespaceid(namespaceid)
        _ns = cache_interface.execute_sql(Scripts.SELECT_NS_BY_TXID,
                                          (txid, _ns, ), 3)
        return _ns

    def get_namespace_by_id(self, namespaceid: str,
                            cache_interface: SQLInterface) -> MNamespace:
        _ns = cache_interface.execute_sql(Scripts.SELECT_NS,
                                          (namespaceid, ), 3)
        return _ns

    def get_ns_by_shortcode(self, shortcode: int,
                            cache_interface: SQLInterface) -> MNamespace:
        _bs = str(shortcode)
        _block = int(_bs[1:int(_bs[0])+1])

        if int(_bs[0])+1 < len(_bs):
            _n = int(_bs[int(_bs[0])+1:])
            _ns_id = cache_interface.execute_sql(Scripts.SELECT_NS_BY_POS,
                                                 (_block, _n), 3)
        else:
            _ns_id = []

        if len(_ns_id) == 1:
            _ns = cache_interface.execute_sql(Scripts.SELECT_NS,
                                              (_ns_id[0][0], ), 3)
        else:
            _ns = []

        return _ns

    def get_root_namespace_by_id(self, namespaceid: str,
                                 cache_interface: SQLInterface,
                                 convert: bool = False) -> MNamespace:
        if convert is True:
            namespaceid = self.convert_to_namespaceid(namespaceid)
        _ns = cache_interface.execute_sql(Scripts.SELECT_NS_ROOT_TEST,
                                          (namespaceid, ), 3)
        return _ns

    # def update_namespace(self, ns: MNamespace,
    #                      cache_interface: SQLInterface):
    #     #self.ns_cache.update(_ns, _db_cache)
    #     _result = cache_interface.execute_sql(Scripts.UPDATE_NS,
    #                                           (json.dumps(ns.toDict()),
    #                                            ns.namespaceid), 1)
