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

from django.test import TestCase
from django.contrib.auth.models import User
from shared.models import Budget, Year, Category, RealAcct,\
    VirtualAcct, RealTxn, VirtualTxn


class VirtualAcctTests(TestCase):
    """
    Tests balance of Virtual Acct objects.
    """
    
    def setUp(self):
        """
        Add some transactions to a VirtualAcct.
        """
        user = User.objects.create(username = 'testuser', email = 'email@domain.tld')
        budget = Budget(owner = user, period_budget_amount = '100.00')
        year = Year.objects.create()
        budget.period_length = year
        budget.save()
        
        category = Category(owner = user, name = 'test', budget = budget)
        category.save()
        
        self.acct = RealAcct.objects.create(owner = user)
        self.vacct = VirtualAcct.objects.create(owner = user, real_acct = self.acct, parent_budget = budget)
        
        self.txn_1 = RealTxn(value = '110.00', category = category, real_acct = self.acct)
        self.txn_1.save()
        self.vtxn_1 = VirtualTxn(value = '90.00', real_txn = self.txn_1, virtual_acct = self.vacct)
        self.vtxn_1.save()
        self.vtxn_2 = VirtualTxn(value = '20.00', real_txn = self.txn_1, virtual_acct = self.vacct)
        self.vtxn_2.save()
        
    def test_balance(self):
        self.assertEqual(self.vacct.balance, '110.00')