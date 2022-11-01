"""
Manage simple-smart-home services.
    list,
    create,
    remove,
    toggle,
    and configure services.
"""
from unit import Schedule, OnCalendar, EnvLoggerScript, EnvLoggerService 


def main():
    from argparse import ArgumentParser
    from pathlib import Path

    config_path = Path('/') / 'etc' / 'simple-smart-home'

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--config', default=config_path, help=f'Path to configuration, specified as a path. default:{config_path}')
    subparsers = parser.add_subparsers(dest='sub', help='sub-command help')
    list_parser = subparsers.add_parser('list', help='list all services (active and inactive)')
    create_parser = subparsers.add_parser('create',  help='create service (make a systemd unit and add to service file')
    remove_parser = subparsers.add_parser('remove', help='remove service, delete from configuration, and delete from service file')
    toggle_parser = subparsers.add_parser('toggle', help='toggle service (set enabled, set disabled, toggle)')
    config_parser = subparsers.add_parser('configure', help='configure (update the services configuration)')

    args = parser.parse_args()
    match args.sub:
        case 'list':
            pass
        case 'create':
            pass
        case 'remove':
            pass
        case 'toggle':
            pass
        case 'configure':
            pass
        case None:
            pass

if __name__ == '__main__':
    main()
