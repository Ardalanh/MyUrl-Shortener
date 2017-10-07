from django.core import mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase


class PasswordResetMailTests(TestCase):
    def setUp(self):
        """Setup for getting email and response."""
        User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.response = self.client.post(reverse('password_reset'), {'email': 'john@doe.com'})
        self.email = mail.outbox[0]

    def test_email_subject(self):
        """If the subject is correct."""
        self.assertEqual('[MyUrl] Please reset your password.', self.email.subject)

    def test_email_body(self):
        """
        If the correct url is sent for resetting password.
        If the correct name and email is sent.
        """
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('john', self.email.body)
        self.assertIn('john@doe.com', self.email.body)

    def test_email_to(self):
        """Email is sent to the correct user."""
        self.assertEqual(['john@doe.com', ], self.email.to)
