"""
Utility script to manage centrak.
"""
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import argparse
from routes import authnz
from datetime import datetime



# HACK: using cork.Cork, admin user required, but this is a utility
# shell script meant to help in quick user creation.. hence the HACK
def _create_user(username, password, role='user'):
    if username in authnz._store.users:
        print("error: User already exists.")
        return
    if role not in authnz._store.roles:
        print("error: Role doesn't exist.")
        return

    tstamp = str(datetime.utcnow())
    h = authnz._hash(username, password)
    h = h.decode('ascii')
    authnz._store.users[username] = {
        'role': role,
        'hash': h,
        'email_addr': None,
        'desc': None,
        'creation_date': tstamp,
        'last_login': tstamp
    }
    authnz._store.save_users()
    print('User Created.\n')


def _create_role(role, level):
    if role in authnz._store.roles:
        raise Exception("error: Role already exist.")
    
    authnz._store.roles[role] = level
    authnz._store.save_roles()


def _setup_roles():
    roles = (
        ('admin',     100),
        ('moderator',  80),
        ('team-lead',  70),
        ('member',     60),
        ('user',       50)
    )
    
    try:
        for role, level in roles:
            _create_role(role, level)
        print('Roles setup successful!')
    except Exception as ex:
        print('Roles setup failed: %s' % str(ex))
        raise ex


def _list_users():
    line_fmt = '{0:20} {1:10}'
    header = line_fmt.format('USER', 'ROLE')

    print('\n{0}\n{1}'.format(header, '-'*31))
    for info in authnz.list_users():
        print(line_fmt.format(info[0], info[1]))
    print()


def _list_roles():
    line_fmt = '{0:10} {1:5}'
    header = line_fmt.format('ROLE', 'LEVEL')

    print('\n{0}\n{1}'.format(header, '-'*16))
    for info in authnz.list_roles():
        print(line_fmt.format(info[0], info[1]))
    print()


def _create_parser():
    parser = argparse.ArgumentParser(description='CENTrak Management Script')
    add = parser.add_argument
    add('-d', '--delete-user')
    add('--delete-role')
    add('-l', '--list-users', action='store_true')
    add('--list-roles', action='store_true')
    add('--setup-roles', action='store_true')
    # add('--reset-password', nargs=2)
    
    subparser = parser.add_subparsers(help='create user commands')
    parser_cu = subparser.add_parser('create-user')
    add_cu = parser_cu.add_argument
    add_cu('username')
    add_cu('password')
    add_cu('-r', '--role')
    return parser


def run(args):
    if 'username' in args:
        call_args = [args.username, args.password]
        if args.role:
            call_args.append(args.role)
        _create_user(*call_args)
        return
    
    if args.list_users:
        _list_users()
        return

    if args.list_roles:
        _list_roles()
        return
    
    if args.setup_roles:
        _setup_roles()
        return

if __name__ == '__main__':
    args = _create_parser().parse_args()
    run(args)

