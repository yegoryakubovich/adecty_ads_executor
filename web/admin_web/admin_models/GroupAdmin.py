from django.contrib import admin

from admin_web.admin import admin_site
from admin_web.models import Group, Message, MessageStates, SessionTask, GroupStates
from admin_web.models.session_task import SessionTaskStates, SessionTaskType


class PresenceState:
    yes = "Да"
    no = "Нет"
    wait = "План"


"""
INLINE
"""


class SessionTaskInline(admin.TabularInline):
    model = SessionTask
    extra = 0
    fields = ("id", "session", "group", "order", "message", "type", "state", "state_description")

    show_change_link = False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


"""
ACTIONS
"""


@admin.action(description="Диактивировать")
def state_to_inactive(model_admin: admin.ModelAdmin, request, queryset):
    for group in queryset:
        group.state = GroupStates.inactive
        group.save()


"""
MAIN
"""


@admin.register(Group, site=admin_site)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "state", "subscribers", "created", "delete_count", "presence", "abortively_percent")
    list_filter = ("state",)
    readonly_fields = ("id", "created")
    inlines = [SessionTaskInline]
    actions = [state_to_inactive]

    list_per_page = 1000

    def has_add_permission(self, request):
        return False

    @admin.display(description="Удаленных сообщений")
    def delete_count(self, model: Group):
        messages_count = len(Message.objects.filter(group=model).all())
        delete_count = len(Message.objects.filter(group=model, state=MessageStates.deleted).all())
        return f"{delete_count}/{messages_count}"

    @admin.display(description="Присутствия")
    def presence(self, model: Group):
        messages_waiting = Message.objects.filter(group=model, state=MessageStates.waiting).all()
        if messages_waiting:
            return PresenceState.yes
        task_send_by_order = SessionTask.objects.filter(
            group=model, state=SessionTaskStates.enable, type=SessionTaskType.send_by_order
        ).all()
        if task_send_by_order:
            return PresenceState.wait
        return PresenceState.no

    @admin.display(description="Вступления | Отправка")
    def abortively_percent(self, model: Group):
        len_abortively_join = len(SessionTask.objects.filter(
            group=model, state=SessionTaskStates.abortively, type=SessionTaskType.join_group
        ).all())
        len_finished_join = len(SessionTask.objects.filter(
            group=model, state=SessionTaskStates.finished, type=SessionTaskType.join_group
        ).all())
        len_all_join = len_abortively_join + len_finished_join

        len_abortively_send = len(SessionTask.objects.filter(
            group=model, state=SessionTaskStates.abortively, type=SessionTaskType.send_by_order
        ).all())
        len_finished_send = len(SessionTask.objects.filter(
            group=model, state=SessionTaskStates.finished, type=SessionTaskType.send_by_order
        ).all())
        len_all_send = len_abortively_send + len_finished_send

        if len_all_join == 0 or len_all_send == 0:
            return f"0%"

        math_join = round(len_abortively_join / len_all_join * 100, 2)
        math_send = round(len_abortively_send / len_all_send * 100, 2)

        return f"{math_join}% | {math_send}%"

    def get_action_choices(self, request, *args, **kwargs):  # auto select action
        choices = super(GroupAdmin, self).get_action_choices(request)
        choices.pop(0)
        choices.reverse()
        return choices
