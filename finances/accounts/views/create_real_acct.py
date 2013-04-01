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

from django import forms
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import BaseFormView
from django.views.generic.base import TemplateView

from shared.models import CHARFIELD_MAX_LENGTH, RealAcct
from shared.views.mixins.login_required import LoginRequiredMixin


class RealAcctForm(forms.Form):
    name = forms.CharField(max_length=CHARFIELD_MAX_LENGTH)


class CreateRealAcct(BaseFormView, LoginRequiredMixin, TemplateView):
    """
    Create a new RealAcct.
    """
    
    template_name = 'accounts/create_real_acct.hamlpy'
    form_class = RealAcctForm
    success_url = reverse_lazy('accounts:index')
    
    def form_valid(self, form):
        RealAcct.objects.create(
            owner=self.request.user,
            name=form.cleaned_data['name']
            )
        return super(CreateRealAcct, self).form_valid(form)
