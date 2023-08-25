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
from admin_web.admin_models.MessageAdmin.inlines import MessageInline
from admin_web.admin_models.OrderGroupAdmin.inlines import OrderGroupInline
from admin_web.admin_models.OrderPersonalAdmin.inlines import OrderPersonalInline
from admin_web.admin_models.OrderUserAdmin.inlines import OrderUserInline
from admin_web.admin_models.SessionOrderAdmin.inlines import SessionOrderInline
from admin_web.admin_models.SessionTaskAdmin.inlines import SessionTaskInline
from admin_web.models import Order


@admin.register(Order, site=admin_site)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "state", "type", "datetime_stop", "created")
    search_fields = ("id",)
    list_filter = ("state", "type", "created")
    readonly_fields = ("id", "created")
    inlines = [
        SessionTaskInline, MessageInline, SessionOrderInline, OrderGroupInline, OrderPersonalInline, OrderUserInline
    ]
    list_per_page = max_rows
