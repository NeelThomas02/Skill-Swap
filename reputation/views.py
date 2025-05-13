from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Vote
from users.models import Profile

class VoteView(LoginRequiredMixin, View):
    def post(self, request):
        profile_id = request.POST.get('profile_id')
        value      = int(request.POST.get('value'))
        profile    = get_object_or_404(Profile, pk=profile_id)
        voter_prof = request.user.profile

        # Prevent self‐voting
        if profile.user == request.user:
            msg = "You cannot vote on your own profile."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': msg}, status=400)
            messages.error(request, msg)
            return redirect(request.META.get('HTTP_REFERER','/'))

        # Determine current vote (if any)
        try:
            vote = Vote.objects.get(profile=profile, voter=voter_prof)
        except Vote.DoesNotExist:
            vote = None

        # Undo?
        if value == 0:
            if vote:
                vote.delete()
                acted = 'undone'
            else:
                acted = 'none'
        else:
            is_up = (value == 1)
            if vote is None:
                Vote.objects.create(profile=profile, voter=voter_prof, upvote=is_up)
                acted = 'created'
            else:
                if vote.upvote == is_up:
                    vote.delete()
                    acted = 'undone'
                else:
                    vote.upvote = is_up
                    vote.save()
                    acted = 'changed'

        # Recalculate score & has_voted
        votes = profile.votes.all()
        up    = votes.filter(upvote=True).count()
        down  = votes.filter(upvote=False).count()
        score = up - down
        has_voted = Vote.objects.filter(profile=profile, voter=voter_prof).exists()

        # If AJAX, return JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'score': score,
                'has_voted': has_voted,
                'acted': acted,
            })

        # Otherwise fallback to redirect
        return redirect(request.META.get('HTTP_REFERER',
                                         f"/users/profile/{profile.pk}/"))
