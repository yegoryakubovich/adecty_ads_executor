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

from admin_web.admin import admin_site
from admin_web.models import Proxy, SessionProxy, ProxyStates


@admin.action(description="Активировать")
def state_to_active(model_admin: admin.ModelAdmin, request, queryset):
    for proxy in queryset:
        proxy.state = ProxyStates.enable
        proxy.save()


@admin.register(Proxy, site=admin_site)
class ProxyAdmin(admin.ModelAdmin):
    list_display = ("id", "country", "ip_port", "user", "password", "type", "state", "created", "session_count")
    list_filter = ("state", "type")
    readonly_fields = ("id", "created")
    actions = [state_to_active]
    list_per_page = 1000

    def has_add_permission(self, request):
        return False

    @admin.display(description="ip:port")
    def ip_port(self, model: Proxy):
        return f"{model.host}:{model.port}"

    @admin.display(description="Сессий")
    def session_count(self, model: Proxy):
        return f"{len(SessionProxy.objects.filter(proxy=model).all())}/{model.max_link}"
