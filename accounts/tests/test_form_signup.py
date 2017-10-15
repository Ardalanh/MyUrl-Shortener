from django.test import TestCase
from ..forms import SignUpForm


class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        """
        SignUpForm should have 6 fields.
        -first_name
        -last_name
        -username
        -email
        -password1
        -password2
        """
        form = SignUpForm()
        expected = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', ]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
