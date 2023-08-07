from django.contrib import admin

from admin_web.admin import admin_site
from admin_web.models import Shop, Session, Proxy


@admin.register(Shop, site=admin_site)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "link", "created", "session_count", "proxy_count")
    readonly_fields = ("id", "created")
    list_per_page = 1000

    # search_fields = ()
    # list_editable = ()

    def has_add_permission(self, request):
        return False

    @admin.display(description="Сессий")
    def session_count(self, model: Shop):
        return str(len(Session.objects.filter(shop=model).all()))

    @admin.display(description="Прокси")
    def proxy_count(self, model: Shop):
        return str(len(Proxy.objects.filter(shop=model).all()))
