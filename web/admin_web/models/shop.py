from django.db import models


class Shop(models.Model):
    class Meta:
        db_table = 'shops'
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=False, verbose_name="Время создания")

    name = models.CharField(max_length=128, verbose_name="Название")
    link = models.CharField(max_length=128, verbose_name="Ссылка")

    def __str__(self):
        return f"{self.name} ({self.id})"
