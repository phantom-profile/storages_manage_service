import sys
import subprocess
import pathlib


# Stubs collection for emulating cmdline tools
class CmdlineStub:
    def __init__(self, tool_name: str, args: list, with_pass: bool = False):
        if tool_name not in self.tools:
            raise RuntimeError(f'tool {tool_name} not registered')

        self.tool_name = tool_name
        # for emulating access via password input
        self.with_pass = with_pass
        self.cmd_args = args
        print(self.cmd_args)

    def launch(self):
        return self.tools[self.tool_name]()

    @property
    def tools(self):
        return {
            "ssh": self.ssh,
            "scp": self.scp
        }

    def ssh(self):
        if self.with_pass:
            input('input password: ')

        cmd = self.cmd_args[1]
        print(f'executing "{cmd}"')
        proc = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()

        print('\nFinished with', proc.returncode)

    def scp(self):
        if self.with_pass:
            input('input password: ')

        src = pathlib.Path(args[0])
        dst = pathlib.Path(args[1].split(':')[1])
        dst.unlink(missing_ok=True)

        with src.open('r') as f1:
            data = f1.read()

            with dst.open('w') as f2:
                f2.write(data)

        print('\nFinished')


def main():
    cmd = sys.argv[1]
    args = sys.argv[2:]
    CmdlineStub(tool_name=cmd, args=args)


if __name__ == '__main__':
    main()
