from django.db import models
import random
import string 


def generate_short_code():
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=6))

class ShortenerURL(models.Model):
    original_url = models.URLField(verbose_name="Original Link")
    short_code = models.CharField(
        max_length=10,
        unique=True,
        default=generate_short_code,
        verbose_name="Short code"
    )
    clicks_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Count of transitions"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date of creation"
    )
    
    class Meta:
        verbose_name = "Shorted link"
        verbose_name_plural = "Shrotener link"
        ordering = ["-created_at"]
        
    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"
    
    
class ClickLog(models.Model):
    url = models.ForeignKey(
        ShortenerURL,
        on_delete=models.CASCADE,
        related_name="clicks",
        verbose_name="Link"
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Ip adress"
    )
    user_agent = models.TextField(
        null=True,
        blank=True,
        verbose_name = "User-Agent"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Time of transition"
    )
    
    class Meta:
        verbose_name = "Log of transition"
        verbose_name_plural = "Logs of transitions"
        ordering = ["-created_at"]
        
    def __str__(self):
        return f"Click to {self.url.short_code} ({self.created_at.strftime('%d.%m.%Y %H:%M')})"