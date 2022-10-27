#!/usr/bin/python3
"""
env-logger
sample an env-node at a specified location and append the returned data
to the log directory.
"""
from argparse import ArgumentParser
from datetime import datetime
from requests import get
from sys import exit
from pathlib import Path


LOG_DIR = Path('/') / 'var' / 'env-log'
LOG_DIR = '/var/env-log'

def headers(ip):
    """
    sample an env sensor at http://<ip>/headers, 
    return the data headers or fails
    """
    address = f'http://{ip}/headers'
    response = get(address)
    if response.ok:
        return response.text
    else:
        exit(f'failed to get header data from {ip}\n{response.status_code = }')

def sample(ip):
    """
    sample an env sensor at http://<ip>, 
    return the data or fail
    """
    address = f'http://{ip}'
    response = get(address)
    if response.ok:
        return response.text
    else:
        exit(f'failed to sample data from {ip}\n{response.status_code = }')

def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('ip', help='address of the env-node, i.e. 192.168.1.x') 
    parser.add_argument('location', help='location the env-senor is in. i.e. living-room.') 
    parser.add_argument('--log', default=LOG_DIR, help=f'root location of the log directory. default:{LOG_DIR}') 

    args = parser.parse_args()
    log_path = Path(args.log)
    ip = args.ip

    # setup log file directory
    if not log_path.exists():
        log_path.mkdir(parents=True, exist_ok=True)

    log_file_path = log_path / f'{args.location}.log'
    log_file = open(log_file_path, 'a')

    # if log doesnt exist, write headers
    if log_file_path.stat().st_size == 0:
        if header:= headers(ip):
            log_file.write(f'# datetime format: YYYYMMDD.HHMM\n')
            log_file.write(f'datetime,{header}\n')

    now = datetime.now()
    if data:= sample(ip):
        log_file.write(f'{now.year}{now.month}{now.day}.{now.hour}{now.minute:02},{data}\n')

    log_file.close()


if __name__ == '__main__':
    main()
