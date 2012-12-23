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
from django.contrib.auth import views as auth_views
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from registration.views import register

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
    url(r'^login/$',
        auth_views.login,
        {'template_name': 'registration/login.hamlpy'},
        name='auth_login'
    ),
    url(r'^logout/$',
        auth_views.logout,
        {'template_name': 'registration/logout.hamlpy'},
        name='auth_logout'
    ),
    url(r'^password/change/$',
        auth_views.password_change,
        {'template_name' : 'registration/password_change_form.hamlpy',
            # ugh, this is tied to the namespace; needs to be namespace-agnostic
            # since the namspace is determined by the importing app
            # TODO: see Issue #1
            'post_change_redirect' : reverse_lazy('registration:auth_password_change_done')
        },
        name='auth_password_change'
    ),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        {'template_name' : 'registration/password_change_done.hamlpy'},
        name='auth_password_change_done'
    ),
    url(r'^password/reset/$',
        auth_views.password_reset,
        {'template_name' : 'registration/password_reset_form.hamlpy',
            # same issue as above
            'post_reset_redirect' : reverse_lazy('registration:auth_password_reset_done'),
            'email_template_name' : 'registration/password_reset_email.hamlpy',
            'subject_template_name' : 'registration/password_reset_subject.hamlpy',
        },
        name='auth_password_reset'
    ),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name' : 'registration/password_reset_confirm.hamlpy'},
        name='auth_password_reset_confirm'
    ),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        {'template_name' : 'registration/password_reset_complete.hamlpy'},
        name='auth_password_reset_complete'
    ),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        {'template_name' : 'registration/password_reset_done.hamlpy'},
        name='auth_password_reset_done'
    ),
)