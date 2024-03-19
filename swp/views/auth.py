from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from swp.forms import LoginForm, PasswordResetForm, PasswordResetConfirmForm

__all__ = [
    'LoginView',
    'LogoutView',
    'PasswordResetConfirmView',
    'PasswordResetCompleteView',
    'PasswordResetDoneView',
    'PasswordResetView',
]


class LoginView(auth_views.LoginView):
    template_name = 'auth/login.html'
    form_class = LoginForm


class LogoutView(auth_views.LogoutView):
    template_name = 'auth/logout.html'


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'auth/password-reset/start.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('password-reset:done')
    email_template_name = 'mails/password-reset.plain'
    html_email_template_name = 'mails/password-reset.html'
    subject_template_name = 'mails/password-reset.subject'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'auth/password-reset/confirm.html'
    form_class = PasswordResetConfirmForm
    success_url = reverse_lazy('password-reset:complete')


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'auth/password-reset/complete.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'auth/password-reset/done.html'
