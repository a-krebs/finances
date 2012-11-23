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

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import FieldError

CHARFIELD_MAX_LENGTH = 200

class OwnedModel(models.Model):
    """
    Abstract class to move owner attribute into a common parent class.
    
    Owner should be set at instantiation, and not be changed afterward.
    """
    
    _owner = models.ForeignKey(User)
    
    class Meta:
        abstract = True
    
    def __unicode__(self) :
        # this is an abstract model, so this method should be overridden later
        raise NotImplementedError()
    
    @property
    def owner(self):
        """
        Returns the User object of this Account's owner.
        """
        return self._owner 
    
    @owner.setter
    def owner(self, owner):
        """
        Raises a FieldError if this object's owner is already set.
        """
        # try to fetch _owner, if it doesn't exist we can set it
        try:
            if self._owner:
                raise FieldError('owner is already set and cannot be set again')
        except User.DoesNotExist:
            self._owner = owner
    
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
    
    _name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        # this is an abstract model, so this method should be overridden later
        raise NotImplementedError()
    
    @property
    def name(self):
        """
        Returns the display name of this Account.
        """
        return self._name
    
    @name.setter
    def name(self, name):
        """
        Sets the display name of this Account.
        """
        self._name = name

class PeriodLength(NamedModel):
    """
    Abstract class that determines a period length. Since months are not
    always the same number of days, and years can be leap years, etc., this
    class exists to help in determining the length of a period.
    """
    
    def __unicode__(self):
        # This is an abstract class, so this method should be implemented in subclasses
        raise NotImplementedError()
    
    @property
    def current_period_start_date(self):
        """
        Returns the start date of the current period. Uses the @property decorator.
        
        This is an abstract method. It always throws a NotImplementedError
        as subclasses should implement the method and then Duck Typing can
        be used.
        """
        
        raise NotImplementedError()
    
    @property
    def current_period_end_date(self):
        """
        Returns the end date of the current period (inclusive). Uses the @property decorator.
        
        This is an abstract method. It always throws a NotImplementedError
        as subclasses should implement the method and then Duck Typing can
        be used.
        """
        raise NotImplementedError()
    
    def in_current_period(self, timezone_date):
        """
        Returns True if the given timezone_date is in the current period, otherwise returns False
        
        This is an abstract method. It always throws a NotImplementedError
        as subclasses should implement the method and then Duck Typing can
        be used.
        """
        raise NotImplementedError()

class Month(PeriodLength):
    """
    Represents a one month period length (eg, a budget would have this period
    length if the money for that budget is allocated monthly).
    """
    
    def __unicode__(self):
        return "Month PeriodLength"
    
    @property
    def current_period_start_date(self):
        """
        Returns the start date of the current period.
        Uses the @property decorator.
        """
        raise NotImplementedError()
    
    @property
    def current_period_end_date(self):
        """
        Returns the end date of the current period (inclusive).
        Uses the @property decorator.
        """
        raise NotImplementedError()
    
    def in_current_period(self, timezone_date):
        """
        Returns True if the given timezone_date is in the current period, otherwise returns False
        """
        raise NotImplementedError()

class Year(PeriodLength):
    """
    Represents a one year period length (eg, a budget would have this period
    length if the money for that budget is allocated yearly).
    """
    
    def __unicode__(self):
        return "Year PeriodLength"
    
    @property
    def current_period_start_date(self):
        """
        Returns the start date of the current period.
        Uses the @property decorator.
        """
        raise NotImplementedError()
    
    @property
    def current_period_end_date (self) :
        """
        Returns the end date of the current period (inclusive).
        Uses the @property decorator.
        """
        raise NotImplementedError()
    
    def in_current_period (self, timezone_date) :
        """
        Returns True if the given timezone_date is in the current period, otherwise returns False
        """ 
        raise NotImplementedError()

class Budget(NamedModel, OwnedModel):
    """
    A Budget represents an overall behaviour of a budget. It contains
    information on a budget's period, and the amount budgeted per period.
    
    Category objects are associated with a Budget so that RealTxn objects
    with said Category are counted against the budget.
    """
    
    _period_budget_amount = models.DecimalField(max_digits = 15, decimal_places = 2)
    _period_length = models.ForeignKey(PeriodLength)
    
    def __unicode__(self):
        return self.owner.user.username + "'s Budget: " + self.name
        
    def current_account(self):
        """
        Returns the VirtualAcct that should be used for this budget in the
        current period. Uses the @property decorator.
        """
        raise NotImplementedError()
    
    @property
    def period_length(self):
        """
        Returns the PeriodLength object that determines the period length for this budget.
        """
        return self._period_length
    
    @period_length.setter
    def period_length(self, length):
        """
        Given a PeriodLength object, sets the length of the period for this budget.
        """
        self._period_length = length
    
    @property
    def period_budget_amount(self):
        """
        Returns the float value of the amount that is to be budgeted for each
        budget period. Uses the @property decorator.
        """
        return self._period_budget_amount
    
    @period_budget_amount.setter
    def period_budget_amount(self, float_amount):
        """
        Sets the float value of the amount that is to be budgeted for each
        budget period. Uses the @property decorator.
        """
        self._period_budget_amount = float_amount

class Category(NamedModel, OwnedModel):
    """
    The Category class defines types of Transactions. Categories can be
    associated with one Budget object such that Transactions with said Category
    count against that Budget.
    """
    
    _budget = models.ForeignKey(Budget)
    
    def __unicode__ (self) :
        return self.owner.user.username + "'s Category: " + self.name
    
    @property
    def budget (self) :
        """
        Returns the Budget object that this Category is under.
        """
        return self._budget
    
    @budget.setter
    def budget (self, budget) :
        """
        Sets the Budget object that this Category is under.
        """
        self._budget = budget

