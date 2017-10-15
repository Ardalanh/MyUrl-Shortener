from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.generic import View

from .forms import NewUrlForm
from .models import Urls
from .randurl import get_random_url


class HomeView(View):
    def render(self, request):
        return render(request, 'shortener/home.html', {'form': self.form})

    def post(self, request):
        if request.user.is_authenticated():
            user = request.user
        else:
            user = User.objects.first()
        self.form = NewUrlForm(request.POST)
        if self.form.is_valid():
            random_url = get_random_url()
            requested_url = self.form.cleaned_data.get('user_url')
            try:    # chekcing if this url is already submited
                url = Urls.objects.get(user_url=requested_url)
                return redirect('info', short_id=url.short_id)
            except:
                url = self.form.save(commit=False)
                url.short_id = random_url
                url.count = 0
                url.created_by = user
                url.save()
                return redirect('info', short_id=random_url)
        return self.render(request)

    def get(self, request):
        self.form = NewUrlForm()
        return self.render(request)


def follow(request, short_id):
    """Increasing the count of URL and  forwarding the external URL."""
    url_obj = get_object_or_404(Urls, pk=short_id)
    if request.user != url_obj.created_by:
        url_obj.count += 1
        url_obj.save()
    return redirect(url_obj.user_url)


def info(request, short_id):
    """Render the information about submiter and the short URL."""
    url_obj = get_object_or_404(Urls, pk=short_id)
    host = settings.SITE_NAME
    return render(request, 'shortener/info.html',
                  {"url_obj": url_obj, "host": host})


@login_required
def profile(request, user_name):
    """Show all the URLs submited by this user."""
    user_profile = get_object_or_404(User, username=user_name)
    urls = Urls.objects.filter(created_by=user_profile)
    data_context = {
        "user_profile": user_profile,
        "urls": urls,
        "host": settings.SITE_NAME
    }
    return render(request, 'shortener/profile.html', context=data_context)
