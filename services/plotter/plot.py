"""
parametric plotter for data files
"""
from argparse import ArgumentParser as AP
from datetime import datetime
from math import ceil, floor
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


plt.style.use('ggplot')

parser = AP(description=__doc__)
parser.add_argument('datafile', help='path to the datafile')
parser.add_argument('out', help='path to the newly created plot file')
parser.add_argument('--header', type=int, default=0, help='number of lines in the header. default: 0')
parser.add_argument('--footer', type=int, default=0, help='number of lines in the footer. default: 0')
parser.add_argument('--sep', default=',', help='seperation character used in the datafile')

args = parser.parse_args()
datafile = Path(args.datafile)
out = Path(args.out)
header = args.header
footer = args.footer
sep = args.sep

df = pd.read_csv(datafile, sep=sep, header=header, skipfooter=footer, engine='c')

def pad_zero(x):
    """timestamps ending in 0, must be padded or time parsing fails. """
    if len(x) < 13:
        diff = 13 - len(x) 
        x += '0' * diff
    return x

def to_datetime(x):
    return datetime.strptime(x, '%Y%m%d.%H%M')

df.datetime = df.datetime.astype(str)
df.datetime = df.datetime.transform(pad_zero)
df.datetime = df.datetime.transform(to_datetime)
df.set_index('datetime', inplace=True)
df['temp'] = df['temperature(C)']
df['hum'] = df['humidity(%)']

def C2F(c):
    return c * 9 / 5 + 32

df.temp = C2F(df.temp)
last_hour = df.last('3D')

fig, axs = plt.subplots(2, 1)
datetimeformat = mdates.DateFormatter('%a %-d, %I:%M %p')

# temperature plot
min_ = floor(last_hour.temp.min())
max_ = ceil(last_hour.temp.max())
plt.xticks(rotation=45)
axs[0].plot(last_hour.index, last_hour.temp)
axs[0].set_title('Temperature (F)')
axs[0].set_yticks(range(min_, max_, 4))
axs[0].tick_params(axis="x", rotation=45)
axs[0].xaxis.set_major_formatter(datetimeformat)

# humidity plot
min_ = floor(last_hour.hum.min())
max_ = ceil(last_hour.hum.max())
axs[1].plot(last_hour.index, last_hour.hum)
axs[1].set_title('Humidity (%)')
axs[1].set_yticks(range(min_, max_, 5))
axs[1].tick_params(axis="x", rotation=45)
axs[1].xaxis.set_major_formatter(datetimeformat)

plt.tight_layout()
plt.savefig(out)
