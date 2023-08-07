from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from admin_web.admin import admin_site

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('', admin_site.urls),
]
