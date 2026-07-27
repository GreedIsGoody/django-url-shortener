from django.urls import path 
from . import views  


urlpatterns = [
    path('api/shorten/', views.ShortenURLAPIView.as_view(), name='create_short_url'),
    path('api/analytics/<str:short_code>', views.ShortenerURLAnalyticsAPIView.as_view(), name='url_analytics'),
    path('r/<str:short_code>/', views.redirect_to_original, name='redirect_to_original'),
]