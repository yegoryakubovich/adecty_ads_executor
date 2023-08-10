from django.contrib import admin
from django.http import HttpResponseRedirect

from admin_web.admin import admin_site
from admin_web.models import User


@admin.action(description="Выбрать для рассылки")
def select_from_mailing(model_admin: admin.ModelAdmin, request, queryset):
    users = ','.join([str(user.id) for user in queryset])
    return HttpResponseRedirect(f"/mailing_users?users={users}")



@admin.register(User, site=admin_site)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "tg_user_id", "username", "first_name", "last_name", "created")
    list_filter = ("created",)
    readonly_fields = ("id", "created")
    actions = [select_from_mailing]

    list_per_page = 1000

    def has_add_permission(self, request):
        return False

    def get_action_choices(self, request, *args, **kwargs):  # auto select action
        choices = super(UserAdmin, self).get_action_choices(request)
        choices.pop(0)
        choices.reverse()
        return choices
