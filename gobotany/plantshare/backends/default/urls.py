"""
Customized URLConf for our customized django-registration backend.
NOTE: This can be tweaked in the future if we want to change the workflow
a little.
"""

from django.conf.urls import url, include
from django.contrib.auth.views import (password_change, password_reset,
    password_reset_complete, password_reset_confirm, password_reset_done)
from django.views.generic.base import TemplateView

from registration.backends.default.views import ActivationView
from registration.backends.default.views import RegistrationView

from gobotany.plantshare.views import (change_email,
    change_email_confirmation_sent, confirm_email)
from .forms import RegistrationFormWithHiddenField

urlpatterns = [
    url(r'^activate/complete/$',
        TemplateView.as_view(
            template_name='registration/activation_complete.html'),
        name='registration_activation_complete'),
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to the
    # view; that way it can return a sensible "invalid key" message instead
    # of a confusing 404.
    url(r'^activate/(?P<activation_key>\w+)/$',
        ActivationView.as_view(),
        name='registration_activate'),
    url(r'^register/$',
        RegistrationView.as_view(form_class=RegistrationFormWithHiddenField),
        name='registration_register'),
    url(r'^register/complete/$',
        TemplateView.as_view(
        template_name='registration/registration_complete.html'),
        name='registration_complete'),
    url(r'^register/closed/$',
        TemplateView.as_view(
        template_name='registration/registration_closed.html'),
        name='registration_disallowed'),

    # Use names from django.auth.urls.py to avoid a NoMatch error as seen with
    # password_reset_done (http://stackoverflow.com/questions/20307473).
    url(r'^password/change/$', password_change,
        {'template_name': 'registration/change_password.html'},
        name='password_change'),
    url(r'^password/change/done/$',
        TemplateView.as_view(
        template_name='registration/change_password_done.html'),
        name='password_change_done'),
    url(r'^password/reset/$', password_reset,
        {'template_name': 'registration/forgot_password.html'},
        name='password_reset'),
    url(r'^password/reset/done/$', password_reset_done,
        {'template_name': 'registration/reset_password_email_sent.html'},
        name='password_reset_done'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm,
        {'template_name': 'registration/choose_new_password.html'},
        name='password_reset_confirm'),
    url(r'^password/reset/complete/$', password_reset_complete,
        {'template_name': 'registration/change_password_done.html'},
        name='password_reset_complete'),

    url(r'^email/change/$', change_email,
        name='ps-change-email'),
    url(r'^email/change/confirmation-sent/$', change_email_confirmation_sent,
        name='ps-change-email-confirmation-sent'),
    url(r'^email/confirm/(?P<key>\w+)/$', confirm_email,
        name='ps-confirm-email'),

    url(r'', include('registration.auth_urls')),
]
