# Copyright (C) 2013  Aaron Krebs akrebs@ualberta.ca

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


class PeriodLengthFactory(object):
    """
    Factory class for period length controllers.
    
    Each controller will implement the following methods:
    
    current_period_start_date(self):
        Returns the start date of the current period.
    
    current_period_end_date(self):
        Returns the end date of the current period (inclusive).
    
    in_current_period(self, timezone_date):
        Returns True if the given timezone_date is in the current period, otherwise returns False
    """
    def __init__(self, length, *args, **kwargs):
        self.length = length
        super(PeriodLengthFactory, self).__init__(*args, **kwargs)
    
    def make_controller(self):
        if self.length == WEEK_PERIOD:
            raise NotImplementedError()
        elif self.length == MONTH_PERIOD:
            return MonthPeriodController()
        elif self.length == YEAR_PERIOD:
            raise NotImplementedError()
        else:
            raise NotImplementedError()


class MonthPeriodController(object):
    @property
    def current_period_start_date(self):
        raise NotImplementedError()
    
    @property
    def current_period_end_date(self):
        raise NotImplementedError()
    
    def in_current_period(self, timezone_date):
        raise NotImplementedError()
