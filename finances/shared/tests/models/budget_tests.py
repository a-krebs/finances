# Copyright (C) 2012  Aaron Krebs akrebs@ualberta.ca

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

from django.contrib.auth.models import User
from django.test import TestCase
from shared.models import Budget


class BudgetTests(TestCase):
    """
    Tests for parts of Budget that are not related to period length (as
    those have their own controllers and thus their own tests).
    """
    
    def setUp(self):
        user = User.objects.create(username='testuser', email='email@domain.tld')
        self.budget = Budget.objects.create(period_budget_amount=10.00,owner=user)
        
    
    def test_current_account(self):
        # TODO once I figure out how this should work
        pass
    
    def test_account_for_date(self):
        pass
