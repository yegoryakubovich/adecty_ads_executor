from django.db import models

from admin_web.models import Country, Shop


class ProxyTypes:
    http = "http"
    socks5 = "socks5"

    choices = ((http, http), (socks5, socks5))


class ProxyStates:
    wait = "wait"
    enable = "enable"
    disable = "disable"

    choices = ((wait, wait), (enable, enable), (disable, disable))


class Proxy(models.Model):
    class Meta:
        db_table = 'proxies'
        verbose_name = 'Прокси'
        verbose_name_plural = 'Прокси'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=False, verbose_name="Время создания")

    type = models.CharField(max_length=128, choices=ProxyTypes.choices, verbose_name="Тип")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, verbose_name="Страна")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="Магазин")
    host = models.CharField(max_length=32, verbose_name="Host")
    port = models.IntegerField(verbose_name="Port")
    user = models.CharField(max_length=128, verbose_name="User")
    password = models.CharField(max_length=256, verbose_name="Password")
    max_link = models.IntegerField(default=3, verbose_name="Максимум подключений")

    state = models.CharField(max_length=64, default=ProxyStates.wait, choices=ProxyStates.choices,
                             verbose_name="Состояние")
    state_description = models.CharField(max_length=2056, null=True, blank=True, verbose_name="Описание состояния")

    def __str__(self):
        return f"{self.id} ({self.state})"
