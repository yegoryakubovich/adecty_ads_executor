from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from admin_web.admin import admin_site
from admin_web.forms import AddUsersForm
from admin_web.forms.users import MailingUsersForm
from admin_web.models import User


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
        users = form.cleaned_data["users"].replace(' ', '')
        messages.info(self.request, self.request.GET.get("users"))
        if not users or not users.split(','):
            messages.info(self.request, "Ошибка")
            return HttpResponseRedirect("/add_users")

        for user in users.split(','):
            if user:
                User.objects.get_or_create(username=user)
        messages.info(self.request, "Задачи были созданы")
        return HttpResponseRedirect("/admin_web/sessiontask/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Выбор ордера'
        context['has_permission'] = True
        context['has_file_field'] = True
        context.update(**admin_site.each_context(self.request))
        return context
