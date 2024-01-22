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
from django.contrib import admin
from django.http import HttpResponseRedirect

from admin_web.models import SessionStates, SessionGroup, SessionOrder, Sleep, SessionTask, SessionProxy, \
    SessionPersonal
from .views import LinkedSessionOrderURL


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


@admin.action(description="В kicked")
def to_kicked(model_admin: admin.ModelAdmin, request, queryset):
    for session in queryset:
        for sgroup in SessionGroup.objects.all(session=session):
            sgroup.delete()
        for sorder in SessionOrder.objects.all(session=session):
            sorder.delete()
        for spersonal in SessionPersonal.objects.all(session=session):
            spersonal.delete()
        for sproxy in SessionProxy.objects.all(session=session):
            sproxy.delete()
        for stask in SessionTask.objects.all(session=session):
            stask.delete()
        for sleep in Sleep.objects.all(session=session):
            sleep.delete()
        session.state = SessionStates.kicked
        session.save()


@admin.action(description="Связать с заказом")
def select_link_order(model_admin: admin.ModelAdmin, request, queryset):
    sessions = ','.join([str(session.id) for session in queryset])
    return HttpResponseRedirect(f"/{LinkedSessionOrderURL}?sessions={sessions}")


actions_list = [select_link_order, to_in_work, to_free, to_kicked, to_wait]
