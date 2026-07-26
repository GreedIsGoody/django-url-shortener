from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ShortenerURL


@csrf_exempt
def create_short_url(request):
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            original_url = data.get("url")
            
            if not original_url:
                return JsonResponse({"error": "URL is required"}, status=400)
            
            link = ShortenerURL.objects.create(original_url=original_url)
            
            short_url = request.build_absolute_uri(f"/r/{link.short_code}")
            
            return JsonResponse({
                "short_code": link.short_code,
                "short_url" : short_url,
                "original_url": link.original_url
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
    return HttpResponseBadRequest("Only POST request are allowed")

def redirect_to_original(request, short_code):
    link = get_object_or_404(ShortenerURL, short_code=short_code)
    
    link.clicks_count += 1
    link.save(update_fields=["clicks_count"])
    
    return redirect(link.original_url)