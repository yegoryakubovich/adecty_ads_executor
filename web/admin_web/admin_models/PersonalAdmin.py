from django.contrib import admin

from admin_web.admin import admin_site
from admin_web.models import Shop, Session, Proxy, Personal


@admin.register(Personal, site=admin_site)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "value", "created")
    list_filter = ("type", "created")
    readonly_fields = ("id", "created")
    list_per_page = 1000

