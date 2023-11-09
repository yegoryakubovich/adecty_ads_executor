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
from admin_web.admin_models import max_rows
from admin_web.models import Setting


@admin.register(Setting, site=admin_site)
class SettingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "key", "type", "value", "created")
    list_filter = ("type",)
    search_fields = ("id", "name", "key")
    readonly_fields = ("id", "created")
    list_per_page = max_rows
