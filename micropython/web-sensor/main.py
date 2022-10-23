from sensor import fake_temp, fake_hum
from microdot import Microdot

app = Microdot()

@app.route('/')
def index(_):
    return f'{fake_temp()},{fake_hum()}'

@app.route('/headers')
def headers(_):
    return 'temperature(F),humidity(%)'

app.run(port=80)
