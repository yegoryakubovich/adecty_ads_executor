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

            category_1_app = {"name": "Категория 1", "has_module_perms": True, "models": []}
            category_1_list = [""]

            for app in app_list:
                for model in app["models"]:
                    if model["object_name"] in category_1_list:
                        category_1_app["models"].append(app["models"][app["models"].index(model)])
                    else:
                        new_app["models"].append(app["models"][app["models"].index(model)])

            app_list[0] = new_app
            app_list.append(category_1_app) if category_1_app["models"] else None
        return app_list


admin_site = MyAdminSite()

registration_load()
