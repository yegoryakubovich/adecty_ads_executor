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

from admin_web.admin_models.UserAdmin.views import MailingUsersURL


@admin.action(description="Выбрать для рассылки")
def select_from_mailing(model_admin: admin.ModelAdmin, request, queryset):
    users = ','.join([str(user.id) for user in queryset])
    return HttpResponseRedirect(f"/{MailingUsersURL}?users={users}")


actions_list = [select_from_mailing]
