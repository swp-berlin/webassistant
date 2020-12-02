from django.contrib.auth import views as auth_views
from swp.forms import LoginForm

__all__ = [
    'LoginView',
    'LogoutView',
]


class LoginView(auth_views.LoginView):
    template_name = 'auth/login.html'
    form_class = LoginForm


class LogoutView(auth_views.LogoutView):
    template_name = 'auth/logout.html'
