from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .models import ShortenerURL, ClickLog
from .serializer import ShortenURLCreateSerializer, ShortenerURLResponseSerializer

class ShortenURLAPIView(APIView):
    @extend_schema(
        request=ShortenURLCreateSerializer,
        responses={201: ShortenerURLResponseSerializer}
    )
    def post(self, request):
        serializer = ShortenURLCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        link= serializer.save()
        
        response_serializer = ShortenerURLResponseSerializer(link, context={"request": request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
        
    return ip

def redirect_to_original(request, short_code):
    link = get_object_or_404(ShortenerURL, short_code=short_code)
    
    link.clicks_count += 1
    link.save(update_fields=["clicks_count"])
    
    ClickLog.objects.create(
        url=link,
        ip_address=get_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", "")
    )
    
    return redirect(link.original_url)