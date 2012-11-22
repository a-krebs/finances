#Copyright (C) 2012  Aaron Krebs akrebs@ualberta.ca
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>

from django.views.generic.simple import direct_to_template

from registration.views import register

from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    # urls for simple one-step registration
    url(r'^register/$',
        register,
        {'backend': 'registration.backends.simple.SimpleBackend',
            'template_name' : 'registration/registration_form.hamlpy',
        },
        name='registration_register'
    ),
    url(r'^register/closed/$',
        direct_to_template,
        {'template': 'registration/registration_closed.hamlpy'},
        name='registration_disallowed'
    ),
    (r'', include('registration.auth_urls')),
)