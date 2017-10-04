from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

from .forms import NewUrlForm
from .models import Urls
from .randurl import get_random_url

from random import choice


def home(request):
    """Home/Index view, contains a simple form for URL."""
    if request.method == 'POST':
        # randomly chocing a user,
        # Atleast one user should exist, spuerusers count
        user = choice(User.objects.all())  # random user
        form = NewUrlForm(request.POST)
        if form.is_valid():
            random_url = get_random_url()
            requested_url = form.cleaned_data.get('user_url')
            try:    # chekcing if this url is already submited
                url = Urls.objects.get(user_url=requested_url)
                return redirect('info', short_id=url.short_id)
            except:
                url = form.save(commit=False)
                url.short_id = random_url  # TODO: make function for generating
                url.count = 0
                url.created_by = user
                url.save()
                return redirect('info', short_id=random_url)
    else:
        form = NewUrlForm()
    return render(request, 'shortener/home.html', {'form': form})


def follow(request, short_id):
    """Increasing the count of URL and  forwarding the external URL."""
    url_obj = get_object_or_404(Urls, pk=short_id)
    url_obj.count += 1
    url_obj.save()
    return redirect(url_obj.user_url)


def info(request, short_id):
    """Render the information about submiter and the short URL."""
    url_obj = get_object_or_404(Urls, pk=short_id)
    short_url = settings.SITE_BASE_URL + short_id
    return render(request, 'shortener/info.html',
                  {"url_obj": url_obj, "short_url": short_url})
