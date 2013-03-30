# Copyright (C) 2013  Aaron Krebs akrebs@ualberta.ca

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

from django.views.generic.base import TemplateView
from django.views.generic.detail import BaseDetailView

from shared.views.mixins.login_required import LoginRequiredMixin
from shared.models import RealAcct


class AccountsShowRealAcct(BaseDetailView, LoginRequiredMixin, TemplateView):
    """
    View the transactions listed against a RealAcct.
    """
    context_object_name = 'real_acct'
    template_name = 'accounts/show_real_acct.hamlpy'
    
    def dispatch(self, request, *args, **kwargs):
        self.queryset = RealAcct.objects.filter(_owner=request.user.id)
        return super(AccountsShowRealAcct, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(AccountsShowRealAcct, self).get_context_data(
            txns=self.object.realtxn_set.all(),
            **kwargs
        )
