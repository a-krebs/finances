from django.db import models
from django.contrib.auth.models import User

CHARFIELD_MAX_LENGTH = 200

class UserProfile(models.Model):
    """
    This class is set up as the Django user profile model;
    see the documentation on Authentication for more information:
    django-docs-1.4-en/topics/auth.html#storing-additional-information-about-users
    
    This class exists to associate a user with their accounts and
    budget policies within the app, and store additional information to Django's User
    """
    
    user = models.OneToOneField(User)
    
    def __unicode__(self):
        NotImplementedError
        
    def get_user(self):
        """
        returns the Django User object associated with this profile
        """
        NotImplementedError
        
    def get_account_set(self):
        """
        returns the set of accounts associated with this user profile
        """
        NotImplementedError
        
    def get_budget_set(self):
        """
        returns the set of Budget objects assocaited with this user profile
        """
        NotImplementedError
        
class OwnedModel(models.Model):
    """
    Abstract class to move owner attribute into a common parent class.
    
    Owner should be set at instantiation, and not be changed afterward.
    """
    
    owner = models.ForeignKey(UserProfile)
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        NotImplementedError
        
    def get_owner(self):
        """
        returns the UserProfile object of this Account's owner
        """
        NotImplementedError
        
    def is_allowed(self, request):
        """
        returns True if the given request can be processed
        """
        NotImplementedError
        
    def assert_is_allowed(self, request):
        """
        raises a PermissionDenied exception if the requesting user is not
        permitted to perform the action
        """
        NotImplementedError
        
class NamedModel(OwnedModel):
    """
    Abstract class to move name attribute into a common parent class.
    """
    
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        NotImplementedError
        
    def get_name(self):
        """
        returns the display name of this Account
        """
        NotImplementedError
        
    def set_name(self, name):
        """
        sets the display name of this Account
        """
        NotImplementedError
        
class EndPolicy(NamedModel):
    """
    Abstract class for encapsulating Budget behaviour. A subclass of EndPolicy
    will implement specifically what actions are taken with a BudgetPeriod's
    Earmark objects when the BudgetPeriod ends.
    
    For example, a subclass of EndPolicy might implement that at the end of a
    BudgetPeriod all Earmark surpluses are carried over to the next BudgetPeriod
    object, and that any shortfalls are also carried to the next BudgetPeriod
    """
    
    description = models.TextField()
    
    
    def __unicode__(self):
        NotImplementedError
        
    def get_description(self):
        """
        returns the user-facing description of the behaviour of this EndPolicy
        """
        NotImplementedError
        
    def calculate_budget_period_balance(self, budget_period):
        """
        returns the float value of the budget's remaining balance (positive or
        negative depending on surplus or shortfall)
        """
        NotImplementedError
        
    def apply_policy(self, new_budget_period):
        """
        performs the actions of the end policy, altering the given new BudgetPolicy
        object such that it can be used as the next current BudgetPeriod
        """
        NotImplementedError
        
class Budget(NamedModel):
    """
    A Budget represents an overall behaviour of a budget. It contains
    information on a budget's period, the behaviour with leftover surpluses or
    shortfalls at the end of the budget period, and the amount budgeted per period.
    
    Category objects are associated with a Budget so that Transaction objects
    with said Category are counted against the budget.
    
    For example: a Budget may define a budget that calls for $200 per
    budget period, with a budget period being one month, with surpluses
    rolling over to the next month's budget balance and shortfalls coming out
    of the next month's balance.
    """
    
    end_policy = models.OneToOneField(EndPolicy)
    period_budget_amount = models.FloatField()
    
    def __unicode__(self):
        NotImplementedError
        
    def get_budget_period_set(self, after_date, before_date):
        """
        returns the set of BudgetPeriod objects associated with this Budget.
        """
        NotImplementedError
        
    def get_current_budget_period(self):
        """
        returns the current BudgetPeriod object for this budget
        """
        NotImplementedError
        
    def set_current_budget_period(self, budget_period):
        """
        sets the current BudgetPeriod for this budget
        """
        NotImplementedError
        
    def get_end_policy(self):
        """
        returns the EndPolicy object of this Budget
        """
        # remember on implementation that the subclass of EndPolicy object must be
        # returned for Duck Typing. The EndPolicy object cannot be an abstract class
        # but we'll access it through EndPolicy, get the subclass, and then return that. 
        NotImplementedError
        
    def get_period_length(self):
        """
        returns the PeriodLength object that determines the period length for this budget
        """
        NotImplementedError
        
    def get_period_budget_amount(self):
        """
        returns the float value of the amount that is to be budgeted for each budget period
        """
        NotImplementedError
        
    def set_period_budget_amount(self, float_amount):
        """
        sets the float value of the amount that is to be budgeted for each budget period
        """
        NotImplementedError
        
    def process_budget_period(self, new_budget_period):
        """
        checks if the current budget period is still supposed to be active.
        If yes, then nothing is done and the function returns False. If the
        current Budget Period should be over, it is closed out and a new BudgetPeriod
        object is created and made current.
        """
        NotImplementedError
        
