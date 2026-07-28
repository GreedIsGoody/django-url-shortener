from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .models import ShortenerURL, ClickLog
from .serializer import (ShortenURLCreateSerializer, ShortenerURLResponseSerializer, ShortenerURLAnalyticsSerializer)
from django.http import Http404

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
    
    #Checking if link is expired
    if link.is_expired():
        raise Http404("Validity period")
    
    #Earn ip address
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    #Earn User-Agent
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    
    #Creating a click log
    ClickLog.objects.create(
        url = link,
        ip_address=ip,
        user_agent=user_agent
    )
    link.clicks_count += 1
    link.save(update_fields=["clicks_count"])
    
    return redirect(link.original_url)

class ShortenerURLAnalyticsAPIView(APIView):
    # receiving API endpoint for analytics of trasition by link 
    @extend_schema(
        responses={200: ShortenerURLAnalyticsSerializer},
        summary="Receive analytic about click by short code"
    )
    def get(self, request, short_code):
        link = get_object_or_404(ShortenerURL, short_code=short_code)
        serializer = ShortenerURLAnalyticsSerializer(link)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ShortenerURLDeleteAPIView(APIView):
    @extend_schema(
        responses={
            204: None,
            404: {"description" : "Link was not found"}
        },
        summary="Delete short link by code"
    )
    
    def delete(self, request,short_code):
        link  = get_object_or_404(ShortenerURL, short_code=short_code)
        link.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

