from django.contrib import admin

from admin_web.admin import admin_site
from admin_web.models import SessionProxy


@admin.register(SessionProxy, site=admin_site)
class SessionProxyAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "proxy", "created")
    readonly_fields = ("id", "created")
    list_per_page = 1000

    # search_fields = ()
    # list_editable = ()

    def has_add_permission(self, request):
        return False
