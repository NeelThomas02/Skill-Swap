# users/views.py

from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LogoutView
from .models import Profile
from django.views import generic
from .forms import ProfileForm
from django.db import models
from django.views.generic import DetailView
from reputation.models import Vote

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login')  # redirect to login after signup
    def form_valid(self, form):
       # 1) Let CreateView save the new User and build its HttpResponseRedirect
        response = super().form_valid(form)
        # 2) Create the associated Profile
        Profile.objects.create(user=self.object)
        # 3) Return the redirect response so the view completes properly
        return response

class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = 'users/profile.html'

    def get_object(self):
        # get or create a Profile for the logged-in user
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_context_data(self, **kwargs):
         ctx = super().get_context_data(**kwargs)
         votes = self.object.votes.all()
         up_count   = votes.filter(upvote=True).count()
         down_count = votes.filter(upvote=False).count()
         score = up_count - down_count
         ctx['reputation_score'] = score

         # ---- Tier logic ----
         if score < 1:
             tier, style = 'Novice', 'secondary'
         elif score < 5:
             tier, style = 'Intermediate', 'info'
         elif score < 10:
             tier, style = 'Advanced', 'primary'
         else:
             tier, style = 'Expert', 'success'
         ctx['reputation_tier']       = tier
         ctx['reputation_tier_class'] = f'badge bg-{style} text-white'
         return ctx

class LogoutOnGetView(LogoutView):
    http_method_names = ['get', 'post']
    next_page = 'users:login'   # or wherever you want to redirect

class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        # Ensure a Profile always exists
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile'   # for clarity

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        votes = self.object.votes.all()
        up   = votes.filter(upvote=True).count()
        down = votes.filter(upvote=False).count()
        score = up - down
        ctx['reputation_score'] = score

        # ---- Tier logic ----
        if score < 1:
            tier, style = 'Novice', 'secondary'
        elif score < 5:
            tier, style = 'Intermediate', 'info'
        elif score < 10:
            tier, style = 'Advanced', 'primary'
        else:
            tier, style = 'Expert', 'success'
        ctx['reputation_tier']       = tier
        ctx['reputation_tier_class'] = f'badge bg-{style} text-white'
        # Has the logged-in user already voted on this profile?
        voter_profile = self.request.user.profile
        ctx['has_voted'] = Vote.objects.filter(
            profile=self.object,
            voter=voter_profile
        ).exists()
        return ctx