class Category(NamedModel):
    """
    The Category class defines types of Transactions. Categories can be
    associated with one Budget object such that Transactions with said Category
    count against that Budget.
    """
    
    budget = models.ForeignKey(Budget)
    
    def __unicode__(self):
        NotImplementedError
        
    def get_budget(self):
        """
        returns the Budget object that this Category is under.
        """
        NotImplementedError
        
    def set_budget(self, budget):
        """
        sets the Budget object that this Category is under.
        """ 
        NotImplementedError
        
class Account(NamedModel):
    """
    An Account object mirrors a bank account. It has a balance which is determined
    by the Transactions (debits, credits, transfers, etc) made against that Account.
    """
    
    def __unicode__(self):
        NotImplementedError
        
    def get_transaction_set(self):
        """
        returns the set of all Transaction objects associated with this Account
        """
        NotImplementedError
        
    def get_balance(self):
        """
        returns a Float representing the calculated balance of this Account
        """
        NotImplementedError
        
    def create_earmark(self, budget_period, earmark, amount):
        """
        populates the given earmark object with the amount given. 
        Returns False if the balance is not available in the account to be earmarked
        """ 
        NotImplementedError
        
    def get_free_balance(self):
        """
        returns the float value of the money avaibale in the account that has not been earmarked
        """
        NotImplementedError
        
class Transaction(NamedModel):
    """
    This class represents a transaction on an account.
    
    Credit values (money into account) are given as positive; Debit values
    (money removed from account) as negative.
    """
    
    account = models.ForeignKey(Account)
    value = models.FloatField()
    category = models.ForeignKey(Category)
    
    def __unicode__(self):
        NotImplementedError
        
    def get_value(self):
        """
        returns the value of the transaction.
        Credit values (money into account) are given as positive; Debit values
        (money removed from account) as negative.
        """
        NotImplementedError
        
    def get_category(self):
        """
        returns the Category object associated with the Transaction
        """
        NotImplementedError
        
    def set_category(self, category):
        """
        sets the Category this transaction is associated with
        """
        NotImplementedError
        
    def get_account(self):
        """
        returns the Account object this transaction is counted against
        """
        NotImplementedError
        
class BudgetPeriod(NamedModel):
    """
    A Budget Period object is instantiated for each period as defined by the
    parent Budget object. This class contains actual start and end dates (the
    Budget object only has the period length, and thus a new BudgetPeriod is
    made for each period), and can be associated with Earmark obejcts to track
    portions of account balances that are appropriated for a budget period.
    
    Start and end dates are inclusive.
    """
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    parent_budget = models.ForeignKey(Budget)
    is_closed_out = models.BooleanField(False)
    
    def __unicode__(self):
        NotImplementedError
        
    def get_start_date(self):
        """
        returns the start date of the budget period as a DateTime object
        """
        NotImplementedError
        
    def get_end_date(self):
        """
        returns the end date of the budget period as a DateTime object
        """
        NotImplementedError
        
    def get_parent_budget(self):
        """
        returns the Budget object that defines the budget for which this period exists
        """
        NotImplementedError
        
    def get_remaining_balance(self):
        """
        returns the balance remaining in the budget. This value is calculated
        from Earmarks associated with this BudgetPeriod and Transactions that are
        related to this BudgetPeriod vie Categories associated with the parent Budget object
        """
        NotImplementedError
        
    def get_earmark_set(self):
        """
        returns the set of Earmark objects associated with this BudgetPeriod
        """
        NotImplementedError
        
    def close_out(self, new_budget_period):
        """
        closes out this BudgetPeriod. The parent Budget EndPolicy is processed
        and this BudgetPeriod is marked as closed.
        """
        NotImplementedError
        
    def is_closed_out(self):
        """
        returns True if the BudgetPeriod has been processed and closed out,
        returns False if the BudgetPeriod is still active
        """
        NotImplementedError
        
