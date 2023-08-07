from django.db import models

from admin_web.models import Country, Shop


class SessionStates:
    waiting = "waiting"
    check = "check"
    free = "free"
    in_work = "in_work"
    banned = "banned"
    spam_block = "spam_block"

    choices = (
        (waiting, waiting), (check, check), (free, free), (in_work, in_work), (banned, banned), (spam_block, spam_block)
    )


class Session(models.Model):
    class Meta:
        db_table = 'sessions'
        verbose_name = 'Сессия'
        verbose_name_plural = 'Сессии'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=False, verbose_name="Время создания")

    phone = models.BigIntegerField(verbose_name="Номер")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Страна")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="Магазин")

    string = models.CharField(max_length=512, verbose_name="String session")
    api_id = models.BigIntegerField(verbose_name="API ID")
    api_hash = models.CharField(max_length=256, verbose_name="API HASH")

    tg_user_id = models.BigIntegerField(verbose_name="Телеграм ID")
    username = models.CharField(max_length=128, null=True, blank=True, verbose_name="USERNAME")
    first_name = models.CharField(max_length=128, null=True, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=128, null=True, blank=True, verbose_name="Фамилия")

    state = models.CharField(max_length=64, default=SessionStates.waiting, choices=SessionStates.choices,
                             verbose_name="Состояние")
    state_description = models.CharField(max_length=2056, null=True, blank=True, verbose_name="Описание состояния")
    work = models.BooleanField(default=False, verbose_name="Запущен")

    messages_send = models.IntegerField(null=True, blank=True, verbose_name="Сообщений отправлено")

    def __str__(self):
        return f"{self.id} ({self.state})"
