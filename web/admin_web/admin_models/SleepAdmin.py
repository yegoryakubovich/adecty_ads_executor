from datetime import timedelta, datetime

from django.contrib import admin

from admin_web.admin import admin_site
from admin_web.models import Sleep, SleepStates


@admin.register(Sleep, site=admin_site)
class SleepAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "time_second", "state", "created", "sleep_now")
    list_filter = ("state", "created")
    readonly_fields = ("id", "created")
    list_per_page = 1000

    # search_fields = ()
    # list_editable = ()

    def has_add_permission(self, request):
        return False

    @admin.display(description="Осталось сна")
    def sleep_now(self, model: Sleep):
        if model.state == SleepStates.enable:
            delta = (model.created + timedelta(seconds=model.time_second)).replace(tzinfo=None) - datetime.utcnow()
            return f"{delta}"
        return f"Нет"
