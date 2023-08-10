from django import forms

from admin_web.models import Order, OrderTypes


class AddUsersForm(forms.Form):
    users = forms.CharField(widget=forms.Textarea, label="Пользователи через запятую", required=True)


class MailingUsersForm(forms.Form):
    choices = [(order.name, order.id) for order in Order.objects.all()]
    order = forms.ChoiceField(choices=choices, label="Выбор ордера", required=True)
