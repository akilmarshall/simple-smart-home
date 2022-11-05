#!/usr/bin/python3
"""
Manage simple-smart-home services.
    list,
    create,
    remove,
    toggle,
    and configure services.
"""
from argparse import ArgumentParser
import os
from pathlib import Path

from manage_unit import enable, status, disable
from unit import EnvLoggerScript, EnvLoggerService, Schedule, TimerOnCalendar

UNIT_PATH = Path('/') / 'etc' / 'systemd' / 'system'
# roster file for services (contains a list of services [active and inactive])
# the systemd units that have been created and must be managed
SERVICE_FILE = Path('/') / 'etc' / 'simple-smart-home.services'  

def load_services() -> list[str] | None:
    if SERVICE_FILE.exists():
        services = []
        with open(SERVICE_FILE, 'r') as f:
            for line in f.readlines():
                services.append(line.strip())
        return services

def write_services(services):
    with open(SERVICE_FILE, 'w') as f:
        for service in services:
            f.write(f'{service}\n')


def make_env_unit(schedule:Schedule, ip:str, location:str, log:Path):
    timer = TimerOnCalendar(f'timer for env-logger at {location}', schedule) 
    script = EnvLoggerScript(ip, location, log)
    service = EnvLoggerService(f'service file for env-logger at {location}', script) 
    timer_file_name = f'env-logger-{location}.timer'
    service_file_name = f'env-logger-{location}.service'
    with open(UNIT_PATH / timer_file_name, 'w') as f:
        f.write(str(timer))
    with open(UNIT_PATH / service_file_name, 'w') as f:
        f.write(str(service))
    enable(timer_file_name)

def remove_unit(unit:str, service=True, timer=True):
    if service:
        os.remove(UNIT_PATH / f'{unit}.service')
    if timer:
        os.remove(UNIT_PATH / f'{unit}.timer')



def make_env_parser(parser: ArgumentParser):
    parser.add_argument('ip', help='ip address of the edge device to monitor.')
    parser.add_argument('location', help='brief one word (no white space) description of the physical location of the env Edge Device.')
    parser.add_argument('log', type=Path, help='absolute path to the directory to write date files')
    parser.add_argument('n', type=int, help='minute interval to take measurements')
    return parser

def main():

    config_path = Path('/') / 'etc' / 'simple-smart-home'

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--config', default=config_path, help=f'Path to configuration, specified as a path. default:{config_path}')
    subparsers = parser.add_subparsers(dest='sub', help='sub-command help')
    list_parser = subparsers.add_parser('list', help='list all services (active and inactive)')
    # create_parser = subparsers.add_parser('create', help='create service (make a systemd unit and add to service file')
    make_env_parser(subparsers.add_parser('create-env', help='create env-logger service, parameterized by (ip, location, log-path, n)'))
    remove_parser = subparsers.add_parser('remove', help='remove service, delete from configuration, and delete from service file')
    remove_parser.add_argument('service', help='name of service to remove')
    toggle_parser = subparsers.add_parser('toggle', help='toggle service (set enabled, set disabled, toggle)')
    toggle_parser.add_argument('service', help='name of service to toggle')
    config_parser = subparsers.add_parser('configure', help='configure (update the services configuration)')

    args = parser.parse_args()
    services = load_services()  # load in service population from SERVICE_FILE 
    match args.sub:
        case 'list':
            if services:
                for service in services:
                    print(f'{service}', end='\t')
                    print(status(f'{service}.timer'))
            else:
                print('no installed services')
        case 'create-env':
            ip = args.ip
            location = args.location
            log = args.log
            n = args.n

            schedule = Schedule(minute=f'0/{n}')
            make_env_unit(schedule, ip, location, log)
            service = f'env-logger-{location}'
            # append to services population
            if services:
                services.append(service)  
            else:
                services = [service]
            print(f'created: {service}')
        case 'remove':
            service = args.service
            if services and service in services:
                services.remove(service)  # remove from services population
                remove_unit(service)
                print(f'removed: {service}')
            else:
                print(f'I cant find a service called: {service}')
                print(services)

        case 'toggle':
            service = args.service
            if services and service in services:
                match status(f'{service}.timer'):
                    case 'enabled':
                        disable(f'{service}.timer')
                        print(f'disabled {service}')
                    case 'disabled':
                        enable(f'{service}.timer')
                        print(f'enabled {service}')
            else:
                print(f'I cant find a service called: {service}')
                print(services)
        case 'configure':
            pass
        case None:
            pass
    if services:
        write_services(services)
    else:
        write_services([])

if __name__ == '__main__':
    main()
