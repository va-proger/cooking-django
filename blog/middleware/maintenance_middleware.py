from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from blog.models import SiteSettings


class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        settings = SiteSettings.get_solo()

        if settings.maintenance_mode:
            if not request.user.is_authenticated or not request.user.is_staff:
                return HttpResponseForbidden("Сайт на техническом обслуживании")

        return self.get_response(request)