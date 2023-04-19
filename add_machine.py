import sqlite3
from dataclasses import dataclass


@dataclass
class AddMachine:
    filename: str
    _table_name = 'machines'

    def __post_init__(self) -> None:
        self._create_db()

    def _create_db(self) -> None:
        with sqlite3.connect(self.filename) as conn:
            cursor = conn.cursor()
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {self._table_name} (ip text NOT NULL, mac text NOT NULL)')

    def add_machine(self, ip: str, mac: str) -> None:
        if not ip:
            raise Exception('Cannot add machine, ip is empty')
        if not mac:
            raise Exception('Cannot add machine, mac is empty')
        with sqlite3.connect(self.filename) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self._table_name} WHERE ip = ?", (ip,))
            row = cursor.fetchone()
            if row:
                cursor.execute(f"UPDATE {self._table_name} SET mac = ? WHERE ip = ?", (mac, ip))
            else:
                cursor.execute(f"INSERT INTO {self._table_name} (ip, mac) VALUES (?, ?)", (ip, mac))
            conn.commit()

    def contains_ip(self, value: str) -> list[tuple[str, str], ...] | list[None]:
        """Returns a list of tuple(s) if value found, otherwise return empty list"""
        with sqlite3.connect(self.filename) as conn:
            cursor = conn.cursor()
            # cursor.execute('SELECT * FROM {self._table_name} WHERE ip=:c', {'c': value})
            cursor.execute(f'SELECT * FROM {self._table_name} WHERE ip=?', (value,))
            ips_search: list = cursor.fetchall()
            return ips_search

    def get_all_rows(self) -> list[tuple[str, str], ...] | list[None]:
        """Returns a list of tuple[str, str] of all rows"""
        with sqlite3.connect(self.filename) as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM {self._table_name}')
            ips_search: list = cursor.fetchall()
            return ips_search
