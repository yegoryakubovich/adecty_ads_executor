from django.urls import path

from admin_web.admin import admin_site
from admin_web.views import AddUsersView, MailingUsersView

urlpatterns = [
    path("add_users", AddUsersView.as_view(), name="add_users"),
    path("mailing_users", MailingUsersView.as_view(), name="mailing_users"),
    path('', admin_site.urls),
]
