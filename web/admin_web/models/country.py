from django.db import models


class Country(models.Model):
    class Meta:
        db_table = 'countries'
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=False, verbose_name="Время создания")

    code = models.CharField(max_length=8, unique=True, verbose_name="Код")
    name = models.CharField(max_length=128, verbose_name="Название")

    def __str__(self):
        return f"{self.name} ({self.id})"
