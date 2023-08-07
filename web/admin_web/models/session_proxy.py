from django.db import models

from admin_web.models import Session, Proxy


class SessionProxy(models.Model):
    class Meta:
        db_table = 'session_proxy'
        verbose_name = 'Связь прокси'
        verbose_name_plural = 'Связи прокси'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=False, verbose_name="Время создания")

    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name="Сессия",
                                related_name="session_proxy_session")
    proxy = models.ForeignKey(Proxy, on_delete=models.CASCADE, verbose_name="Прокси",
                              related_name="session_proxy_proxy")

    def __str__(self):
        return f"{self.session}-{self.proxy} ({self.id})"
