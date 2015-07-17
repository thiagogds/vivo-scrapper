#-*- coding: utf-8 -*-
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.conf import settings


class EmailTemplate(EmailMultiAlternatives):
    def __init__(self, tpl_message, context, tpl_alternative=None, **kwargs):
        context = Context(context)
        super(EmailTemplate, self).__init__(**kwargs)

        self.message_from_template(tpl_message, context)
        if tpl_alternative:
            self.attach_alternative_from_template(tpl_alternative, context)

    def message_from_template(self, template, context):
        self.body = render_to_string(template, context)

    def attach_alternative_from_template(self, template, context):
        content = render_to_string(template, context)
        self.attach_alternative(content, 'text/html')


class EmailTemplateDefaultCc(EmailTemplate):
    def __init__(self, *args, **kwargs):
        # Nós queremos receber cópia dos emails enviados para os inscritos.
        if not 'cc' in kwargs:
            kwargs['cc'] = [settings.DEFAULT_CC_EMAIL]

        super(EmailTemplateDefaultCc, self).__init__(*args, **kwargs)
