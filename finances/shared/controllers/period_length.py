# Copyright (C) 2013  Aaron Krebs akrebs@ualberta.ca
from django.utils import timezone
from django.conf import settings

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

WEEK_PERIOD = 10
MONTH_PERIOD = 20
YEAR_PERIOD = 30

PERIOD_LENGTH_CHOICES = (
    (WEEK_PERIOD, 'Weekly'),
    (MONTH_PERIOD, 'Monthly'),
    (YEAR_PERIOD, 'Yearly')
)


class PeriodLengthFactory(object):
    """
    Factory class for period length controllers.
    
    Each controller will implement the following methods:
    
    current_period_start_date(self):
        Returns the start date of the current period.
    
    current_period_end_date(self):
        Returns the end date of the current period (inclusive).
    
    get_start_date_for_period(self, timezone_date):
        Returns the start date for the period in which timezone_date resides.
    
    get_end_date_for_period(self, timezone_date):
        Returns the end date for the period in which timezone_date resides.
    
    in_current_period(self, timezone_date):
        Returns True if the given timezone_date is in the current period, otherwise returns False
    """
    def __init__(self, length, *args, **kwargs):
        self.length = int(length)
        super(PeriodLengthFactory, self).__init__(*args, **kwargs)
    
    def make_controller(self):
        if self.length == WEEK_PERIOD:
            return WeekPeriodController()
        elif self.length == MONTH_PERIOD:
            return MonthPeriodController()
        elif self.length == YEAR_PERIOD:
            return YearPeriodController()
        else:
            raise NotImplementedError()


class PeriodControllerBase(object):
    """
    Base class for Period Length Controllers.
    
    Provides the interface specification and access to helper attributes/methods.
    """
    
    def __init__(self, *args, **kwargs):
        super(PeriodControllerBase, self).__init__(*args, **kwargs)
        now = timezone.now()
        self.local_now = timezone.localtime(now)
        self.local_today = self.local_now - timezone.timedelta(
            hours=self.local_now.hour,
            minutes=self.local_now.minute,
            seconds=self.local_now.second,
            microseconds=self.local_now.microsecond,
        )
    
    @property
    def current_period_start_date(self):
        """
        Returns the start date of the current period.
        """
        return self.get_start_date_for_period(self.local_today)
    
    @property
    def current_period_end_date(self):
        """
        Returns the end date of the current period (inclusive).
        """
        return self.get_end_date_for_period(self.local_today)
    
    def get_start_date_for_period(self, timezone_date):
        """
        Returns the start date for the period in which timezone_date resides.
        """
        raise NotImplementedError()
    
    def get_end_date_for_period(self, timezone_date):
        """
        Returns the end date for the period in which timezone_date resides.
        """
        raise NotImplementedError()
    
    def in_current_period(self, timezone_date):
        """
        Returns True if the given timezone_date is in the current period, otherwise returns False
        """
        raise NotImplementedError()


class WeekPeriodController(PeriodControllerBase):
    def get_start_date_for_period(self, timezone_date):
        """
        Returns the start date for the period in which timezone_date resides.
        """
        days_offset = timezone_date.weekday()
        days_offset = days_offset + 1 if days_offset < 6 else 0
        days_offset += settings.FIRST_DAY_OF_WEEK
        return timezone.localtime(
            timezone_date\
            - timezone.timedelta(days=days_offset)\
            - timezone.timedelta(
                    hours=timezone_date.hour,
                    minutes=timezone_date.minute,
                    seconds=timezone_date.second,
                    microseconds=timezone_date.microsecond,
            )
        )
    
    def get_end_date_for_period(self, timezone_date):
        """
        Returns the end date for the period in which timezone_date resides.
        """
        return self.get_start_date_for_period(timezone_date)\
            + timezone.timedelta(days=7)\
            - timezone.timedelta(microseconds=1)
    
    def in_current_period(self, timezone_date):
        """
        Returns True if the given timezone_date is in the current period, otherwise returns False
        """
        if timezone_date >= self.get_start_date_for_period(self.local_today)\
            and timezone_date <= self.get_end_date_for_period(self.local_today):
                return True
        return False


class MonthPeriodController(PeriodControllerBase):
    def get_start_date_for_period(self, timezone_date):
        """
        Returns the start date for the period in which timezone_date resides.
        """
        raise NotImplementedError()
    
    def get_end_date_for_period(self, timezone_date):
        """
        Returns the end date for the period in which timezone_date resides.
        """
        raise NotImplementedError()
    
    def in_current_period(self, timezone_date):
        """
        Returns True if the given timezone_date is in the current period, otherwise returns False
        """
        raise NotImplementedError()


class YearPeriodController(PeriodControllerBase):
    def get_start_date_for_period(self, timezone_date):
        """
        Returns the start date for the period in which timezone_date resides.
        """
        raise NotImplementedError()
    
    def get_end_date_for_period(self, timezone_date):
        """
        Returns the end date for the period in which timezone_date resides.
        """
        raise NotImplementedError()
    
    def in_current_period(self, timezone_date):
        """
        Returns True if the given timezone_date is in the current period, otherwise returns False
        """
        raise NotImplementedError()
