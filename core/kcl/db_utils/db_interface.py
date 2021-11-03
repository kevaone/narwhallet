import sqlite3
from core.kcl.db_utils.db_scripts import Scripts


class SQLInterface():
    def __init__(self, db_file):
        self.db_file = db_file
        self.scripts = Scripts
        self.connection = self.create_connection()
        self.cursor = self.create_cursor()

    def create_connection(self):
        _connection = None
        _connection = sqlite3.connect(self.db_file)
        # _connection.execute('PRAGMA foreign_keys=1;')
        _connection.execute('PRAGMA journal_mode=memory;')
        # _connection.execute('PRAGMA synchronous=off;')
        return _connection

    def create_cursor(self):
        _cursor = self.connection.cursor()
        return _cursor

    def close_cursor(self):
        self.cursor.close()

    def setup_tables(self):
        _tmp = self.execute_sql(self.scripts.SELECT_TX, ('', ), 2)
        if isinstance(_tmp, sqlite3.OperationalError):
            self.execute_sql(self.scripts.CREATE_TX_CACHE, (), 1)
            # print('created tx cache table')

        _tmp = self.execute_sql(self.scripts.SELECT_TX_VIN, ('', ), 2)
        if isinstance(_tmp, sqlite3.OperationalError):
            self.execute_sql(self.scripts.CREATE_TX_VIN_CACHE, (), 1)
            # print('created tx vin cache table')

        _tmp = self.execute_sql(self.scripts.SELECT_TX_VOUT, ('', ), 2)
        if isinstance(_tmp, sqlite3.OperationalError):
            self.execute_sql(self.scripts.CREATE_TX_VOUT_CACHE, (), 1)
            # print('created tx vout cache table')

        _tmp = self.execute_sql(self.scripts.SELECT_NS, ('', ), 2)
        if isinstance(_tmp, sqlite3.OperationalError):
            self.execute_sql(Scripts.CREATE_NS_CACHE, (), 1)
            # print('created ns cache table')

        _tmp = self.execute_sql(self.scripts.SELECT_NFT, ('', ), 2)
        if isinstance(_tmp, sqlite3.OperationalError):
            self.execute_sql(Scripts.CREATE_NFT_CACHE, (), 1)
            # print('created nft cache table')

        _tmp = self.execute_sql(self.scripts.SELECT_ACTION_CACHE_ENTRY,
                                ('', ''), 2)
        if isinstance(_tmp, sqlite3.OperationalError):
            self.execute_sql(self.scripts.CREATE_ACTION_CACHE, (), 1)
            # print('created action cache table')

    def execute_sql(self, sql, payload, flag):
        # SELECT = 3
        # INSERT = 2
        # UPDATE / DELETE = 1
        try:
            self.cursor.execute(sql.value, payload)

            if flag == 1:
                self.connection.commit()
                _return = True
            elif flag == 2:
                self.connection.commit()
                _row_id = self.cursor.lastrowid
                _return = _row_id
            elif flag == 3:
                _rows = self.cursor.fetchall()
                _return = _rows
            else:
                # Flag 0 falls here
                _return = True
        except sqlite3.OperationalError as Ex:
            # print('Ex', Ex, type(Ex))
            _return = Ex
        except sqlite3.IntegrityError as Ex:
            # print('Ex', Ex, type(Ex))
            _return = Ex
        return _return

    def executemany_sql(self, sql, payload, flag):
        try:
            # NOTE Filter execute many calls to insert, add others as needed
            if flag == 2:
                self.cursor.executemany(sql, payload)
                self.connection.commit()
                _return = True
            else:
                # Flag 0 falls here
                _return = False
        except Exception as Ex:
            # print('Ex', Ex)
            _return = Ex
        return _return
