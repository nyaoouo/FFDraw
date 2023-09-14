import pathlib
import queue
import shutil
import threading
import typing
import sqlite3
from nylib.utils import ResEvent

CREATE_TABLE = (
    'CREATE TABLE IF NOT EXISTS rsv_string (key TEXT PRIMARY KEY, data BLOB);'
    'CREATE TABLE IF NOT EXISTS rsf_header (key INTEGER PRIMARY KEY, data BLOB);'
)
INSERT_RSV_STRING = 'INSERT OR IGNORE INTO rsv_string (key, data) VALUES (?, ?);'
INSERT_RSF_HEADER = 'INSERT OR IGNORE INTO rsf_header (key, data) VALUES (?, ?);'
SELECT_RSV_STRING = 'SELECT key, data FROM rsv_string;'
SELECT_RSF_HEADER = 'SELECT key, data FROM rsf_header;'


class Act:
    INSERT_RSV_STRING_SINGLE = 1
    INSERT_RSV_STRING_MULTI = 2
    INSERT_RSF_HEADER_SINGLE = 3
    INSERT_RSF_HEADER_MULTI = 4
    LIST_RSV_STRING = 5
    LIST_RSF_HEADER = 6
    LOAD_NEW_DB = 7


class RsDataHandler:
    db_queue: queue.Queue = queue.Queue()
    db_thread: typing.Optional[threading.Thread] = None

    def __init__(self, db_name):
        self.db_name = db_name

    def db_work(self, wait_time=5):
        if self.db_name is None: return
        self.db_name.parent.mkdir(exist_ok=True, parents=True)
        conn = sqlite3.connect(self.db_name)
        conn.executescript(CREATE_TABLE)
        conn.commit()
        while True:
            try:
                action, args, res = self.db_queue.get(timeout=wait_time)
            except queue.Empty:
                self.db_thread = None
                if conn is not None:
                    conn.close()
                break
            try:
                match action:
                    case Act.INSERT_RSV_STRING_SINGLE:
                        conn.execute(INSERT_RSV_STRING, args)
                        conn.commit()
                        res.set()
                    case Act.INSERT_RSV_STRING_MULTI:
                        conn.executemany(INSERT_RSV_STRING, args)
                        conn.commit()
                        res.set()
                    case Act.INSERT_RSF_HEADER_SINGLE:
                        conn.execute(INSERT_RSF_HEADER, args)
                        conn.commit()
                        res.set()
                    case Act.INSERT_RSF_HEADER_MULTI:
                        conn.executemany(INSERT_RSF_HEADER, args)
                        conn.commit()
                        res.set()
                    case Act.LIST_RSV_STRING:
                        res.set(conn.execute(SELECT_RSV_STRING).fetchall())
                    case Act.LIST_RSF_HEADER:
                        res.set(conn.execute(SELECT_RSF_HEADER).fetchall())
                    case Act.LOAD_NEW_DB:
                        if (src := pathlib.Path(args[0])).exists():
                            conn.close()
                            if self.db_name.exists():
                                self.db_name.unlink()
                            shutil.copy(src, self.db_name)
                            conn = sqlite3.connect(self.db_name)
                            conn.executescript(CREATE_TABLE)
                            conn.commit()
            except Exception as e:
                res.set_exception(e)

    def _start(self, action, args):
        self.db_queue.put((action, args, res := ResEvent()))
        if self.db_thread is None or not self.db_thread.is_alive():
            self.db_thread = threading.Thread(target=self.db_work, daemon=True)
            self.db_thread.start()
        return res

    def insert_rsv_string(self, key: str, data: bytes | bytearray):
        return self._start(Act.INSERT_RSV_STRING_SINGLE, (key, data))

    def insert_rsv_string_multi(self, data: typing.Iterable[tuple[str, bytes | bytearray]]):
        return self._start(Act.INSERT_RSV_STRING_MULTI, data)

    def insert_rsf_header(self, key: int, data: bytes | bytearray):
        return self._start(Act.INSERT_RSF_HEADER_SINGLE, (key, data))

    def insert_rsf_header_multi(self, data: typing.Iterable[tuple[int, bytes | bytearray]]):
        return self._start(Act.INSERT_RSF_HEADER_MULTI, data)

    def list_rsv_string(self):
        return self._start(Act.LIST_RSV_STRING, None)

    def list_rsf_header(self):
        return self._start(Act.LIST_RSF_HEADER, None)

    def load_new_db(self, src: pathlib.Path | str):
        return self._start(Act.LOAD_NEW_DB, (src,))
