from rest_framework import serializers
from .models import ShortenerURL, ClickLog
from django.utils import timezone
import re

class ShortenURLCreateSerializer(serializers.ModelSerializer):
    
    #Optional fields for our json
    custom_code = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=15,
        help_text = "Your custom code"
    )
    
    expires_at = serializers.DateTimeField(
        required=False,
        allow_null=True,
        help_text="Date and time of ending of link"
    )
    
    class Meta:
        model = ShortenerURL
        fields = ("original_url", "custom_code", "expires_at")
        
    def validate_custom_code(self,value):
        
        if not value:
            return value 
        
        if not re.match(r"[a-zA-Z0-9_-]+$", value):
            raise serializers.ValidationError("Code can consists only chatacters,digits - and _")
        
        if ShortenerURL.objects.filter(short_code=value).exists():
            raise serializers.ValidationError("This custom code already used")
        
        return value
    
    def validate_expires_at(self, value):
        if value and value <= timezone.now():
            raise serializers.ValidationError("Date of expiring need to be in the future")
        return value
    
    def create(self, validated_data):
        #Logic of saving link to db
        custom_code = validated_data.pop("custom_code", None)
        
        if custom_code:
            validated_data["short_code"] = custom_code
            
        return super().create(validated_data)
        
        
        
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
        fields = ['ip_address', 'browser', 'os', 'device_type', 'created_at']
        
        
class ShortenerURLAnalyticsSerializer(serializers.ModelSerializer):
    recent_clicks = serializers.SerializerMethodField()
    
    class Meta:
        model = ShortenerURL
        fields = ("short_code", "original_url", "clicks_count", "created_at", "recent_clicks")
        
    def get_recent_clicks(self, obj):
        recent = obj.clicks.all()[:10]
        return ClickLogSerializer(recent, many=True).data