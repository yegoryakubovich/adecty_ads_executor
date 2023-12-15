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
from django.contrib.admin import AdminSite

from admin_web.admin_models import registration_load


class MyAdminSite(AdminSite):
    site_header = "Панель администрирования Телеграм-бота"
    site_title = "Админ-панель |"
    index_title = " "

    def get_app_list(self, request):
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())
        if app_list:
            new_app = {"name": "Основной", "app_label": "admin_web", "has_module_perms": True, "models": []}

            addon_app = {"name": "Побочный", "has_module_perms": True, "models": []}
            addon_app_list = [
                "SessionProxy", "SessionGroup", "SessionPersonal", "SessionOrder", "SessionDevice",
                "GroupCountry",
                "OrderAttachment", "OrderGroup", "OrderPersonal", "OrderUser",
                "CountryLink",
            ]

            for app in app_list:
                for model in app["models"]:
                    if model["object_name"] in addon_app_list:
                        addon_app["models"].append(app["models"][app["models"].index(model)])
                    else:
                        new_app["models"].append(app["models"][app["models"].index(model)])

            app_list[0] = new_app
            app_list.append(addon_app) if addon_app["models"] else None
        return app_list


admin_site = MyAdminSite()

registration_load()
