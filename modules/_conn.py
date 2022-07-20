import sqlite3
from typing import *

from pygame import Cursor


class _Conn(sqlite3.Connection):
    def __init__(self, path) -> None:
        super().__init__(path)
        self._path = path

    def __enter__(self) -> Cursor:
        return self.cursor()

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.cursor().close()
        self.close()
        if exc_traceback is None:
            ...
        else:
            ...

    def __repr__(self) -> str:
        return '_conn(path = %s)' % self._path

