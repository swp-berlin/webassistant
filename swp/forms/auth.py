from django.contrib.auth import forms as auth_forms

from .mixins import BlueprintFormMixin


class LoginForm(BlueprintFormMixin, auth_forms.AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.input_type = 'email'


class PasswordResetForm(BlueprintFormMixin, auth_forms.PasswordResetForm):
    pass


class PasswordResetConfirmForm(BlueprintFormMixin, auth_forms.SetPasswordForm):
    pass
