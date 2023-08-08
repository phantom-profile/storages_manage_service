import json
import subprocess
import pathlib

FILENAME = pathlib.Path(__file__).name
CONFIG_FILE = pathlib.Path(__file__).parent / 'config.json'


class ConfigParser:
    NO_FILE_ERROR = 'Add file config.json to same dir where this script located'
    WRONG_CONFIG_ERROR = f'No copied or target or password pathes provided to config.json file'

    class ConfigError(Exception):
        ...

    def __init__(self, filepath: pathlib.Path):
        if not filepath.exists():
            raise self.ConfigError(self.NO_FILE_ERROR)

        self.filepath = filepath
        self.opts = {}

    def parse(self):
        with self.filepath.open('r') as config:
            main_opts = json.load(config)

        if main_opts['testing']:
            self.opts = main_opts['test_cfg']
        else:
            self.opts = main_opts['prod_cfg']

        if not all(self.must_filled_fields):
            raise self.ConfigError(self.WRONG_CONFIG_ERROR)

        return self.opts

    @property
    def must_filled_fields(self) -> list:
        return [
            self.opts.get('password_file'),
            self.opts.get('copied_file'),
            self.opts.get('target_location'),
            self.opts.get('target_host'),
            self.opts.get('md5_journal_location')
        ]


class DataTransitionClient:
    def __init__(self, opts: dict[str, str]):
        self.opts = opts
        self.password = ''

    def get_password(self):
        if self.password:
            return self.password

        pass_file = self.opts['password_file']
        with open(pass_file) as file:
            self.password = (file.read().strip() + '\n').encode('utf-8')
            return self.password

    def transfer_file_to_remote(self):
        file_dst = f"{self.opts['target_host']}:{self.opts['target_location']}"
        proc = subprocess.Popen(
            [*self.opts['rsync_call'], self.opts['copied_file'], file_dst],
            stdin=subprocess.PIPE
        )
        if self.opts['use_password']:
            self.input_password(proc)

        proc.wait()

    def trigger_slave(self, command):
        jrnl_location = self.opts["md5_journal_location"]
        target_location = self.opts['target_location']
        slave_exec = f'"python3 sum_register_slave.py {command} {jrnl_location} {target_location}"'
        proc = subprocess.Popen(
            [*self.opts['ssh_call'], self.opts['target_host'], slave_exec],
            stdin=subprocess.PIPE
        )
        if self.opts['use_password']:
            self.input_password(proc)

        proc.wait()

    def input_password(self, proc):
        proc.stdin.write(b'yes\n')
        proc.stdin.flush()
        proc.stdin.write(self.get_password())
        proc.stdin.flush()


def main():
    opts = ConfigParser(CONFIG_FILE).parse()
    client = DataTransitionClient(opts)

    client.trigger_slave('new_line')
    client.transfer_file_to_remote()
    client.trigger_slave('check_sum')


if __name__ == '__main__':
    main()
