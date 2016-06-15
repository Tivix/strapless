from allauth.account.adapter import DefaultAccountAdapter as BaseDefaultAccountAdapter
from allauth.account import app_settings


class DefaultAccountAdapter(BaseDefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context, *args, **kwargs):
        # update context sent to email
        context['ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS'] = app_settings.EMAIL_CONFIRMATION_EXPIRE_DAYS
        return super(DefaultAccountAdapter, self).send_mail(template_prefix, email, context, *args, **kwargs)
