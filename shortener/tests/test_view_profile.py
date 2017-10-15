from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase
from django.conf import settings

from ..views import profile
from ..models import User, Urls


class ProfileTests(TestCase):
    def setUp(self):
        """
        Set up URL and user DB and get profle response page.
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
        self.profile_url = reverse('profile', kwargs={'user_name': self.username})
        self.response = self.client.get(self.profile_url)

    def test_profile_view_success_status_code(self):
        """If view.profile successfuly runs with correct data from DB."""
        self.assertEquals(self.response.status_code, 200)

    def test_profile_view_does_not_show_other_users(self):
        """If the user trys to access another profile, redirects to no_my_profile."""
        user = User.objects.create_user(username="notmyusername",
                                        email="notmy@email.com",
                                        password=self.password)
        wrong_profile_url = reverse('profile', kwargs={'user_name': 'notmyusername'})
        response = self.client.get(wrong_profile_url)
        self.assertContains(response, self.profile_url, 2)

    def test_profile_view_resolves_profile_view(self):
        """If "/u/**" runs the corect view."""
        view = resolve('/u/testusername')
        self.assertEquals(view.func, profile)

    def test_profile_view_shows_the_right_user(self):
        """If informations is for the same user showing in profile."""
        self.assertContains(self.response, self.user.username)
        self.assertContains(self.response, self.user.first_name)
        self.assertContains(self.response, self.user.last_name)
        self.assertContains(self.response, self.user.email)

    def test_profile_view_shows_the_right_table(self):
        """If URLs are for the user."""
        self.assertContains(self.response, self.url.user_url)


class LoginRequiredProfileTests(TestCase):
    def setUp(self):
        self.url = reverse('profile', kwargs={'user_name': 'testuser'})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(
            login_url=login_url, url=self.url))
