from narwhallet.core.kcl.models.cache.actions import MActions
from narwhallet.core.kcl.models.cache.transactions import MTransactions
from narwhallet.core.kcl.models.cache.namespaces import MNamespaces
from narwhallet.core.kcl.db_utils import SQLInterface


class MCache():
    def __init__(self, cache_path):
        self.interface = SQLInterface(cache_path)
        self.actions = MActions(self.interface)
        self.tx = MTransactions(self.interface)
        self.ns = MNamespaces(self.interface)
