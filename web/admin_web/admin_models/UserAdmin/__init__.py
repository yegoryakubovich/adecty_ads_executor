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
from admin_web.models import User
from .actions import actions_list
from ..MessageAdmin.inlines import MessageInline
from ..OrderUserAdmin.inlines import OrderUserInline
from ..SessionTaskAdmin.inlines import SessionTaskInline


@admin.register(User, site=admin_site)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "tg_user_id", "username", "first_name", "last_name", "created")
    search_fields = ("id",)
    list_filter = ("created",)
    readonly_fields = ("id", "created")
    actions = actions_list
    inlines = [SessionTaskInline, MessageInline, OrderUserInline]
    list_per_page = max_rows

    def get_action_choices(self, request, *args, **kwargs):  # auto select action
        choices = super(UserAdmin, self).get_action_choices(request)
        choices.pop(0)
        choices.reverse()
        return choices
