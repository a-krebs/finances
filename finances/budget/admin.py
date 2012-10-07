from django.contrib import admin

from budget.models import (
            UserProfile,
            Budget,
            Category,
            RealAcct,
            VirtualAcct,
            RealTxn,
            VirtualTxn,
            Month,
            Year,
            )

admin.site.register(UserProfile)
admin.site.register(Budget)
admin.site.register(Category)
admin.site.register(RealAcct)
admin.site.register(VirtualAcct)
admin.site.register(RealTxn)
admin.site.register(VirtualTxn)
admin.site.register(Month)
admin.site.register(Year)