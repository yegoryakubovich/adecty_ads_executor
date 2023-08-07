from django.db import models


class GroupStates:
    waiting = 'waiting'
    active = 'active'
    inactive = 'inactive'

    choices = ((waiting, waiting), (active, active), (inactive, inactive))


class Group(models.Model):
    class Meta:
        db_table = 'groups'
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=False, verbose_name="Время создания")

    name = models.CharField(max_length=128, verbose_name="Название")
    state = models.CharField(max_length=32, default=GroupStates.waiting, choices=GroupStates.choices,
                             verbose_name="Состояние")
    subscribers = models.IntegerField(verbose_name="Подписчиков")  # Количество подписчиков

    can_image = models.BooleanField(default=True, verbose_name="Отправка картинки")
    can_message = models.BooleanField(default=False, verbose_name="Отправка ссылок")
    can_message_no_url = models.BooleanField(default=True, verbose_name="Отправка без ссылок")
    can_message_short = models.BooleanField(default=True, verbose_name="Отправка короткого текста")

    captcha_have = models.BooleanField(default=False, verbose_name="Капча")
    captcha_type = models.CharField(max_length=128, blank=True, verbose_name="Тип капчи")
    captcha_data = models.CharField(max_length=128, blank=True, verbose_name="Информация по капче")

    def __str__(self):
        return f"{self.id} - {self.name}  ({self.state})"
