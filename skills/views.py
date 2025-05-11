# skills/views.py

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic, View
from users.models import Profile
from .models import Skill, Match
from django.urls import reverse
from django.contrib import messages
from notifications.models import Notification

# 1) List all skills
class SkillListView(generic.ListView):
    model = Skill
    template_name = 'skills/list.html'
    context_object_name = 'skills'

# 2) Skill detail & request logic
class SkillDetailView(LoginRequiredMixin, generic.DetailView):
    model = Skill
    template_name = 'skills/detail.html'
    context_object_name = 'skill'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user_profile = self.request.user.profile
        skill = self.object

        # all other profiles offering this skill
        holders = skill.holders.exclude(pk=user_profile.pk)
        ctx['holders'] = holders

        # whom I've already requested
        ctx['requested_helpers'] = Match.objects.filter(
            seeker=user_profile, skill=skill
        ).values_list('helper_id', flat=True)

        # mutual helpers
        outgoing = set(Match.objects.filter(seeker=user_profile)
                       .values_list('helper_id', flat=True))
        incoming = set(Match.objects.filter(helper=user_profile)
                       .values_list('seeker_id', flat=True))
        ctx['mutual_helpers'] = outgoing.intersection(incoming)

        return ctx

class RequestMatchView(LoginRequiredMixin, View):
    def post(self, request, pk, helper_pk):
        profile = request.user.profile
        skill   = get_object_or_404(Skill, pk=pk)
        helper  = get_object_or_404(Profile, pk=helper_pk)
        match, created = Match.objects.get_or_create(
            seeker=profile, helper=helper, skill=skill
        )
        if created:
            Notification.objects.create(
                user=helper.user,
                message=f"{request.user.username} requested your help on “{skill.name}”."
            )
            messages.success(request,
                             f"You’ve requested help from {helper.user.username}!")
        else:
            messages.info(request,
                          f"You’d already requested help from {helper.user.username}.")
        return redirect('skills:detail', pk=pk)

# 3) List only mutual matches
class MutualMatchesView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'skills/mutual_matches.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        profile = self.request.user.profile

        out_ids = set(Match.objects.filter(seeker=profile)
                      .values_list('helper_id', flat=True))
        in_ids  = set(Match.objects.filter(helper=profile)
                      .values_list('seeker_id', flat=True))
        mutual_ids = out_ids.intersection(in_ids)

        ctx['mutual_matches'] = Match.objects.filter(
            seeker=profile,
            helper_id__in=mutual_ids
        ).select_related('helper', 'skill')
        return ctx
