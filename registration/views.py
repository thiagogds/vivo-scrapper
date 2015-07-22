# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import get_backends
from django.contrib.auth import login as auth_login
from django.core.exceptions import SuspiciousOperation
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from simple_email_confirmation.models import EmailAddress

from lib.mail import EmailTemplate
from registration.forms import RegistrationForm


class RegistrationView(FormView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm

    def form_valid(self, form):
        user = form.save()

        activation_url = '%s://%s%s?&activation_key=%s' % (
            self.request.scheme, self.request.get_host(),
            reverse('auth:activation'),
            user.confirmation_key
        )

        mail = EmailTemplate(
            subject=u'Ingressos Grátis - Ativação da conta', to=[user.email],
            tpl_message=u'registration/email/activation.txt',
            tpl_alternative=u'registration/email/activation.html',
            context={'activation_url': activation_url}
        )

        mail.send()

        return super(RegistrationView, self).form_valid(form)

    def get_success_url(self):
        return reverse('auth:registration_complete')


class RegistrationComplete(TemplateView):
    template_name = 'registration/registration_complete.html'

class ActivationComplete(TemplateView):
    template_name = 'registration/activation_complete.html'

def activation(request):
    activation_key = request.GET.get('activation_key', '')

    if not activation_key:
        raise SuspiciousOperation

    try:
        address = EmailAddress.objects.confirm(activation_key)
        user = address.user
    except EmailAddress.DoesNotExist, EmailAddress.EmailConfirmationExpired:
        raise SuspiciousOperation

    return redirect('auth:activation_complete')


register = RegistrationView.as_view()
registration_complete = RegistrationComplete.as_view()
activation_complete = ActivationComplete.as_view()
