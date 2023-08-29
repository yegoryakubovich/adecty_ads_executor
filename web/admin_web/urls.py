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
from django.urls import path

from admin_web.admin import admin_site
from admin_web.admin_models.GroupAdmin.views import LinkedGroupOrderURL, LinkedGroupOrderView
from admin_web.admin_models.PersonalAdmin.views import LinkedPersonalOrderView, LinkedPersonalOrderURL
from admin_web.admin_models.SessionAdmin.views import LinkedSessionOrderView, LinkedSessionOrderURL
from admin_web.admin_models.UserAdmin.views import MailingUsersView, AddUsersView, MailingUsersURL, AddUsersURL

urlpatterns = [
    path(AddUsersURL, AddUsersView.as_view(), name="AddUsers"),
    path(MailingUsersURL, MailingUsersView.as_view(), name="MailingUsers"),
    path(LinkedSessionOrderURL, LinkedSessionOrderView.as_view(), name="LinkedSessionOrder"),
    path(LinkedPersonalOrderURL, LinkedPersonalOrderView.as_view(), name="LinkedPersonalOrder"),
    path(LinkedGroupOrderURL, LinkedGroupOrderView.as_view(), name="LinkedGroupOrder"),
    path('', admin_site.urls),
]
