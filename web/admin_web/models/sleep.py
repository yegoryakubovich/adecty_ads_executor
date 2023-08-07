from django.db import models

from admin_web.models import Session


class SleepStates:
    enable = 'enable'
    disable = 'disable'

    choices = ((enable, enable), (disable, disable))


class Sleep(models.Model):
    class Meta:
        db_table = 'sleeps'
        verbose_name = 'Сны'
        verbose_name_plural = 'Сон'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=False, verbose_name="Время создания")

    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name="Сессия",
                                related_name="sleep_session")

    time_second = models.IntegerField(verbose_name="Время (сек)")
    state = models.CharField(max_length=32, default=SleepStates.enable, choices=SleepStates.choices,
                             verbose_name="Состояние")

    def __str__(self):
        return f"{self.id} - {self.time_second}с. ({self.state})"
