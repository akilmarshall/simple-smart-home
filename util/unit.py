"""
Module for creating systemd units (service and timer pairs) using templates (jinja2)
Timers (only realtime currently) and Services (correlate to Edge Device services) are represented with classes that implement __str__ to render valid systemd timer and services files.
Both are built up using primitive data members or classes when appropriate.
"""
from pathlib import Path

from jinja2 import Template


TEMPLATE_PATH = Path('templates')
LOG_PATH = Path('/') / 'var' / 'simple-smart-home'

class Schedule:
    """
    Class representing an onCalendar schedule string
    str representation of this is a valid schedule string
    weekday year-month-day hour:min:sec
    see man systemd.time for more details
    """
    def __init__(
            self,
            week_day:list|str|None=None,
            year:list|str|int|None=None,
            month:list|str|int|None=None,
            day:list|str|int|None=None,
            hour:list|str|int|None=None,
            minute:list|str|int|None=0,
            second:list|str|int|None=0,
            ):
        """
        None becomes * (activates indescriminately)
        A list of value may be passed, or any valid timer string

        :week_day:      full name or abbreviated, case does not matter.
        :year:          4 digit year (YYYY) to activate on, probably
                        always None.
        :month:         month of the year (1-12) to activate on.
        :day:           day of the month to activate on.
        :hour:          hour of the day to activate on (0-23)
        :minute:        minute of the hour to actiavte on (0-59)
        :seceond:       second of the minute to activate on (0-59)
        """

        self._week_day = week_day
        self._year = year
        self._month = month
        self._day = day
        self._hour = hour
        self._minute = minute
        self._second = second

    @property
    def week_day(self):
        return self.parse_week_day(self._week_day)

    @property
    def year(self):
        return self.parse(self._year)

    @property
    def month(self):
        return self.parse(self._month)

    @property
    def day(self):
        return self.parse(self._day)

    @property
    def hour(self):
        return self.parse(self._hour)

    @property
    def minute(self):
        return self.parse(self._minute)

    @property
    def second(self):
        return self.parse(self._second)

    def parse(self, x):
        if isinstance(x, list):
            return ','.join(map(str, x))
        elif isinstance(x, str) or isinstance(x, int):
            return x
        return '*'

    def parse_week_day(self, x):
        if isinstance(x, list):
            return ','.join(x) + ' '
        elif isinstance(x, str):
            return x + ' '
        elif x is None:
            return ''

    def __repr__(self):
        return f'Schedule({self._week_day = }, {self._year = }, {self._month = }, {self._day = }, {self._hour = }, {self._minute = }, {self._second = }'
            
    def __str__(self):
        """Render the schedule string. """
        return f'{self.week_day}{self.year}-{self.month}-{self.day} {self.hour}:{self.minute}:{self.second}'


def minutely(n:int, start:int=0):
    """Define a schedule that schedules at a specified minute interval, optionally specify the initial minute. """
    return Schedule(minute=f'{start}/{n}')

class TimerOnCalendar:
    """
    Render an OnCalendar (realtime) timer 
    """
    template = TEMPLATE_PATH / 'oncalender.timer'

    def __init__(self, description:str, schedule:Schedule, persistent:bool=False):
        """
        :description:   description field of the timer file
        :schedule:      Schedule object
        :persistent:    true/false, default: false
        """

        self.description = description
        self.schedule = schedule
        self.persistent = 'true' if persistent else 'false'

    def set_description(self, description):
        self.description = description 

    def set_persistent(self, persistent:bool):
        self.persistent = 'true' if persistent else 'false'

    def __str__(self):
        """Render the timer string using the template and data members. """

        template_str = open(TimerOnCalendar.template.absolute(), 'r').read()
        template = Template(template_str)
        return template.render(description=self.description, schedule=self.schedule, persistence=self.persistent)


class EnvLoggerScript:
    """
    Class representing the env-logger script and a set of parameters.
    Renders to a valid bash one liner: path/to/script/ valid parameter pack
    To be used in the EnvLoggerUnit to render an entire service file
    """
    script = Path('.').absolute().parent / 'services' / 'env-node' / 'env-logger.py'
    def __init__(self, ip, location, log=LOG_PATH / 'env'):
        self.ip = ip
        self.location = location
        self.log = log

    def __str__(self):
        return f'{EnvLoggerScript.script} {self.ip} {self.location} --log {self.log}'


class EnvLoggerService:
    """
    Render a Env Logger Service file
    """
    template = TEMPLATE_PATH / 'env.service'

    def __init__(self, description:str, script:EnvLoggerScript):
        self.description = description
        self.script = script

    def __str__(self):
        template_str = open(EnvLoggerService.template.absolute(), 'r').read()
        template = Template(template_str)
        return template.render(description=self.description, script=self.script)
