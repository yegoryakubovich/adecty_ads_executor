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
from django.http import HttpResponseRedirect
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from admin_web.admin_models.GroupAdmin.views import LinkedGroupOrderURL
from admin_web.models import Group, Message, MessageStates, GroupStates, SessionTask, SessionTaskStates, GroupType


@admin.action(description="Диактивировать")
def state_to_inactive(model_admin: admin.ModelAdmin, request, queryset):
    for group in queryset:
        for task in SessionTask.objects.filter(group=group, state=SessionTaskStates.enable).all():
            task.delete()
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
        group.can_image = True
        group.type = GroupType.link
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


@admin.action(description="Связать с заказом")
def select_link_order(model_admin: admin.ModelAdmin, request, queryset):
    groups = ','.join([str(group.id) for group in queryset])
    return HttpResponseRedirect(f"/{LinkedGroupOrderURL}?groups={groups}")


actions_list = [select_link_order, state_to_inactive, state_to_active, state_to_waiting, export_presence]
