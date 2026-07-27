from rest_framework import serializers
from .models import ShortenerURL, ClickLog

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
    
    
class ClickLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClickLog
        fields = ("ip_address", "user_agent", "created_at")
        
        
class ShortenerURLAnalyticsSerializer(serializers.ModelSerializer):
    recent_clicks = serializers.SerializerMethodField()
    
    class Meta:
        model = ShortenerURL
        fields = ("short_code", "original_url", "clicks_count", "created_at", "recent_clicks")
        
    def get_recent_clicks(self, obj):
        recent = obj.clicks.all()[:10]
        return ClickLogSerializer(recent, many=True).data