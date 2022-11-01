"""
Module for creating systemd units (services and timers) using templates (jinja2)
"""
from jinja2 import Template
from pathlib import Path


TEMPLATE_PATH = Path('templates')

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
            minute:list|str|int|None=None,
            second:list|str|int|None=None,
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

        self.week_day = self.parse_week_day(week_day)
        self.year = self.parse(year)
        self.month = self.parse(month)
        self.day = self.parse(day)
        self.hour = self.parse(hour)
        self.minute = self.parse(minute)
        self.second = self.parse(second)

    def set_week_day(self, week_day):
        self.week_day = self.parse_week_day(week_day)

    def set_year(self, year):
        self.year = self.parse(year)

    def set_month(self, month):
        self.month = self.parse(month)

    def set_day(self, day):
        self.day = self.parse(day)

    def set_hour(self, hour):
        self.hour = self.parse(hour)

    def set_minute(self, minute):
        self.minute = self.parse(minute)

    def set_second(self, second):
        self.second = self.parse(second)

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

    def __str__(self):
        """Render the schedule string. """
        return f'{self.week_day}{self.year}-{self.month}-{self.day} {self.hour}:{self.minute}:{self.second}'
            
class TimerOnCalendar:
    """
    A realtime (OnCalendar) timer
    Class represents a realtime (OnCalendar) timer.

    """
    template = TEMPLATE_PATH / 'oncalender.timer'

    def __init__(self, description:str, schedule:Schedule, persistent:str='false'):
        """
        :description:   description field of the timer file
        :schedule:      Schedule object
        :persistent:    true/false, default: false
        """

        self.description = description
        self.schedule = schedule
        self.persistent = persistent

    def set_description(self, description):
        self.description = description 

    def __str__(self):
        """Render the timer string using the template and data members. """

        template_str = open(TimerOnCalendar.template.absolute(), 'r').read()
        template = Template(template_str)
        return template.render(description=self.description, schedule=self.schedule, persistence=self.persistent)


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
