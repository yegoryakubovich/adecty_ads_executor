from django.db import models

from admin_web.models import Session, Order, Group


class MessageStates:
    waiting = 'waiting'
    fine = 'fine'
    deleted = 'deleted'

    choices = ((waiting, waiting), (fine, fine), (deleted, deleted))


class Message(models.Model):
    class Meta:
        db_table = 'messages'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=False, verbose_name="Время создания")

    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name="Сессия",
                                related_name="message_session")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True,verbose_name="Заказ",
                              related_name="message_order")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа",
                              related_name="message_group")
    state = models.CharField(max_length=64, default=MessageStates.waiting, choices=MessageStates.choices,
                             verbose_name="Состояние")

    message_id = models.BigIntegerField(blank=True,verbose_name="ID Сообщения")
    text = models.CharField(max_length=1024, null=True, verbose_name="Текст")

    def __str__(self):
        return f"{self.id} ({self.state})"
