from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import SignUpForm


class SignupView(View):
    """Signup view contains the UserCreationForm plus email, first_name and last_name fields."""

    def render(self, request):
        return render(request, 'signup.html', {'form': self.form})

    def post(self, request):
        self.form = SignUpForm(request.POST)
        if self.form.is_valid():
            user = self.form.save()
            auth_login(request, user)
            return redirect('home')
        return self.render(request)

    def get(self, request):
        self.form = SignUpForm()
        return self.render(request)
