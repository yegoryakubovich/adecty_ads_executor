from datetime import datetime

from django.db import models


class PersonalTypes:
    name = 'name'
    surname = 'surname'
    avatar = 'avatar'
    about = 'about'

    choices = (
        (name, name), (surname, surname), (avatar, avatar), (about, about)
    )


class Personal(models.Model):
    class Meta:
        db_table = 'personals'
        verbose_name = 'Персонал'
        verbose_name_plural = 'Персонали'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.now, verbose_name="Время создания")

    type = models.CharField(max_length=64, choices=PersonalTypes.choices, verbose_name="Тип")
    value = models.CharField(max_length=256, verbose_name="Значение")

    def __str__(self):
        return f"{self.id} ({self.type}) - {self.value}"
