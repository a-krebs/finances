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

from calendar import monthrange
from django.test import TestCase
from shared.controllers.period_length import PeriodLengthFactory, WEEK_PERIOD,\
    MONTH_PERIOD, WeekPeriodController, YEAR_PERIOD, MonthPeriodController,\
    YearPeriodController
import random
from django.utils import timezone
from django.conf import settings


class PeriodLengthTests(TestCase):
    """
    Test for all PeriodLength subclasses.
    """
    
    def setUp(self):
        # factories for different period lengths
        self.week = PeriodLengthFactory(WEEK_PERIOD)
        self.month = PeriodLengthFactory(MONTH_PERIOD)
        self.year = PeriodLengthFactory(YEAR_PERIOD)
        self.week_controller = self.week.make_controller()
        self.month_controller = self.month.make_controller()
        self.year_controller = self.year.make_controller()
        
        # helper variables for testing
        now = timezone.localtime(timezone.now())
        self.now = now
        self.today_start = now - timezone.timedelta(
            hours=now.hour,
            minutes=now.minute,
            seconds=now.second,
            microseconds=now.microsecond,
        )
        self.today_end = self.today_start\
            + timezone.timedelta(days=1)\
            - timezone.timedelta(microseconds=1)
        
        days_offset = self.today_start.weekday()
        days_offset = days_offset + 1 if days_offset < 6 else 0
        days_offset += settings.FIRST_DAY_OF_WEEK
        self.week_beginning = self.today_start - timezone.timedelta(days=days_offset)
        self.week_end = self.week_beginning\
            + timezone.timedelta(weeks=1)\
            - timezone.timedelta(microseconds=1)
        self.next_week = self.week_beginning + timezone.timedelta(weeks=1)
        self.previous_week = self.week_beginning - timezone.timedelta(weeks=1)
        self.month_beginning = timezone.datetime(self.today_start.year, self.today_start.month, 1)
        self.month_beginning = timezone.make_aware(self.month_beginning, timezone.get_current_timezone())
        self.month_end = timezone.datetime(self.today_start.year, self.today_start.month, monthrange(self.today_start.year, self.today_start.month)[1])
        self.month_end = timezone.make_aware(self.month_end, timezone.get_current_timezone())
        if self.today_start.month == 12:    # account for Jan and Dec in month testing
            self.next_month = timezone.datetime(self.today_start.year, 1, 1)
        else:
            self.next_month = timezone.datetime(self.today_start.year, self.today_start.month + 1, 1)
        self.next_month = timezone.make_aware(self.next_month, timezone.get_current_timezone())
        if self.today_start.month == 1:
            self.previous_month = timezone.datetime(self.today_start.year - 1, 12, 1)
        else:
            self.previous_month = timezone.datetime(self.today_start.year, self.today_start.month - 1, 1)
        self.previous_month = timezone.make_aware(self.previous_month, timezone.get_current_timezone())
        
        self.year_beginning = timezone.make_aware(
            timezone.datetime(self.today_start.year, 1, 1),
            timezone.get_current_timezone()
        )
        self.year_end = timezone.make_aware(
            timezone.datetime(self.today_start.year, 12, 31),
           timezone.get_current_timezone()
        )
        self.next_year = timezone.make_aware(
            timezone.datetime(self.today_start.year + 1, self.today_start.month, 1),
           timezone.get_current_timezone()
        )
        self.previous_year = timezone.make_aware(
            timezone.datetime(self.today_start.year - 1, self.today_start.month, 1),
           timezone.get_current_timezone()
        )
    
    def test_make_controller(self):
        """
        Check that factory pattern works as intended.
        
        Run make_controller() a few hundred times to be sure that the
        correct type is returned and there isn't a strange case after a few calls
        to the factory.
        """
        instances = set()
        A = lambda returned_type, check_type: self.assertTrue(isinstance(returned_type, check_type))
        for _ in xrange(0, int(1000 * random.random())):
            week = self.week.make_controller()
            month = self.month.make_controller()
            year = self.year.make_controller()
            self.assertTrue(week not in instances)
            self.assertTrue(month not in instances)
            self.assertTrue(year not in instances)
            instances.add(week)
            instances.add(month)
            instances.add(year)
            A(week, WeekPeriodController)
            A(month, MonthPeriodController)
            A(year, YearPeriodController)
        
    def test_current_period_start_date(self):
        """
        Test that the period start dates are as expected.
        """
        self.assertTrue(self.week_controller.current_period_start_date, self.week_beginning)
        self.assertTrue(self.month_controller.current_period_start_date, self.month_beginning)
        self.assertTrue(self.year_controller.current_period_start_date, self.year_beginning)
    
    def test_week_boundary_conditions(self):
        """
        Test boundary conditions of week controller.
        """
        self.assertEqual(self.week_controller.current_period_start_date, self.week_beginning)
        self.assertEqual(self.week_controller.current_period_end_date, self.week_end)
        
        self.assertTrue(self.week_controller.in_current_period(self.now))
        self.assertTrue(self.week_controller.in_current_period(self.week_end))
        self.assertTrue(self.week_controller.in_current_period(self.week_beginning))
        self.assertFalse(self.week_controller.in_current_period(self.next_week))
        self.assertFalse(self.week_controller.in_current_period(self.previous_week))
    
    def test_month_boundary_conditions(self):
        """
        Test boundary conditions of month controller.
        """
        self.assertEqual(self.month_controller.current_period_start_date, self.month_beginning)
        self.assertEqual(self.month_controller.current_period_end_date, self.month_end)
        
        self.assertTrue(self.month_controller.in_current_period(self.now))
        self.assertTrue(self.month_controller.in_current_period(self.month_end))
        self.assertTrue(self.month_controller.in_current_period(self.month_beginning))
        self.assertFalse(self.month_controller.in_current_period(self.next_month))
        self.assertFalse(self.month_controller.in_current_period(self.previous_month))
    
    def test_year_boundary_conditions(self):
        """
        Test boundary conditions of year controller.
        """
        self.assertEqual(self.year_controller.current_period_start_date, self.year_beginning)
        self.assertEqual(self.year_controller.current_period_end_date, self.year_end)
        
        self.assertTrue(self.year_controller.in_current_period(self.now))
        self.assertTrue(self.year_controller.in_current_period(self.year_end))
        self.assertTrue(self.year_controller.in_current_period(self.year_beginning))
        self.assertFalse(self.year_controller.in_current_period(self.next_year))
        self.assertFalse(self.year_controller.in_current_period(self.previous_year))

    def test_week_start_date_for_period(self):
        T = lambda input_date, expected_return:\
            self.assertEqual(
                self.week_controller.get_start_date_for_period(input_date),
                expected_return
            )
        # some arbitrary dates
        mar_12_1998 = timezone.datetime(day=12, month=3, year=1998)
        mar_12_1998 = timezone.make_aware(mar_12_1998, timezone.get_current_timezone())
        mar_8_1998 = timezone.datetime(day=8, month=3, year=1998)
        mar_8_1998 = timezone.make_aware(mar_8_1998, timezone.get_current_timezone())
        T(mar_12_1998, mar_8_1998)
