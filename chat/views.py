# chat/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db.models import Q
from .models import Message

class ChatListView(LoginRequiredMixin, generic.ListView):
    model = Message
    template_name = 'chat/list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        # Show only messages involving the current user’s profile
        user_profile = self.request.user.profile
        return Message.objects.filter(
            Q(sender=user_profile) | Q(receiver=user_profile)
        ).order_by('timestamp')
