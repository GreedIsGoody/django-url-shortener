from django.contrib import admin
from .models import ShortenerURL, ClickLog


class ClickLogInline(admin.TabularInline):
    model = ClickLog
    extra = 0
    readonly_fields = ("ip_address", "user_agent", "created_at")

@admin.register(ShortenerURL)
class ShortenerURLAdmin(admin.ModelAdmin):
    
    #Fields what will display in table
    list_display = ("short_code", "original_url", "clicks_count", "created_at")
    
    
    #Search fields
    search_fields = ("short_code", "original_url")
    
    #Filters to the fields
    list_filter = ("created_at",)
    
    #Only for reading fields
    readonly_fields = ("clicks_count", "created_at")

@admin.register(ClickLog)
class ClickLogAdmin(admin.ModelAdmin):
    list_display = ("url", "ip_address", "created_at")
    list_filter = ("created_at",)
    readonly_fields = ("url", "ip_address", "user_agent", "created_at")