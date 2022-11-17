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
parser.add_argument('--last', default='', help='filter the data to the last NT, where N is an integer and T is a character in {H: hour, D: day, W:week, M:month, Y:year}. i.e. 1W selects the last week of data')

args = parser.parse_args()
datafile = Path(args.datafile)
out = Path(args.out)
header = args.header
footer = args.footer
sep = args.sep
last = args.last

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
if last:
    data = df.last(last)
else:
    data = df


fig, axs = plt.subplots(2, 1)
time_str = '%a %-d, %I:%M %p'
datetimeformat = mdates.DateFormatter(time_str)

plt.suptitle(f'{data.index.min().strftime(f"%b {time_str}")} - {data.index.max().strftime(f"%b {time_str}")}')

# temperature plot
min_ = floor(data.temp.min())
max_ = ceil(data.temp.max())
plt.xticks(rotation=45)
axs[0].plot(data.index, data.temp)
axs[0].set_title('Temperature (F)')
axs[0].set_yticks(range(min_, max_, 4))
axs[0].tick_params(axis="x", rotation=45)
axs[0].xaxis.set_major_formatter(datetimeformat)

# humidity plot
min_ = floor(data.hum.min())
max_ = ceil(data.hum.max())
axs[1].plot(data.index, data.hum)
axs[1].set_title('Humidity (%)')
axs[1].set_yticks(range(min_, max_, 5))
axs[1].tick_params(axis="x", rotation=45)
axs[1].xaxis.set_major_formatter(datetimeformat)

plt.tight_layout()
plt.savefig(out)
