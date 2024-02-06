from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.utils.lorem_ipsum import COMMON_P as LOREM_IPSUM
from django.views.generic import TemplateView

from swp.forms import PasswordResetForm
from swp.models import Monitor, Publication
from swp.tasks.errorreport import collect_scraper_errors
from swp.utils.mail import render_mail


class MailPreView(LoginRequiredMixin, TemplateView):
    template_name = 'mails/preview.html'

    def get_context_data(self, *, identifier, **kwargs):
        context = self.get_mail_context(identifier)
        subject, plain, html = render_mail(identifier, request=self.request, context=context)

        kwargs.update(subject=subject, plain=plain, html=html)

        return super().get_context_data(**kwargs)

    @transaction.atomic
    def get_mail_context(self, identifier, *, using: str = None):
        if identifier == 'monitor-publications':
            monitor = Monitor(name='Preview', description=LOREM_IPSUM)
            publications = Publication.objects.order_by('?')[:10]

            return {
                'monitor': monitor,
                'last_sent': monitor.created,
                'publications': publications,
            }

        if identifier == 'password-reset':
            return MailPreViewPasswordResetForm.get_context(self.request)

        if identifier == 'scraper-errors':
            queryset, pools = collect_scraper_errors(using)

            return {'pools': pools}

        raise NotImplementedError(f'Missing mail context for {identifier}.')


class MailPreViewPasswordResetForm(PasswordResetForm):

    def __init__(self, user):
        self.user = user
        self.context = {}

        data = {'email': user.email}

        super().__init__(data=data)

    def send_mail(self, subject_template_name, email_template_name, context, *args, **kwargs):
        self.context = context

    def get_users(self, email):
        return [self.user]

    @classmethod
    def get_context(cls, request):
        form = cls(request.user)

        cls.full_clean(form)
        cls.save(form, request=request)

        return form.context
