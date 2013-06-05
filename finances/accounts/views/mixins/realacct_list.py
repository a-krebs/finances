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

from shared.models import RealAcct


class RealAcctListMixin(object):
    """
    Add a list of the user's RealAccts to context
    """
    
    def get_context_data(self, **kwargs):
        context = {
            'realacct_list': RealAcct.objects.filter(
                owner=self.request.user
            )
        }
        context.update(super(RealAcctListMixin, self).get_context_data(**kwargs))
        return context
