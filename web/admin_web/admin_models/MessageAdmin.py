from django.contrib import admin

from admin_web.admin import admin_site
from admin_web.models import Message


@admin.register(Message, site=admin_site)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "order", "group", "state", "message_id", "text", "created")
    list_filter = ("state", "created")
    readonly_fields = ("id", "created")
    list_per_page = 1000

    # search_fields = ()
    # list_editable = ()

    def has_add_permission(self, request):
        return False

    @admin.display(description="Сообщений")
    def message_send_now(self, model: Message):
        return "0"
