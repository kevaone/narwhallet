from narwhallet.core.kcl.cache.db_utils import SQLInterface


class MActions():
    def __init__(self, db_interface: SQLInterface):
        self.dbi = db_interface

    def all(self, state: int):
        _r = self.dbi.execute_sql(self.dbi.scripts.SELECT_ACTION_CACHE_ALL,
                                  (state, ), 3)
        return _r

    def get(self, tx: str, action: str):
        _r = self.dbi.execute_sql(self.dbi.scripts.SELECT_ACTION_CACHE_ENTRY,
                                  (tx, action), 3)
        return _r

    def add(self, tx: str, action: str, data: str):
        _r = self.dbi.execute_sql(self.dbi.scripts.INSERT_ACTION_CACHE,
                                  (tx, action, data), 2)
        return _r

    def update(self, time: str, tx: str, action: str, state: int):
        _r = self.dbi.execute_sql(self.dbi.scripts.UPDATE_ACTION_CACHE,
                                  (state, time, tx, action), 1)
        return _r

    def delete(self, tx: str, action: str):
        _r = self.dbi.execute_sql(self.dbi.scripts.DELETE_ACTION_CACHE,
                                  (tx, action), 1)
        return _r