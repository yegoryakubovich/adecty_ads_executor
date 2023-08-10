from django.db import models

from admin_web.models import Session, User, Order, Group


class MessageStates:
    from_user = 'from_user'
    to_user = 'to_user'
    waiting = 'waiting'
    fine = 'fine'
    deleted = 'deleted'

    choices = ((from_user, from_user), (to_user, to_user), (waiting, waiting), (fine, fine), (deleted, deleted))


class Message(models.Model):
    class Meta:
        db_table = 'messages'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=False, verbose_name="Время создания")

    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True,
                                related_name="message_session", verbose_name="Сессия")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="message_user",
                             verbose_name="Пользователь")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name="message_order",
                              verbose_name="Заказ")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, related_name="message_group",
                              verbose_name="Группа")
    state = models.CharField(max_length=64, default=MessageStates.waiting, choices=MessageStates.choices,
                             verbose_name="Состояние")

    message_id = models.BigIntegerField(blank=True, verbose_name="ID Сообщения")
    text = models.CharField(max_length=1024, null=True, verbose_name="Текст")

    def __str__(self):
        return f"{self.id} ({self.state})"
