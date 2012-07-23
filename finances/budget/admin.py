from django.contrib import admin

from budget.models import (
            UserProfile,
            EndPolicy,
            Budget,
            Category,
            Account,
            Transaction,
            BudgetPeriod,
            Earmark,
            Month,
            CarryOverAllPolicy,
            SurplusCarryNegativePolicy,
            TransactionGroup,
            )

admin.site.register(UserProfile)
admin.site.register(EndPolicy)
admin.site.register(Budget)
admin.site.register(Category)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(BudgetPeriod)
admin.site.register(Earmark)
admin.site.register(Month)
admin.site.register(CarryOverAllPolicy)
admin.site.register(SurplusCarryNegativePolicy)
admin.site.register(TransactionGroup)
