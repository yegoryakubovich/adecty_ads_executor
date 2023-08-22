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
from admin_web.models import Session, Message, Sleep, SleepStates, SessionStates, SessionTask, SessionTaskStates, \
    SessionGroup, SessionGroupState, Personal, SessionPersonal, PersonalTypes


@admin.action(description="В work")
def to_in_work(model_admin: admin.ModelAdmin, request, queryset):
    for session in queryset:
        session.state = SessionStates.in_work
        session.save()


@admin.action(description="В free")
def to_free(model_admin: admin.ModelAdmin, request, queryset):
    for session in queryset:
        session.state = SessionStates.free
        session.save()


@admin.action(description="В wait")
def to_wait(model_admin: admin.ModelAdmin, request, queryset):
    for session in queryset:
        session.state = SessionStates.waiting
        session.save()


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

    def get_queryset(self, request):
        return super().get_queryset(request).filter(state=SessionTaskStates.enable).order_by("-id").all()


@admin.register(Session, site=admin_site)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "phone", "username", "name", "surname", "country", "shop", "state", "created",
        "message_send_now", "sleep_now", "work", "groups_count"
    )
    search_fields = ("id",)
    list_filter = ("state", "work")
    readonly_fields = ("id", "phone", "username", "tg_user_id", "created", "work")
    actions = [to_in_work, to_free, to_wait]
    inlines = [SessionTaskInline]
    list_per_page = max_rows

    @admin.display(description="Сообщений")
    def message_send_now(self, model: Session):
        return len(Message.objects.filter(session=model).all())

    @admin.display(description="Сон")
    def sleep_now(self, model: Session):
        sleep = Sleep.objects.filter(session=model, state=SleepStates.enable).first()
        if sleep:
            delta = (sleep.created + timedelta(seconds=sleep.time_second)).replace(tzinfo=None) - datetime.utcnow()
            return f"{delta}"
        return f"Нет"

    @admin.display(description="Групп")
    def groups_count(self, model: Session):
        groups = SessionGroup.objects.filter(session=model, state=SessionGroupState.active).all()
        if groups:
            return f"{len(groups)}"
        return f"0"

    @admin.display(description="Имя")
    def name(self, model: Session):
        sp = SessionPersonal.objects.filter(session=model, type=PersonalTypes.name).all()
        if sp:
            personal = Personal.objects.get(id=sp[0].personal_id)
            return personal.value
        return None

    @admin.display(description="Фамилия")
    def surname(self, model: Session):
        sp = SessionPersonal.objects.filter(session=model, type=PersonalTypes.surname).all()
        if sp:
            personal = Personal.objects.get(id=sp[0].personal_id)
            return personal.value
        return None
