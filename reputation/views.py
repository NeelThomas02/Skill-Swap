from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from .models import Vote
from users.models import Profile

class VoteView(LoginRequiredMixin, View):
    def post(self, request):
        # profile being voted on
        profile_id = request.POST.get('profile_id')
        value      = int(request.POST.get('value'))  # +1 or -1
        profile    = get_object_or_404(Profile, pk=profile_id)

        # record or update the vote
        # map +1 → True (upvote), -1 → False (downvote)
        upvote = True if value > 0 else False
        vote, created = Vote.objects.update_or_create(
            profile=profile,
            voter=request.user.profile,
            defaults={'upvote': upvote}
        )

        # flash feedback
        verb = 'up-voted' if upvote else 'down-voted'
        if created:
            messages.success(request,
                             f"You’ve {verb} {profile.user.username}.")
        else:
            messages.info(request,
                          f"You changed your vote for {profile.user.username} to a {verb}.")
        return redirect('users:profile')
