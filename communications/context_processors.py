from .models import DirectMessage


def communications_unread(request):
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return {"chat_unread_count": 0}
    return {
        "chat_unread_count": DirectMessage.objects.filter(
            recipient=request.user,
            read_at__isnull=True,
        ).count()
    }
