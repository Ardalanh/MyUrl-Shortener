from django import forms
from .models import Urls


class NewUrlForm(forms.ModelForm):
    user_url = forms.URLField(
        widget=forms.URLInput(),
        label="Enter URL",
        max_length=4000,
        help_text='The max length is 4000 characters. also "http://" is requried',
        initial='http://'
    )

    class Meta:
        model = Urls
        fields = ['user_url']
