#coding: utf-8
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core import mail

from mock import patch
from unipath import Path
from model_mommy.mommy import make as m

from scrapper.models import Ticket
from scrapper.scrapper import Vivo

User = get_user_model()
class TestSendEmail(TestCase):

    @patch('scrapper.scrapper.Vivo')
    def test_send_email_for_active_users(self, mock_client):
        instance = mock_client.return_value
        instance._save_tickets.return_value = [m(Ticket, avaliability='BK'),]
        m(User, email="john@example.com", is_active=True)
        m(User, email="john+1@example.com", is_active=True)
        m(User, email="john+2@example.com", is_active=False)

        self.assertEqual(0, len(mail.outbox))

        call_command('send_emails')

        self.assertEqual(2, len(mail.outbox))
        self.assertIn('john@example.com', mail.outbox[0].to)
        self.assertIn('john+1@example.com', mail.outbox[1].to)
