from time import localtime, sleep
from boot import s, write_web_info

from microdot_asyncio import Microdot
from sensor import fake_hum, fake_temp
import uasyncio

DATA_FILE = 'data.csv'
COLLECT_DATA = False
DATA_INTERVAL = 5  # seconds


app = Microdot()

homedoc = '''<!DOCTYPE html>
<html>
    <head>
        <title>Env Sensor</title>
    </head>
    <body>
        <div>
            <h1>Home</h1>
            <ul>
                <li><a href="/toggle">Toggle data collection(figuring it out)</a></li>
                <li><a href="/log">View live data</a></li>
                <li><a href="/data">Download data log</a></li>
                <li><a href="/kill">Kill the server</a></li>
            </ul>
        </div>
    </body>
</html>
'''

@app.route('/')
async def index(request):
    return homedoc, 200, {'Content-Type': 'text/html'}


logdoc = '''<!DOCTYPE html>
<html>
    <head>
        <title>Data Log</title>
    </head>
    <body>
        <div>
            <h1>Data Log</h1>
            <p>View current sensor data.</p>
            <p>coming soon.</p>
            <p><a href="/data">All data</a></p>
            <p><a href="/">back</a></p>
        </div>
    </body>
</html>
'''
@app.route('/log')
async def log(request):
    return logdoc, 200, {'Content-Type': 'text/html'}


@app.route('/kill')
async def kill(request):
    request.app.shutdown()
    s.clear()
    s.write('web server', 0, 0)
    s.write('killed', 0, 20)
    return 'The server is down.'


@app.get('/data')
async def read_data_file(request):
    global DATA_FILE
    def read_data():
        file = open(DATA_FILE, 'r')
        for line in file.readlines():
            yield line

    return read_data()


async def log_data():
    '''Log env data for this instance. '''
    global DATA_FILE
    (_, month, day, hour, minute, *_) = localtime()
    date = '{}/{} {}:{}'.format(day, month, hour, minute)
    temp = fake_temp()
    hum = fake_hum()
    file = open(DATA_FILE, 'a')
    file.write('{},{},{}\n'.format(date, str(temp), str(hum)))
    file.close()

# def collect_data_loop():
#     '''Function that lives in a thread and takes(tries to) data in a busy loop. '''
#     while True:
#         global DATA_INTERVAL
#         global COLLECT_DATA
#         if COLLECT_DATA.value():
#             log_data()
#         sleep(DATA_INTERVAL)

async def datatoggle_doc(state):
        doc = '''<!DOCTYPE html>
        <html>
            <head>
                <title>Toggle Data Collection</title>
            </head>
            <body>
                <div>
                    <h1>Data Collection Status</h1>
                    <p>Data collection <b>{}</b>.</p>
                    <p><a href="/">back</a></p>
                </div>
            </body>
        </html>
        '''.format(state)
        return doc


@app.route('/toggle')
async def toggle_datacollection(response):
    global COLLECT_DATA
    COLLECT_DATA = not COLLECT_DATA
    if COLLECT_DATA:
        file = open(DATA_FILE, 'w')
        file.write('date, temperature (F), humidity (%)\n')
        file.close()
        s.clear()
        write_web_info()
        s.write('taking data', 0, 40)
        await log_data() # put some dummy data in
        return datatoggle_doc('enabled'), 200, {'Content-Type': 'text/html'}
    else:
        s.clear()
        write_web_info()
        return datatoggle_doc('disabled'), 200, {'Content-Type': 'text/html'}


app.run(port=80)
