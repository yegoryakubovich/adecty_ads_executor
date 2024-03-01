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


from datetime import timedelta, datetime

from django.contrib import admin

from admin_web.admin import admin_site
from admin_web.admin_models import max_rows
from admin_web.admin_models.SessionTaskAdmin.inlines import SessionTaskInline
from admin_web.models import Session, Message, Sleep, SleepStates, SessionGroup, SessionGroupState, Personal, \
    SessionPersonal, PersonalTypes, SessionTask, SessionTaskStates, SessionTaskType, SessionOrder, \
    OrderGroup
from .actions import actions_list
from ..MessageAdmin.inlines import MessageInline
from ..SessionDeviceAdmin.inlines import SessionDeviceInline
from ..SessionGroupAdmin.inlines import SessionGroupInline
from ..SessionOrderAdmin.inlines import SessionOrderInline
from ..SessionPersonalAdmin.inlines import SessionPersonalInline
from ..SessionProxyAdmin.inlines import SessionProxyInline


@admin.register(Session, site=admin_site)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "work", "phone", "fio", "state", "order", "date", "message_send_now", "message_send_day", "sleep_now",
        "groups_count", "tasks_count", "message_tasks_count"
    )
    search_fields = ("id",)
    list_filter = ("state", "work", "created")
    readonly_fields = ("id", "phone", "username", "tg_user_id", "created", "work")
    actions = actions_list
    inlines = [
        SessionTaskInline, MessageInline, SessionGroupInline, SessionOrderInline, SessionProxyInline,
        SessionPersonalInline, SessionDeviceInline
    ]
    list_per_page = max_rows

    def get_action_choices(self, request, *args, **kwargs):  # auto select action
        choices = super(SessionAdmin, self).get_action_choices(request)
        choices.pop(0)
        choices.reverse()
        return choices

    @admin.display(description="ФИО")
    def fio(self, model: Session):
        sp_name = SessionPersonal.objects.filter(session=model, type=PersonalTypes.name).all()
        sp_surname = SessionPersonal.objects.filter(session=model, type=PersonalTypes.surname).all()

        name = Personal.objects.get(id=sp_name[0].personal_id).value if sp_name else ""
        surname = Personal.objects.get(id=sp_surname[0].personal_id).value if sp_surname else ""
        return f"{surname} {name}"

    @admin.display(description="Заказ")
    def order(self, model: Session):
        so = SessionOrder.objects.filter(session=model).all()
        if not so:
            return "Нет"
        return so[0].order.name

    @admin.display(description="Дата")
    def date(self, model: Session):
        return model.created.strftime("%d.%m.%y")

    @admin.display(description="Всего")
    def message_send_now(self, model: Session):
        return len(Message.objects.filter(session=model).all())

    @admin.display(description="Сегодня")
    def message_send_day(self, model: Session):
        msg_all = []
        for msg in Message.objects.filter(session=model).all():
            if msg.created.timestamp() < (datetime.utcnow() - timedelta(hours=24)).timestamp():
                continue
            msg_all.append(msg)
        return len(msg_all)

    @admin.display(description="Сон")
    def sleep_now(self, model: Session):
        sleep = Sleep.objects.filter(session=model, state=SleepStates.enable).first()
        if sleep:
            delta = str((sleep.created + timedelta(seconds=sleep.time_second)).replace(tzinfo=None) - datetime.utcnow())
            return delta[:delta.index('.')]
        return f"Нет"

    @admin.display(description="Групп")
    def groups_count(self, model: Session):
        groups = SessionGroup.objects.filter(session=model, state=SessionGroupState.active).all()
        groups_ban = SessionGroup.objects.filter(session=model, state=SessionGroupState.banned).all()
        return f"{len(groups)}/{len(groups_ban)}"

    @admin.display(description="Задач")
    def tasks_count(self, model: Session):
        tasks = SessionTask.objects.filter(session=model, state=SessionTaskStates.enable).all()
        tasks_check_message = SessionTask.objects.filter(
            session=model, state=SessionTaskStates.enable, type=SessionTaskType.check_message
        ).all()
        result = len(tasks) - len(tasks_check_message)
        if result:
            return f"{result}"
        return f"0"

    @admin.display(description="Проверок")
    def message_tasks_count(self, model: Session):
        tasks_check_message = SessionTask.objects.filter(
            session=model, state=SessionTaskStates.enable, type=SessionTaskType.check_message
        ).all()
        if tasks_check_message:
            return f"{len(tasks_check_message)}"
        return f"0"
