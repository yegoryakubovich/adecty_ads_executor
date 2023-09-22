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

from admin_web.models import ProxyStates


@admin.action(description="Активировать")
def state_to_active(model_admin: admin.ModelAdmin, request, queryset):
    for proxy in queryset:
        proxy.state = ProxyStates.enable
        proxy.save()


@admin.action(description="Стоп")
def state_to_stop(model_admin: admin.ModelAdmin, request, queryset):
    for proxy in queryset:
        proxy.state = ProxyStates.stop
        proxy.save()


@admin.action(description="Диактивировать")
def state_to_disable(model_admin: admin.ModelAdmin, request, queryset):
    for proxy in queryset:
        proxy.state = ProxyStates.disable
        proxy.save()


@admin.action(description="Ожидание")
def state_to_wait(model_admin: admin.ModelAdmin, request, queryset):
    for proxy in queryset:
        proxy.state = ProxyStates.wait
        proxy.save()


actions_list = [state_to_active, state_to_disable, state_to_wait, state_to_stop]
