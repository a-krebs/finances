# Copyright (C) 2012  Aaron Krebs akrebs@ualberta.ca
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from shared.models import OwnedModel, UserProfile

class OwnedModelTestModel(OwnedModel):
    """
    Model to inherit from abstract OwnedModel for testing.
    """

class OwnedModelTests(TestCase):
    def setUp(self):
        self.user = User(username = 'test_user', password = 'pass')
        self.profile = UserProfile()
        self.profile.user = self.user
        self.instance = OwnedModelTestModel()
    
    def test_owner_protection(self):
        """
        OwnerProfile's owner field should only be set once.
        """
        self.instance.owner = self.profile
        
        assert(self.instance.owner == self.profile)
        
        try:
            self.instance.owner = self.profile
        except FieldError:
            assert(True)
            return
        assert(False)
        
    def test_is_allowed(self):
        factory = RequestFactory()
        request = factory.get('/')
        
        assert(self.instance.is_allowed(request) == False)
        request.user = self.profile
        assert(self.instance.is_allowed(request) == True)
        self.instance.assert_is_allowed(request)