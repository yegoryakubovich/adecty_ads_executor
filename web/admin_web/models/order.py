from django.db import models


class OrderStates:
    waiting = "waiting"
    disable = "finished"
    stopped = "stopped"

    choices = ((waiting, waiting), (disable, disable), (stopped, stopped))


class OrderTypes:
    ads = "ads"
    mailing = "mailing"

    choices = ((ads, ads), (mailing, mailing))


class Order(models.Model):
    class Meta:
        db_table = 'orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=False, verbose_name="Время создания")

    name = models.CharField(max_length=128, verbose_name="Название")
    message = models.CharField(max_length=512, verbose_name="Сообщение")
    message_no_link = models.CharField(max_length=512, verbose_name="Сообщение без ссылки")
    message_short = models.CharField(max_length=256, verbose_name="Сообщение короткое")
    image_link = models.CharField(max_length=256, verbose_name="Ссылка на картинку")

    state = models.CharField(max_length=32, default=OrderStates.waiting, choices=OrderStates.choices,
                             verbose_name="Состояние")
    type = models.CharField(max_length=32, null=True, blank=True, choices=OrderTypes.choices, verbose_name="Тип")

    datetime_stop = models.DateTimeField()

    def __str__(self):
        return f"{self.id} - {self.name} ({self.state})"
