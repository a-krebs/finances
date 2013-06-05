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

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from shared.models import RealAcct


class RealTxnListForRealAcctMixin(object):
    """
    Add a list of the RealTxn objects listed against a RealAcct to context.
    """
    
    def get_context_data(self, **kwargs):
        realacct_pk = self.kwargs.get('realacct_pk', None)
        
        if realacct_pk is None:
            raise AttributeError(u"Detail mixin %s must be called with "
                                 u"an object pk." % self.__class__.__name__)
        try:
            realacct = RealAcct.objects.get(
                pk=realacct_pk,
                owner=self.request.user
            )
        except ObjectDoesNotExist:
            raise Http404(u"No %(verbose_name)s found matching the query" %
                          {'verbose_name': RealAcct._meta.verbose_name})  # @UndefinedVariable
        
        context = {
            'realacct': realacct,
            'realtxn_list': realacct.realtxn_set.all(),
        }
        context.update(super(RealTxnListForRealAcctMixin, self).get_context_data(**kwargs))
        return context
