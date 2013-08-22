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

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from shared.controllers import PeriodLengthFactory, MONTH_PERIOD

CHARFIELD_MAX_LENGTH = 200


class OwnedModel(models.Model):
    """
    Abstract class to move owner attribute into a common parent class.
    
    Owner should be set at instantiation, and not be changed afterward.
    """
    
    owner = models.ForeignKey(User)
    
    class Meta:
        abstract = True
    
    def is_allowed(self, request):
        """
        Returns True if the given request can be processed.
        """
        raise NotImplementedError()
    
    def assert_is_allowed(self, request):
        """
        Raises a PermissionDenied exception if the requesting user is not
        permitted to perform the action.
        """
        raise NotImplementedError()


class NamedModel(models.Model):
    """
    Abstract class to move name attribute into a common parent class.
    """
    
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    
    class Meta:
        abstract = True


class Budget(NamedModel, OwnedModel):
    """
    A Budget represents an overall behaviour of a budget. It contains
    information on a budget's period, and the amount budgeted per period.
    
    Category objects are associated with a Budget so that RealTxn objects
    with said Category are counted against the budget.
    """
    
    period_budget_amount = models.DecimalField(max_digits=15, decimal_places=2)
    period_length = models.IntegerField(default=MONTH_PERIOD)
    
    def __init__(self, *args, **kwargs):
        super(Budget, self).__init__(*args, **kwargs)
        self.period_length_controller = PeriodLengthFactory(self.period_length).make_controller()
    
    def __unicode__(self):
        return self.name
        
    def account_for_date(self, timezone_date):
        """
        Returns the VirtualAccount against which transactions on the given date
        should be posted.
        """
        raise NotImplementedError()
    
    @property
    def current_account(self):
        """
        Returns the VirtualAcct that should be used for this budget in the
        current period. Uses the @property decorator.
        """
        return self.account_for_date(timezone.now)
    
    @property
    def current_period_start_date(self):
        """
        Returns the start date of the current period.
        """
        return self.period_length_controller.current_period_start_date
    
    @property
    def current_period_end_date(self):
        """
        Returns the end date of the current period (inclusive).
        """
        return self.period_length_controller.current_period_end_date
    
    def in_current_period(self, timezone_date):
        """
        Returns True if the given timezone_date is in the current period, otherwise returns False
        """
        return self.period_length_controller.in_current_period(timezone_date)


class Category(NamedModel, OwnedModel):
    """
    The Category class defines types of Transactions. Categories can be
    associated with one Budget object such that Transactions with said Category
    count against that Budget.
    """
    
    budget = models.ForeignKey(Budget)
    
    def __unicode__(self):
        return self.name


class RealAcct(OwnedModel, NamedModel):
    """
    Represents a real-world bank account. RealTxn class objects can be listed
    against such an account. Furthermore, VirtualAcct class objects can be
    associated with this account so that they are included in the account balance
    """
    
    def __unicode__(self):
        return self.name
    
    @property
    def balance(self):
        """
        Returns the balance of this account. The account balance is an
        aggregate of all the VirtualAccts associated with this RealAcct
        """
        raise NotImplementedError()


class VirtualAcct(OwnedModel, NamedModel):
    """
    Represents a sub-division of a real account (RealAcct). Is associated with
    a RealAcct class object to represent a portion of that account's aggregate balance.
    """
    
    parent_budget = models.ForeignKey(Budget)
    real_acct = models.ForeignKey(RealAcct)
    
    def __unicode__(self):
        return self.name
    
    @property
    def balance(self):
        """
        Calculates the balance of this account from the VirtualTxn objects
        associated with it. Uses  the @property decorator.
        """
        raise NotImplementedError()


class RealTxn(OwnedModel):
    """
    This class represents a transaction on an a real account.
    
    Credit values (money into account) are given as positive; Debit values
    (money removed from account) as negative.
    """
    
    real_account = models.ForeignKey(RealAcct)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.ForeignKey(Category)
    
    def __unicode__(self):
        return self.name


class VirtualTxn(OwnedModel):
    """
    This class represents a transaction on an a virtual account.
    
    Credit values (money into account) are given as positive; Debit values
    (money removed from account) as negative.
    """
    
    virtual_acct = models.ForeignKey(VirtualAcct)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    real_txn = models.ForeignKey(RealTxn)
    
    def __unicode__(self):
        return self.name
