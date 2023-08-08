import sys
import pathlib

args = sys.argv[1:]
print(sys.argv)
i1 = input('trust this host [yes/no]: ')
i2 = input('input password: ')

src = pathlib.Path(args[0])
dst = pathlib.Path(args[1].split(':')[1])

dst.unlink(missing_ok=True)

raise Exception('aaaa')
with src.open('r') as f1:
    data = f1.read()

    with dst.open('w') as f2:
        f2.write(data)

print()
print('Success')
