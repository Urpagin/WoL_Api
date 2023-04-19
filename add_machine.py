import csv
import os.path

import polars as pl


class AddMachine:
    def __init__(self, filename: str, ip: str | None = None, mac: str | None = None) -> None:
        self.filename = filename
        self.ip = ip
        self.mac = mac

        self.create_csv()
        self._verify_file()

    def _verify_file(self):
        if not os.path.isfile(self.filename):
            return
        try:
            df = pl.read_csv(self.filename)
            _ = df['IP'], df['MAC']
        except Exception:
            self.create_csv(override=True)

    def verify_file(self):

        with open(self.filename, 'r', encoding='utf-8', newline='') as file:
            data = file.readlines()
        data[0] = 'IP,MAC\n'
        with open(self.filename, 'w', encoding='utf-8') as file:
            file.writelines(data)
        try:
            pl.read_csv(self.filename)
        except Exception:
            self.create_csv(override=True)

    def create_csv(self, override: bool = False) -> None:
        if os.path.isfile(self.filename) and not override:
            return
        with open(self.filename, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(('IP', 'MAC'))

    def add_machine(self) -> None:
        if self.ip is None:
            raise Exception('Cannot add machine, ip is empty')
        elif self.mac is None:
            raise Exception('Cannot add machine, mac is empty')

        with open(self.filename, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow((self.ip, self.mac))

    def read_csv(self) -> pl.dataframe.frame.DataFrame:
        if not os.path.isfile(self.filename):
            raise Exception('Cannot read file, file does not exist')

        return pl.read_csv(self.filename)
