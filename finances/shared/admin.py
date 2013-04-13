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

from django.contrib import admin

from shared.models import (
            Budget,
            Category,
            RealAcct,
            VirtualAcct,
            RealTxn,
            VirtualTxn,
            )

admin.site.register(Budget)
admin.site.register(Category)
admin.site.register(RealAcct)
admin.site.register(VirtualAcct)
admin.site.register(RealTxn)
admin.site.register(VirtualTxn)
