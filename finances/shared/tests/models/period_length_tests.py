# Copyright (C) 2012  Aaron Krebs akrebs@ualberta.ca
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from datetime import datetime
from calendar import monthrange
from django.test import TestCase
from shared.models import PeriodLength, Month, Year

class PeriodLengthTests(TestCase):
    """
    Test for all PeriodLength subclasses.
    """
    
    def setUp(self):
        self.period_length = PeriodLength()
        self.month = Month()
        self.year = Year()
        
        now = datetime.now()
        self.now = now
        
        self.month_beginning = datetime(now.year, now.month, 1)
        self.month_end = datetime(now.year, now.month, monthrange(now.year, now.month)[1])
        # account for Jan and Dec in month testing
        if now.month == 12:
            self.next_month = datetime(now.year, 1, 1)
        else:
            self.next_month = datetime(now.year, now.month + 1, 1)
        if now.month == 1:
            self.previous_month = datetime(now.year - 1, 12, 1)
        else:
            self.previous_month = datetime(now.year, now.month - 1, 1)
        
        self.year_beginning = datetime(now.year, 1, 1)
        self.year_end = datetime(now.year, 12, 31)
        self.next_year = datetime(now.year + 1, now.month, 1)
        self.previous_year = datetime(now.year - 1, now.month, 1)
    
    def test_period_length(self):
        now = datetime.now()
        try:
            self.period_length.current_period_start_date()
            assert(False)
        except NotImplementedError:
            assert(True)
        
        try:
            self.period_length.current_period_end_date()
            assert(False)
        except NotImplementedError:
            assert(True)
        
        try:
            self.period_length.in_current_period(now)
            assert(False)
        except NotImplementedError:
            assert(True)
    
    def test_month(self):
        assert(self.month.current_period_start_date == self.month_beginning)
        assert(self.month.current_period_end_date == self.month_end)
        
        assert(self.month.in_current_period(self.now))
        assert(self.month.in_current_period(self.month_end))
        assert(self.month.in_current_period(self.month_beginning))
        assert(self.month.in_current_period(self.next_month) == False)
        assert(self.month.in_current_period(self.previous_month) == False)
    
    def test_year(self):
        assert(self.year.current_period_start_date == self.year_beginning)
        assert(self.year.current_period_end_date == self.year_end)
        
        assert(self.year.in_current_period(self.now))
        assert(self.year.in_current_period(self.year_end))
        assert(self.year.in_current_period(self.year_beginning))
        assert(self.year.in_current_period(self.next_year) == False)
        assert(self.year.in_current_period(self.previous_year) == False)