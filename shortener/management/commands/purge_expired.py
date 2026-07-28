from django.core.management.base import BaseCommand
from django.utils import timezone
from shortener.models import ShortenerURL

class Command(BaseCommand):
    help = "Deleting all short_links what was expired"
    
    def handle(self, *args, **kwargs):
        now = timezone.now()
        
        #Found all expired links
        expired_links = ShortenerURL.objects.filter(
            expires_at__isnull = False,
            expires_at__lte = now
        )
        
        #counter of this links
        count = expired_links.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS("Expired links were not found"))
            return
        
        expired_links.delete()
        
        self.stdout.write(
            self.style.SUCCESS(f"Successfully deleting a expired links: {count}")
        )
        
        