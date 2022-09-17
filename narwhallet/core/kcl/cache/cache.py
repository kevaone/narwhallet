from narwhallet.core.kcl.cache.transactions import MTransactions
from narwhallet.core.kcl.cache.namespaces import MNamespaces
from narwhallet.core.kcl.cache.db_utils import SQLInterface


class MCache():
    def __init__(self, cache_path):
        self.interface = SQLInterface(cache_path)
        self.tx = MTransactions(self.interface)
        self.ns = MNamespaces(self.interface)
