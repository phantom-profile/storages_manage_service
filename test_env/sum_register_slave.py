import pathlib
import sys
from typing import Any


class CheckSumRegister:
    """
    register journal file format:
    1 - abcabc123
    2 -
    ...
    1000 - abcabc123
    """

    def __init__(self, opts: dict[str, Any]):
        self._opts = opts
        self._target_file = pathlib.Path(opts['target_location'])
        self._journal_file = pathlib.Path(opts['md5_journal_location'])

    def add_new_line(self):
        index = self._get_index()
        with self._journal_file.open('a') as file:
            file.write(f'\n{index} - ')

    def register_sum_to_journal(self):
        with self._journal_file.open('a') as file:
            file.write(self._calc_hash_sum())

    def _calc_hash_sum(self):
        return self._target_file.name

    def _get_index(self):
        if not self._journal_file.exists():
            return 1

        with self._journal_file.open('r') as file:
            index = file.readlines()
            if not index:
                return 1
            index = index[-1].split(' - ')[0].strip()
            if not index:
                return 1
            return int(index) + 1


def main():
    args = sys.argv[1:]
    command = args[0]
    opts = {
        'md5_journal_location': args[1],
        'target_location': args[2]
    }
    registartor = CheckSumRegister(opts)
    if command == 'new_line':
        registartor.add_new_line()
    elif command == 'check_sum':
        registartor.register_sum_to_journal()


if __name__ == '__main__':
    main()
