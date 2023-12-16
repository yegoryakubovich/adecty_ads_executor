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
from datetime import datetime, timedelta

from django.contrib import admin
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME

from admin_web.admin import admin_site
from admin_web.admin_models import max_rows
from admin_web.models import Group, Message, MessageStates, SessionGroup, SessionGroupState, OrderGroup
from .actions import actions_list
from ..GroupCountryAdmin.inlines import GroupCountryInline
from ..MessageAdmin.inlines import MessageInline
from ..OrderGroupAdmin.inlines import OrderGroupInline
from ..SessionGroupAdmin.inlines import SessionGroupInline
from ..SessionTaskAdmin.inlines import SessionTaskInline

@admin.register(Group, site=admin_site)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "state", "subscribers", "can_image", "type", "join_request", "captcha_have", "captcha_type",
        "date", "delete_count", "delete_count_today", "orders_group", "sessions_count"
    )
    list_filter = ("state", "can_image", "type", "join_request", "captcha_have", "captcha_type")
    search_fields = ("id",)
    readonly_fields = ("id", "created")
    actions = actions_list
    inlines = [SessionTaskInline, MessageInline, SessionGroupInline, GroupCountryInline, OrderGroupInline]
    list_per_page = max_rows

    @admin.display(description="Актив/Бан")
    def sessions_count(self, model: Group):
        active = SessionGroup.objects.filter(group=model, state=SessionGroupState.active).all()
        banned = SessionGroup.objects.filter(group=model, state=SessionGroupState.banned).all()
        a = len(active) if active else 0
        b = len(banned) if banned else 0
        return f"{a}/{b}"

    @admin.display(description="Дата")
    def date(self, model: Group):
        return model.created.strftime("%d.%m.%y")

    @admin.display(description="Удалений")
    def delete_count(self, model: Group):
        messages_count = len(Message.objects.filter(group=model).all())
        delete_count = len(Message.objects.filter(group=model, state=MessageStates.deleted).all())
        return f"{delete_count}/{messages_count}"

    @admin.display(description="Сегодня")
    def delete_count_today(self, model: Group):
        messages_count = 0
        delete_count = 0
        for msg in Message.objects.filter(group=model).all():
            if msg.state == MessageStates.to_user:
                continue
            if msg.created.timestamp() < (datetime.utcnow() - timedelta(hours=24)).timestamp():
                continue
            messages_count += 1
            if msg.state == MessageStates.deleted:
                delete_count += 1
        return f"{delete_count}/{messages_count}"

    @admin.display(description="Заказы")
    def orders_group(self, model: Group):
        return "\n".join([og.order.name for og in OrderGroup.objects.filter(group=model).all()])

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
