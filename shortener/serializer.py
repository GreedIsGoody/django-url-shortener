from rest_framework import serializers
from .models import ShortenerURL

class ShortenURLCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenerURL
        fields = ("original_url",)
        
        
class ShortenerURLResponseSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ShortenerURL
        fields = ("id", "short_code", "short_url", "original_url", "clicks_count", "created_at")
    
    def get_short_url(self, obj) -> str:
        request = self.context.get("request")
        
        if request:
            return request.build_absolute_uri(f"/r/{obj.short_code}/")
        return f"/r/{obj.short_code}"