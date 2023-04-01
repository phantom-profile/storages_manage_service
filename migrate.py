#!/usr/bin/env python

from sys import argv
from os import system


def up_or_down() -> str:
    if len(argv) < 2 or argv[1].lower() != 'down':
        return 'up'
    return 'down'


def migrate():
    print(f'migrating {up_or_down()}...')
    if up_or_down() == 'up':
        system("yoyo apply -b")
    else:
        system("yoyo rollback -b")

    print('migrating completed!')
    print('reloading sql schema...')
    system("sqlite3 activities_service_db.sqlite3 .schema > db/schema.sql")
    print('reloading sql schema completed!')


migrate()
