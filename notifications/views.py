from django.views import View
from django.shortcuts import redirect

class MarkAllReadView(View):
    def get(self, request):
        request.user.notifications.filter(is_read=False).update(is_read=True)
        return redirect(request.META.get('HTTP_REFERER', '/'))
