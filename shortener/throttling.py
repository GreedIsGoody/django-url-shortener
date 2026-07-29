from rest_framework.throttling import AnonRateThrottle

class CreateLinkRateThrottle(AnonRateThrottle):
    scope = 'burst_create'
    
    