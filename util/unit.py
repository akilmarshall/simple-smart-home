"""
Module for creating systemd units (services and timers) using templates (jinja2)
"""
from jinja2 import Template
from pathlib import Path

TEMPLATE_PATH = Path('templates')


def schedule(
        week_day:list|str|None=None,
        year:list|str|int|None=None,
        month:list|str|int|None=None,
        day:list|str|int|None=None,
        hour:list|str|int|None=None,
        min:list|str|int|None=None,
        sec:list|str|int|None=None,
        ):
    """
    Compute an OnCalendar schedule. 

    None options default to -> * (activates indescriminately)
    A list of value may be passed, or any valid timer string
    see man systemd.time for more details

    :week_day:      full name or abbreviated, case does not matter.
    :year:          4 digit year (YYYY) to activate on, probably
                    always None.
    :month:         month of the year (1-12) to activate on.
    :day:           day of the month to activate on.
    :hour:          hour of the day to activate on (0-23)
    :min:           minute of the hour to actiavte on (0-59)
    :sec:           second of the minute to activate on (0-59)
    """
    def parse(s):
        if isinstance(s, list):
            return ','.join(s)
        elif isinstance(s, str) or isinstance(s, int):
            return s
        return '*'

    if isinstance(week_day, list):
        week_day =  ','.join(week_day) + ' '
    elif isinstance(week_day, str):
        week_day += ' '
    elif week_day is None:
        week_day = ''

    return f'{week_day}{parse(year)}-{parse(month)}-{parse(day)} {parse(hour)}:{parse(min)}:{parse(sec)}'

def timer_on_calendar(description:str, schedule:str, persistent:str='false'):
    """
    A realtime (OnCalendar) timer
    """
    timer_template = TEMPLATE_PATH / 'oncalender.timer'
    template_str = open(timer_template.absolute(), 'r').read()
    template = Template(template_str)
    return template.render(description=description, schedule=schedule, persistence=persistent)

def env_service(ip:str, location:str, log:str):
    """
    :script:
    :ip:
    :location:
    :log:
    """
    env_script = Path('.').absolute().parent / 'services' / 'env-node' / 'env-logger.py'
    env_service_template = TEMPLATE_PATH / 'env.service'
    template_str = open(env_service_template.absolute(), 'r').read()
    template = Template(template_str)
    description = f'Service file for the env-logger service. device located at {location} [simple smart home]'
    return template.render(description=description, script=env_script, ip=ip, location=location, log=log)


