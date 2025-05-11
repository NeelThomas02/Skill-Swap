from .models import Notification

def unread_notifications(request):
    if request.user.is_authenticated:
        qs = Notification.objects.filter(
            user=request.user, is_read=False
        ).order_by('-created')
        return {'unread_notifications': qs}
    return {}
