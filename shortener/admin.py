from django.contrib import admin
from .models import ShortenerURL


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