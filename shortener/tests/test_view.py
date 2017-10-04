from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase
from django.conf import settings

from ..forms import NewUrlForm
from ..views import home, info, follow
from ..models import User, Urls


class HomeTests(TestCase):
    def setUp(self):
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
        self.assertEquals(view.func, home)

    def test_home_valid_post_data(self):
        """If URL objects gets created with valid URL."""
        data = {'user_url': 'http://www.somesite.com'}
        response = self.client.post(self.home_url, data)
        self.assertTrue(Urls.objects.exists())

    def test_home_invalid_post_data(self):
        """
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
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
        """If home contains form."""
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewUrlForm)


class InfoTests(TestCase):
    def setUp(self):
        """
        Set up URL and user DB and get info response page.
        """
        self.user = User.objects.create_user("testusername")
        self.url = Urls.objects.create(short_id="abcABC123",
                                       user_url="https://www.google.com",
                                       count=0,
                                       created_by=self.user)
        self.info_url = reverse('info', kwargs={'short_id': 'abcABC123'})
        self.response = self.client.get(self.info_url)

    def test_info_view_success_status_code(self):
        """If view.info successfuly runs with correct data from DB."""
        self.assertEquals(self.response.status_code, 200)

    def test_info_view_not_found_status_code(self):
        """If view.info successfuly give 404 with wrong data from DB."""
        url = reverse('info', kwargs={'short_id': 'zzzzzzzz'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_info_view_resolves_info_view(self):
        """If "!" directs to info page."""
        view = resolve('/!abcABC123')
        self.assertEquals(view.func, info)

    def test_info_view_shows_the_right_user(self):
        """If created by user is the same user showing in info"""
        self.assertContains(self.response, self.user.username)

    def test_info_contains_link_back_to_home(self):
        """If info has link back to home page."""
        home_url = reverse('home')
        self.assertContains(self.response, 'href="{0}"'.format(home_url))

    def test_info_contains_link_to_orginal_url(self):
        """If info shows the submited URL."""
        self.assertContains(self.response,
                            'href="{0}"'.format(self.url.user_url))

    def test_info_containst_link_of_shorted_url(self):
        """If info shows the shorted URL."""
        self.assertContains(
            self.response,
            'href="{0}"'.format(settings.SITE_BASE_URL + 'abcABC123')
        )


class FollowTests(TestCase):
    def setUp(self):
        """Set up user and URL DB and get follow response page."""
        self.user = User.objects.create_user("testusername")
        self.url = Urls.objects.create(short_id="abcABC123",
                                       user_url="https://www.google.com",
                                       count=0,
                                       created_by=self.user)
        self.follow_url = reverse('follow', kwargs={'short_id': 'abcABC123'})
        self.response = self.client.get(self.follow_url)

    def test_follow_view_redirect_status_code(self):
        """Correct URL should successfuly redirects."""
        self.assertEquals(self.response.status_code, 302)

    def test_follow_view_not_found_status_code(self):
        """Not found status code for wrong URL."""
        url = reverse('follow', kwargs={'short_id': 'zzzzzzzz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_follow_links_to_currect_URL(self):
        """If following url is the correct url in database."""
        self.assertEquals(self.response.url, self.url.user_url)

    def test_follow_view_resolve_follow(self):
        """If follow increases the count"""
        view = resolve('/abcABC123')
        self.assertEquals(view.func, follow)
