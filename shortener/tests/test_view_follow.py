
from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase

from ..views import follow
from ..models import User, Urls


class FollowTests(TestCase):
    def setUp(self):
        """Set up user and URL DB and get follow response page."""
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(
            username=self.username,
            email='john@doe.com',
            password=self.password
        )
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
        """If url '/abcABC123' runs the correct view."""
        view = resolve('/abcABC123')
        self.assertEquals(view.func, follow)

    def test_follow_view_increase_count(self):
        """Follow should increase the count."""
        self.url.refresh_from_db()
        self.assertEquals(self.url.count, 1)

    def test_follow_view_does_not_increase_by_submited_user(self):
        """Follow should not increase the count if the submited user clicks."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.follow_url)
        self.url.refresh_from_db()
        self.assertEquals(self.url.count, 1)
