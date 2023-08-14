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
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from admin_web.admin import admin_site
from admin_web.forms import AddUsersForm
from admin_web.forms.users import MailingUsersForm
from admin_web.models import User, SessionTask, SessionTaskType, SessionTaskStates, Session, SessionStates


class AddUsersView(FormView):
    form_class = AddUsersForm
    template_name = 'admin/custom_form.html'

    def form_valid(self, form: AddUsersForm):
        users = form.cleaned_data["users"].replace(' ', '')
        messages.info(self.request, self.request.GET.get("users"))
        if not users or not users.split(','):
            messages.info(self.request, "Ошибка")
            return HttpResponseRedirect("/add_users")

        for user in users.split(','):
            if user:
                User.objects.get_or_create(username=user)
        messages.info(self.request, "Пользователи успешно добавлены")
        return HttpResponseRedirect("/admin_web/user/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление пользователя'
        context['has_permission'] = True
        context['has_file_field'] = True
        context.update(**admin_site.each_context(self.request))
        return context


class MailingUsersView(FormView):
    form_class = MailingUsersForm
    template_name = 'admin/custom_form.html'

    def form_valid(self, form: MailingUsersForm):
        order_id = int(form.cleaned_data['order'])
        users = self.request.GET.get("users").split(',')

        while users:
            for session in Session.objects.filter(state=SessionStates.free).all():
                if not users:
                    continue
                user_id = users.pop()
                SessionTask.objects.get_or_create(
                    session_id=session.id, user_id=user_id,order_id=order_id,
                    state=SessionTaskStates.enable, type=SessionTaskType.send_by_mailing
                )
        return HttpResponseRedirect("/admin_web/sessiontask/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Выбор ордера'
        context['has_permission'] = True
        context['has_file_field'] = True
        context.update(**admin_site.each_context(self.request))
        return context
