import sys
import subprocess


args = sys.argv[1:]
print(sys.argv)
i1 = input('trust this host [yes/no]: ')
i2 = input('input password: ')

cmd = args[1]

print(f'executing {cmd}')
proc = subprocess.Popen(cmd.strip('"').split(' '), stdin=subprocess.PIPE)
proc.wait()
print(proc)

print()
print('Success')
