from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase

from ..forms import SignUpForm
from ..views import signup


class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_form_inputs(self):
        """
        The view must contain five inputs.
        csrf, username, email, password1, password2
        """
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_sginup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'test_username',
            'email': 'testmail@test.com',
            'password1': 'abcABC123',
            'password2': 'abcABC123'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redirect_home(self):
        """After successful signup, redirect to home."""
        self.assertRedirects(self.response, self.home_url)

    def test_user_created(self):
        """If user exists in DB."""
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        """After user logining/signing up, page should contain the user info."""
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})
        data1 = {
            'username': 'test_username',
            'email': 'wrongemailformat@',
            'password1': 'abcABC123',
            'password2': 'abcABC13'
        }
        self.response1 = self.client.post(url, data1)
        data2 = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': ''
        }
        self.response2 = self.client.post(url, data2)

    def test_signup_status_code(self):
        """An invalid form submission should return to the same page."""
        self.assertEquals(self.response.status_code, 200)
        self.assertEquals(self.response1.status_code, 200)
        self.assertEquals(self.response2.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
        form1 = self.response1.context.get('form')
        self.assertTrue(form.errors)
        form2 = self.response2.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())