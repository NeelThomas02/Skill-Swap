# users/views.py

from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .models import Profile

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login')  # redirect to login after signup

class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = 'users/profile.html'
    
    def get_object(self):
        # show the logged-in user’s profile
        return Profile.objects.get(user=self.request.user)
