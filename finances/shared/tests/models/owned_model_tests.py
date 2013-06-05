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

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from shared.models import OwnedModel


class OwnedModelTestModel(OwnedModel):
    """
    Model to inherit from abstract OwnedModel for testing.
    """


class OwnedModelTests(TestCase):
    def setUp(self):
        self.user = User(username='test_user', password='pass')
        self.instance = OwnedModelTestModel(owner=self.user)
    
    def test_is_allowed(self):
        factory = RequestFactory()
        request = factory.get('/')
        
        assert(self.instance.is_allowed(request) == False)
        request.user = self.user
        assert(self.instance.is_allowed(request) == True)
        self.instance.assert_is_allowed(request)
