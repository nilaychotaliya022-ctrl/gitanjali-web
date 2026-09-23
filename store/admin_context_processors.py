from django.contrib.auth import get_user_model
from .models import Review


ADMIN_URL_PREFIX = "/gitanjali-management/"


def admin_stats(request):
    if request.path.startswith(ADMIN_URL_PREFIX) and request.user.is_staff:
        return {
            "g_review_count": Review.objects.count(),
            "g_user_count": get_user_model().objects.count(),
        }
    return {}