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
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from admin_web.admin import admin_site
from admin_web.models import SessionOrder
from .forms import LinkedSessionOrderForm

LinkedSessionOrderURL = 'link_session_order'


class LinkedSessionOrderView(FormView):
    form_class = LinkedSessionOrderForm
    template_name = 'admin/custom_form.html'

    def form_valid(self, form: LinkedSessionOrderForm):
        order_id = int(form.cleaned_data['order'])
        sessions = self.request.GET.get("sessions").split(',')

        for session in sessions:
            SessionOrder.objects.get_or_create(session_id=session, order_id=order_id)
        return HttpResponseRedirect("/admin_web/session/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Выбор ордера'
        context['has_permission'] = True
        context['has_file_field'] = True
        context.update(**admin_site.each_context(self.request))
        return context
