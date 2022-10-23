from argparse import ArgumentParser
from time import sleep
from datetime import datetime
from requests import get
from sys import exit


description = '''\
        A script that samples an env-sensor n times
        Outputs to stdout.
'''
parser = ArgumentParser(description=description)
parser.add_argument('endpoint', help='address of the env-node. only ip no protocol. 192.168.1.x') 
parser.add_argument('samples', type=int,  help='number of data samples to take') 
parser.add_argument('delay', type=int, help='delay in seconds between samples') 

args = parser.parse_args()

samples = args.samples
delay = args.delay
address = f'http://{args.endpoint}'

response = get(f'{address}/headers')

if response.ok:
    now = datetime.now()
    print(f'# year-month-day')
    print(f'# {now.year}-{now.month}-{now.day}')
    print(f'{response.text},hour,minute,second')
else:
    exit(f'no endpoint found at {address}, check that the device is up.')

for _ in range(samples):
    now = datetime.now()
    response = get(address)
    if response.ok:
        time = f'{now.hour},{now.minute},{now.second}'
        row = f'{response.text},{time}'
        print(row)
    else:
        print('device could not be reached..')
    sleep(delay)
