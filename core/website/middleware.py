from ipware import get_client_ip
from django.utils.translation import activate
from django.core.cache import cache
import requests

class IPBaseLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, is_routable = get_client_ip(request)

        if ip:
            is_iranian = cache.get(ip)
            if is_iranian is None:
                is_iranian = self.is_ip_from_iran(ip)
                cache.set(ip, is_iranian, 3600)
            if is_iranian:
                activate('en')
            else:
                activate('fa')
        response = self.get_response(request)
        
        return response
    def is_ip_from_iran(self, ip):
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        if response.status_code == 200:
            country = response.json().get('country')
            return country == 'IR'
        return False
