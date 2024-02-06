from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.lorem_ipsum import COMMON_P as LOREM_IPSUM
from django.views.generic import TemplateView

from swp.forms import PasswordResetForm
from swp.models import Monitor, Scraper, Thinktank, Publication, ScraperError
from swp.tasks.scheduling import get_absolute_scraper_url
from swp.utils.mail import render_mail


class MailPreView(LoginRequiredMixin, TemplateView):
    template_name = 'mails/preview.html'

    def get_context_data(self, *, identifier, **kwargs):
        context = self.get_mail_context(identifier)
        subject, plain, html = render_mail(identifier, request=self.request, context=context)

        kwargs.update(subject=subject, plain=plain, html=html)

        return super().get_context_data(**kwargs)

    def get_mail_context(self, identifier):
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
            thinktank = Thinktank(id=1, name='Preview')
            scraper = Scraper(id=1, thinktank=thinktank)
            publication = Publication(id=1, thinktank=thinktank, url='https://example.com', title='Example')

            return {
                'scraper': scraper,
                'thinktank': thinktank,
                'url': get_absolute_scraper_url(scraper),
                'errors': [
                    ScraperError(scraper=scraper, publication=publication, message='Error 1'),
                    ScraperError(scraper=scraper, title='Something went wrong', message='Error 2'),
                ],
            }

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
