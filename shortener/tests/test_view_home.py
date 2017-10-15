from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase

from ..forms import NewUrlForm
from ..views import HomeView
from ..models import User, Urls


class HomeTests(TestCase):
    def setUp(self):
        """SetUp to get response page."""
        self.user = User.objects.create_user("testusername")
        self.home_url = reverse('home')
        self.response = self.client.get(self.home_url)

    def test_home_view_csrf(self):
        """Check if html contains csrf."""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_home_view_success_status_code(self):
        """If home page runs succesfuly."""
        self.assertEquals(self.response.status_code, 200)

    def test_home_view_url_resolves_home_view(self):
        """If home page runs corrent function from view."""
        view = resolve('/')
        self.assertEquals(view.func.view_class, HomeView)

    def test_home_valid_post_data(self):
        """If URL objects gets created with valid URL."""
        data = {'user_url': 'http://www.somesite.com'}
        response = self.client.post(self.home_url, data)
        self.assertTrue(Urls.objects.exists())

    def test_home_invalid_post_data(self):
        """
        Invalid post data should not redirect.
        The expected behavior is to show the form again with validation errors.
        """
        response = self.client.post(self.home_url, {})
        form = response.context.get('form')
        self.assertEquals(self.response.status_code, 200)
        self.assertTrue(form.errors)

        data = {'user_url': 'zzzNot a Urlzzz'}
        response = self.client.post(self.home_url, data)
        form = response.context.get('form')
        self.assertEquals(self.response.status_code, 200)
        self.assertFalse(Urls.objects.exists())
        self.assertTrue(form.errors)

    def test_home_empty_post_data(self):
        """If trying to post empty should not redirect."""
        data = {'user_url': ''}
        response = self.client.post(self.home_url, data)
        self.assertFalse(Urls.objects.exists())

    def test_home_contains_form(self):
        """If home contains NewUrlForm."""
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewUrlForm)
