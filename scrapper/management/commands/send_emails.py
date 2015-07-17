from decouple import config
from lib.mail import EmailTemplate

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from scrapper.scrapper import Vivo


User = get_user_model()
class Command(BaseCommand):
    help = 'Send new available tickets email'

    def handle(self, *args, **options):
        client = Vivo()
        client._get_ticket_info()
        availables = client._save_tickets()

        if len(availables) > 0:
            emails = User.objects.filter(is_active=True).values_list('email', flat=True)
            mail = EmailTemplate(
                subject=u'Tem evento novo!', bcc=emails,
                tpl_message=u'scrapper/mail.txt',
                tpl_alternative=u'scrapper/mail.html',
                context={'tickets': availables}
            )

            mail.send()
