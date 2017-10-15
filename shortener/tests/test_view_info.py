from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase
from django.conf import settings

from ..views import info
from ..models import User, Urls


class InfoTests(TestCase):
    def setUp(self):
        """
        Set up URL and user DB and get info response page.
        """
        self.username = 'testusername'
        self.password = 'abcABC123'
        self.user = User.objects.create_user(username=self.username,
                                             email="sample@email.com",
                                             password=self.password)
        self.url = Urls.objects.create(short_id="abcABC123",
                                       user_url="https://www.google.com",
                                       count=0,
                                       created_by=self.user)
        self.client.login(username=self.username, password=self.password)
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
            'href="{0}"'.format('/abcABC123')
        )
