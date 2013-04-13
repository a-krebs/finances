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

from django.views.generic.edit import BaseFormView
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.forms.models import modelformset_factory

from shared.views.mixins import LoginRequiredMixin
from shared.models import Category
from django.db import transaction
from django import forms


class CategoryForm(forms.ModelForm):
    def save(self, owner, commit=True, *args, **kwargs):
        instance = super(CategoryForm, self).save(commit=False, *args, **kwargs)
        instance.owner = owner
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Category
        exclude = ('owner',)

CategoriesFormset = modelformset_factory(
    Category,
    form=CategoryForm,
    can_delete=True,
)


class ManageCategories(BaseFormView, LoginRequiredMixin, TemplateView):
    """
    Use a formset to add, edit, or delete categories.
    """
    template_name = 'budgets/manage_categories.hamlpy'
    form_class = CategoriesFormset
    success_url = reverse_lazy('budgets:categories')
    
    def get_form_kwargs(self):
        kwargs = super(ManageCategories, self).get_form_kwargs()
        kwargs.update(queryset=Category.objects.filter(owner=self.request.user))
        return kwargs
    
    def form_valid(self, form):
        with transaction.commit_on_success():
            for f in form.forms:
                if len(f.changed_data):
                    _ = f.save(owner=self.request.user)
        return super(ManageCategories, self).form_valid(form)