class RealAcct(OwnedModel, NamedModel):
    """
    Represents a real-world bank account. RealTxn class objects can be listed
    against such an account. Furthermore, VirtualAcct class objects can be
    associated with this account so that they are included in the account balance
    """
    
    def __unicode__(self):
        return self.owner.user.username + "'s RealAcct " + self.name
    
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
    
    _parent_budget = models.ForeignKey(Budget)
    _real_acct = models.ForeignKey(RealAcct)
    
    def __unicode__(self):
        return self.owner.user.username + "'s VirtualAcct " + self.name
    
    @property
    def parent_budget(self):
        """
        Returns the budget object with which this virtual account is associated.
        Uses the @property decorator.
        """
        return self._parent_budget
    
    @parent_budget.setter
    def parent_budget(self, budget):
        """
        Raises a FieldError if the object's parent_budget is already set.
        """
        # try to fetch _parent_budget, if it doesn't exist we can set it
        try:
            if self._parent_budget:
                raise FieldError('_parent_budget is already set and cannot be set again')
        except RealAcct.DoesNotExist:
            self._parent_budget = budget
        
    
    @parent_budget.setter
    def parent_budget(self, budget):
        raise NotImplementedError()
    
    @property
    def real_acct(self):
        """
        Returns the RealAcct object this object is associated with.
        """
        raise NotImplementedError()
    
    @real_acct.setter
    def real_acct(self, acct):
        """
        Raises a FieldError if this object's real_acct is already set.
        """
        # try to fetch _real_acct, if it doesn't exist we can set it
        try:
            if self._real_acct:
                raise FieldError('_real_acct is already set and cannot be set again')
        except RealAcct.DoesNotExist:
            self._real_acct = acct
            
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
    
    _real_account = models.ForeignKey(RealAcct)
    _value = models.DecimalField(max_digits = 15, decimal_places = 2)
    _category = models.ForeignKey(Category)
    
    def __unicode__(self):
        return self.owner.username.name + "'s RealTxn " + self.name
    
    @property
    def value(self):
        """
        Returns the value of the transaction.
        
        Credit values (money into account) are given as positive; Debit
        values (money removed from account) as negative.
        
        Uses the @property decorator.
        """
        raise NotImplementedError()
    
    @value.setter
    def value(self, amount):
        """
        Sets the value of the transaction.
        
        Credit values (money into account) are given as positive; Debit
        values (money removed from account) as negative.
        
        Uses the @property decorator.
        """
        raise NotImplementedError()
    
    @property
    def category(self):
        """
        Returns the Category object associated with the Transaction.
        
        Uses the @property decorator.
        """
        raise NotImplementedError()
    
    @category.setter
    def category(self, category):
        """
        Sets the Category this transaction is associated with.
        
        Uses the @property decorator.
        """
        raise NotImplementedError()
    
    @property
    def real_acct(self):
        """
        Returns the Account object this transaction is counted against.
        
        Uses the @property decorator.
        """
        raise NotImplementedError()
    
    @real_acct.setter
    def real_acct(self, acct):
        """
        Raises a FieldError if this object's real_acct is already set.
        """
        # try to fetch _real_acct, if it doesn't exist we can set it
        try:
            if self._real_acct:
                raise FieldError('_real_acct is already set and cannot be set again')
        except RealAcct.DoesNotExist:
            self._real_acct = acct

class VirtualTxn(OwnedModel):
    """
    This class represents a transaction on an a virtual account.
    
    Credit values (money into account) are given as positive; Debit values
    (money removed from account) as negative.
    """
    
    _virtual_acct = models.ForeignKey(VirtualAcct)
    _value = models.DecimalField(max_digits = 15, decimal_places = 2)
    _real_txn = models.ForeignKey(RealTxn)
    
    def __unicode__(self):
        return self.owner.user.username + "'s VirtualTxn " + self.name
    
    @property
    def value(self):
        """
        Returns the value of the transaction.
        
        Credit values (money into account) are given as positive; Debit
        values (money removed from account) as negative.
        
        Uses the @property decorator.
        """
        raise NotImplementedError()
    
    @value.setter
    def value(self, amount):
        """
        Sets the value of the transaction.
        
        Credit values (money into account) are given as positive; Debit
        values (money removed from account) as negative.
        
        Uses the @property decorator.
        """
        raise NotImplementedError()
    
    @property
    def virtual_acct(self):
        """
        Returns the VirtualAcct object this transaction is counted against.
        
        Uses the @property decorator.
        """
        raise NotImplementedError()
    
    @virtual_acct.setter
    def virtual_acct(self, acct):
        """
        Raises a FieldError if this object's virtual_acct is already set.
        """
        # try to fetch _virtual_acct, if it doesn't exist we can set it
        try:
            if self._virtual_acct:
                raise FieldError('_virtual_acct is already set and cannot be set again')
        except VirtualAcct.DoesNotExist:
            self._virtual_acct = acct
    
    @property
    def real_txn(self):
        """
        Returns the RealTxn object associated with this transaction. Uses
        the @property decorator.
        """
        raise NotImplementedError()
    
    @real_txn.setter
    def real_txn(self, txn):
        """
        Raises a FieldError if this object's real_txn is already set.
        """
        # try to fetch _real_txn, if it doesn't exist we can set it
        try:
            if self._real_txn:
                raise FieldError('_real_txn is already set and cannot be set again')
        except VirtualAcct.DoesNotExist:
            self._real_txn = txn