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
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from shared.models import UserProfile

class UserProfileTestModel(UserProfile):
    """
    Inherits from UserProfile to test abstract class.
    """

class UserProfileTests(TestCase):
    
    def test_user_protection(self):
        """
        UserProfile's user field should only be set once.
        """
        user = User(username = 'test_user', password = 'pass')
        instance = UserProfileTestModel()
        instance.user = user
        
        assert(instance.user == user)
        
        try:
            instance.user = user
        except FieldError:
            assert(True)
            return
        assert(False)