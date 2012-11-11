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

from django.test import TestCase
from contrib.auth.models import User
from shared.models import UserProfile, RealAcct, Budget, Year, Category, RealTxn

class RealAcctTests(TestCase):
    """
    Tests that balance is the aggregate of all virtual accounts
    associated with this RealAcct.
    """
    
    def setUp(self):
        """
        Add some transactions to a RealAcct.
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
        
        category = Category(owner = profile, name = 'test', budget = budget)
        category.save()
        
        self.acct = RealAcct(owner = profile)
        self.acct.save()
        
        self.txn_1 = RealTxn(value = '110.00', category = category, real_acct = self.acct)
        self.txn_1.save()
        self.txn_2 = RealTxn(value = '0.00', category = category, real_acct = self.acct)
        self.txn_2.save()
        self.txn_3 = RealTxn(value = '-10.00', category = category, real_acct = self.acct)
        self.txn_3.save()
        
    def test_balance(self):
        self.assertEqual(self.acct.balance, '100.00')