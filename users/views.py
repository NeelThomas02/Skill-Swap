# users/views.py

from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LogoutView
from .models import Profile

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login')  # redirect to login after signup
    def form_valid(self, form):
       # first create the User...
       response = super().form_valid(form)
       # ...then ensure they have a Profile
       Profile.objects.create(user=self.object)
       return 

class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = 'users/profile.html'
    
    def get_object(self):
        # get or create a Profile for the logged-in user
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

class LogoutOnGetView(LogoutView):
    http_method_names = ['get', 'post']
    next_page = 'users:login'   # or wherever you want to redirect