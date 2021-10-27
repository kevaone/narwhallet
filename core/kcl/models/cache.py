from core.kcl.models.actions import MActions
from core.kcl.models.transactions import MTransactions
from core.kcl.models.namespaces import MNamespaces
from core.kcl.db_utils import SQLInterface


class MCache():
    def __init__(self, cache_path):
        self.interface = SQLInterface(cache_path)
        self.actions = MActions(self.interface)
        self.tx = MTransactions(self.interface)
        self.ns = MNamespaces(self.interface)
