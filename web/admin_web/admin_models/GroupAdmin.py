#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from datetime import datetime

from django.contrib import admin
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.http import HttpResponseRedirect
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from admin_web.admin import admin_site
from admin_web.admin_models import max_rows
from admin_web.models import Group, Message, MessageStates, SessionTask, GroupStates, SessionGroup, SessionGroupState
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


@admin.action(description="Активировать")
def state_to_active(model_admin: admin.ModelAdmin, request, queryset):
    for group in queryset:
        group.state = GroupStates.active
        group.save()


@admin.action(description="Проверить")
def state_to_waiting(model_admin: admin.ModelAdmin, request, queryset):
    for group in queryset:
        for task in SessionTask.objects.filter(group=group, state=SessionTaskStates.enable).all():
            task.delete()
        group.state = GroupStates.waiting
        group.save()


@admin.action(description="Выгрузить присутствие в группе")
def export_presence(model_admin: admin.ModelAdmin, request, queryset):
    all_data = [["ID", "Название", "Подписчиков", "Присутствие"]]
    for group in Group.objects.filter(state=GroupStates.active).all():
        messages_waiting = Message.objects.filter(group=group, state=MessageStates.waiting).all()
        if messages_waiting:
            all_data.append([group.id, f"@{group.name}", group.subscribers, "Да"])

    wb = Workbook()
    wb.remove(wb.active)
    ws: Worksheet = wb.create_sheet("Выгрузка")
    for data in all_data:
        ws.append(data)
    for column in ["A", "B", "C", "D", "E"]:
        if column in ["A"]:
            ws.column_dimensions[column].width = 5
        elif column in ["B"]:
            ws.column_dimensions[column].width = 40
        else:
            ws.column_dimensions[column].width = 20
    filename = f"media/exports/groups_{datetime.now().strftime('%y_%m_%d_%H_%M')}"
    wb.save(f"{filename}.xlsx")
    return HttpResponseRedirect(f"/{filename}.xlsx")


"""
MAIN
"""


@admin.register(Group, site=admin_site)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "state", "subscribers", "can_image", "type", "created",
        "delete_count", "presence", "abortively_percent", "sessions_count"
    )
    list_filter = ("state", "type", "created")
    search_fields = ("id",)
    readonly_fields = ("id", "created")
    inlines = [SessionTaskInline]
    actions = [state_to_inactive, state_to_active, state_to_waiting, export_presence]
    list_per_page = max_rows

    def has_add_permission(self, request):
        return False

    @admin.display(description="Актив/Бан")
    def sessions_count(self, model: Group):
        active = SessionGroup.objects.filter(group=model, state=SessionGroupState.active).all()
        banned = SessionGroup.objects.filter(group=model, state=SessionGroupState.banned).all()
        a = len(active) if active else 0
        b = len(banned) if banned else 0
        return f"{a}/{b}"


    @admin.display(description="Удалений")
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

    @admin.display(description="Вступления/Отправка")
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

    def changelist_view(self, request, extra_context=None):
        if 'action' in request.POST and request.POST['action'] == 'export_presence':
            if not request.POST.getlist(ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in Group.objects.all():
                    post.update({ACTION_CHECKBOX_NAME: str(u.id)})
                request._set_post(post)
        return super(GroupAdmin, self).changelist_view(request, extra_context)

    def get_action_choices(self, request, *args, **kwargs):  # auto select action
        choices = super(GroupAdmin, self).get_action_choices(request)
        choices.pop(0)
        choices.reverse()
        return choices
