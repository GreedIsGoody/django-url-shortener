from celery import shared_task
from django.utils import timezone 
from .models import ShortenerURL

@shared_task
def purge_expired_links_task():
    now = timezone.now()
    expired_links = ShortenerURL.objects.filter(expires_at__lt=now)
    count, _ = expired_links.delete()
    
    return f"Purged {count} expired links at {now}"