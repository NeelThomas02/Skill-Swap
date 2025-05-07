# reputation/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect

class VoteView(LoginRequiredMixin, View):
    def post(self, request):
        # TODO: implement actual Vote creation logic here
        # For now, just redirect back to your profile or wherever
        return redirect('users:profile')
