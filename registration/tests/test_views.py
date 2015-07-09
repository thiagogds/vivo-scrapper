# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from registration.forms import RegistrationForm

User = get_user_model()


class RegistrationView(TestCase):
    def setUp(self):
        self.url = reverse('auth:registration')
        self.response = self.client.get(self.url)

    def test_renders_correct_template(self):
        self.assertTemplateUsed(self.response, 'registration/registration.html')

    def test_form_in_context(self):
        self.assertIn('form', self.response.context)
        form = self.response.context['form']
        self.assertIsInstance(form, RegistrationForm)

    def test_valid_post(self):
        response = self.client.post(self.url, {
            'email': 'jalim@example.com',
            'full_name': 'Jalim Rabei',
            'password1': '123qaz',
            'password2': '123qaz',
        })

        self.assertRedirects(response,
            reverse(
                'auth:registration_complete',
            )
        )

    def test_registration_dont_activate_user(self):
        response = self.client.post(self.url, {
            'email': 'jalim@example.com',
            'full_name': 'Jalim Rabei',
            'password1': '123qaz',
            'password2': '123qaz',
        })

        user = User.objects.get(email='jalim@example.com')

        self.assertFalse(user.is_active)

    def test_registration_sends_confirmation_email(self):
        self.assertEqual(0, len(mail.outbox))
        response = self.client.post(self.url, {
            'email': 'jalim@example.com',
            'full_name': 'Jalim Rabei',
            'password1': '123qaz',
            'password2': '123qaz',
        })

        self.assertEqual(1, len(mail.outbox))

    def test_mail_content(self):
        self.assertEqual(0, len(mail.outbox))
        response = self.client.post(self.url, {
            'email': 'jalim@example.com',
            'full_name': 'Jalim Rabei',
            'password1': '123qaz',
            'password2': '123qaz',
        })
        msg = mail.outbox[0]

        user = User.objects.last()
        self.assertIn(user.confirmation_key, msg.body)
        self.assertIn(reverse('auth:activation'), msg.body)


class ActivationView(TestCase):
    def setUp(self):
        email = 'jalim@example.com'
        self.user = User.objects.create_user(email, is_active=False)

    def test_activate_user(self):
        confirmation_key = self.user.confirmation_key
        url = reverse("auth:activation") + "?activation_key=%s" % confirmation_key
        response = self.client.get(url)

        user = User.objects.last()
        self.assertTrue(user.is_active)

    def test_activation_key_required(self):
        url = reverse("auth:activation")
        response = self.client.get(url)

        self.assertEqual(400, response.status_code)

    def test_service_required(self):
        url = reverse("auth:activation")
        response = self.client.get(url)

        self.assertEqual(400, response.status_code)

    def test_wrong_confirmation_key(self):
        confirmation_key = self.user.confirmation_key
        url = reverse("auth:activation") + "?activation_key=%s" % "sfafafsafsa"
        response = self.client.get(url)

        self.assertEqual(400, response.status_code)

    def test_redirec_to_login(self):
        confirmation_key = self.user.confirmation_key
        url = reverse("auth:activation") + "?activation_key=%s" % confirmation_key
        response = self.client.get(url)

        expected_url = "http://testserver/login/"

        self.assertRedirects(response, expected_url, fetch_redirect_response=False)
