from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View, generic
from .models import Message
from .forms import MessageForm
from users.models import Profile
from skills.models import Match
from notifications.models import Notification

class ChatListView(LoginRequiredMixin, generic.ListView):
    template_name = 'chat/list.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        me = self.request.user.profile
        # mutual matches just like before
        out_ids = set(Match.objects.filter(seeker=me).values_list('helper_id', flat=True))
        in_ids  = set(Match.objects.filter(helper=me).values_list('seeker_id', flat=True))
        mutual_ids = out_ids.intersection(in_ids)
        return Profile.objects.filter(pk__in=mutual_ids)

class ChatDetailView(LoginRequiredMixin, View):
    template_name = 'chat/detail.html'

    def get(self, request, pk):
        me    = request.user.profile
        other = get_object_or_404(Profile, pk=pk)
        # mark all new‐message notifications from this chat as read
        Notification.objects.filter(
            user=request.user,
            message__contains="sent you a message",
            message__startswith=f"{other.user.username}",
            is_read=False
        ).update(is_read=True)
        # ensure mutual match
        if not (Match.objects.filter(seeker=me, helper=other).exists() and
                Match.objects.filter(seeker=other, helper=me).exists()):
            return redirect('chat:list')

        chat_messages = Message.objects.filter(
            sender__in=[me, other],
            receiver__in=[me, other]
        ).order_by('timestamp')

        form = MessageForm()
        return render(request, self.template_name, {
           'other': other,
           'chat_messages': chat_messages,
           'form': form,
       })

    def post(self, request, pk):
        me    = request.user.profile
        other = get_object_or_404(Profile, pk=pk)
        form  = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender   = me
            msg.receiver = other
            msg.save()
            # Notify the other user
            Notification.objects.create(
                user=other.user,
                message=(
                    f"{request.user.username} sent you a message: "
                    f"“{msg.text[:50]}{('...' if len(msg.text)>50 else '')}”"
            )
            )
            return redirect('chat:detail', pk=pk)

        # on error, re-render with existing messages
        chat_messages = Message.objects.filter(
            sender__in=[me, other],
            receiver__in=[me, other]
        ).order_by('timestamp')
        return render(request, self.template_name, {
           'other': other,
           'chat_messages': chat_messages,
           'form': form,
       })
