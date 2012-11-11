#Copyright (C) 2012  Aaron Krebs akrebs@ualberta.ca
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>

from contrib.auth.models import User
from django.test import TestCase
from shared.models import Budget, Year, UserProfile

class BudgetTests(TestCase):
    """
    On the Budget model, only current_account() really needs to be tested.
    """
    
    def test_current_account(self):
        # TODO once I figure out how this should work
        pass
    
    def test_periodlength_inheritance(self):
        """
        See if having PeriodLength as not abstract will call PeriodLength
        methods or subclass methods
        """
        user = User(username = 'testuser', email = 'email@domain.tld')
        user.save()
        profile = UserProfile(user = user)
        profile.save()
        budget = Budget(owner = profile, period_budget_amount = '100.00')
        year = Year()
        year.save()
        budget.period_length = year
        budget.save()
        length = budget.period_length
        assert(length.__unicode__() == 'Year PeriodLength')