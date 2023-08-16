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
from admin_web.models import Sleep, SleepStates


@admin.register(Sleep, site=admin_site)
class SleepAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "time_second", "state", "created", "sleep_now")
    list_filter = ("state", "created")
    readonly_fields = ("id", "created")
    list_per_page = 1000

    def has_add_permission(self, request):
        return False

    @admin.display(description="Осталось сна")
    def sleep_now(self, model: Sleep):
        if model.state == SleepStates.enable:
            delta = (model.created + timedelta(seconds=model.time_second)).replace(tzinfo=None) - datetime.utcnow()
            return f"{delta}"
        return f"Нет"