class Earmark(NamedModel):
    """
    An Earmark object represents a sum of money (from an Account) that has been
    earmarked for a budget (specifically, a BudgetPeriod).
    
    The Earmark can be moved from one BudgetPeriod to another by changing the
    associated BudgetPeriod. It cannot be moved from one Account to another
    (since the money physically resides in that account, generally); move money
    to another account first (with a Transaction) and then make a new Earmark
    object if you wish to earmark money from a different account.
    """
    
    account = models.ForeignKey(Account)
    budget_period = models.ForeignKey(BudgetPeriod)
    value = models.FloatField()
    
    def __unicode__(self):
        NotImplementedError
        
    def get_account(self):
        """
        returns the Account object associated with this Earmark
        """
        NotImplementedError
        
    def get_budget_period(self):
        """
        returns the BudgetPeriod object associated with this Earmark
        """
        NotImplementedError
        
    def set_budget_period(self, budget_period):
        """
        sets the BudgetPeriod object with which this Earmark is associated.
        This clears the previous association, if any.
        """
        NotImplementedError
        
    def get_value(self):
        """
        returns the amount of money earmarked.
        """
        NotImplementedError
        
class PeriodLength(NamedModel):
    """
    Abstract class that determines a period length. Since months are not always
    the same number of days, and years can be leap years, etc., this class exists
    to help in determining the length of a period.
    """
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        NotImplementedError
        
    def get_current_period_start_date(self):
        """
        returns the start date of the current period
        """
        NotImplementedError
        
    def get_current_period_end_date(self):
        """
        returns the end date of the current period (inclusive)
        """
        NotImplementedError
        
    def in_current_period(self, date_time):
        """
        returns True if the given date_time is in the current period, otherwise returns False
        """
        NotImplementedError
        
class Month(PeriodLength):
    """
    Represents a one month period length (eg, a budget would have this period
    length if the money for that budget is allocated monthly).
    """

    def __unicode__(self):
        NotImplementedError
        
    def get_current_period_start_date(self):
        """
        returns the start date of the current period
        """
        NotImplementedError
        
    def get_current_period_end_date(self):
        """
        returns the end date of the current period (inclusive)
        """
        NotImplementedError
        
    def in_current_period(self, date_time):
        """
        returns True if the given date_time is in the current period, otherwise returns False
        """
        NotImplementedError
        
class CarryOverAllPolicy(EndPolicy):
    """
    EndPolicy implementation.
    
    See the Description field for details on behaviour.
    """
    
    def __unicode__(self):
        NotImplementedError
        
    def calculate_budget_period_balance(self, budget_period):
        """
        returns the float value of the budget's remaining balance (positive or
        negative depending on surplus or shortfall)
        """
        NotImplementedError
        
    def apply_policy(self, new_budget_period):
        """
        performs the actions of the end policy, altering the given new
        BudgetPolicy object such that it can be used as the next current BudgetPeriod
        """
        NotImplementedError
        
class TransactionGroup(NamedModel):
    """
    A TransactionGroup is a group of Transaction objects. This is used when
    sets of Transactions need to be grouped together for reference.
    
    For example, a series of transactions all to do with a camping trip might
    be group together in a TransactionGroup so that they can be accessed together later.
    """
    
    transactions = models.ManyToManyField(Transaction)
    
    def __unicode__(self):
        NotImplementedError
        
    def get_transaction_set(self):
        """
        returns the set of all transactions in this group
        """
        NotImplementedError
        
    def add_transaction(self, transaction):
        """
        adds the given Transaction t this group
        """
        NotImplementedError
        
    def remove_transaction(self, transaction):
        """
        removes the given Transaction from this group.
        """
        NotImplementedError
        
class SurplusCarryNegativePolicy(EndPolicy):
    """
    EndPolicy implementation.
    
    See the Description field for details on behaviour.
    """
    
    def __unicode__(self):
        NotImplementedError
        
    def calculate_budget_period_balance(self, budget_period):
        """
        returns the float value of the budget's remaining balance (positive or
        negative depending on surplus or shortfall)
        """
        NotImplementedError
        
    def apply_policy(self, new_budget_period):
        """
        performs the actions of the end policy, altering the given new
        BudgetPolicy object such that it can be used as the next current BudgetPeriod
        """
        NotImplementedError
        