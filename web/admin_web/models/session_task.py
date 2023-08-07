from django.db import models

from admin_web.models import Session, Group, Order, Message


class SessionTaskType:
    non_type = 'non_type'
    check_group = 'check_group'
    join_group = 'join_group'
    send_by_order = 'send_by_order'
    check_message = 'check_message'

    choices = (
        (non_type, non_type), (check_group, check_group), (join_group, join_group),
        (send_by_order, send_by_order), (check_message, check_message),
    )


class SessionTaskStates:
    enable = 'enable'
    finished = 'finished'
    abortively = 'abortively'

    choices = ((enable, enable), (finished, finished), (abortively, abortively))


class SessionTask(models.Model):
    class Meta:
        db_table = 'sessions_tasks'
        verbose_name = 'Задача Сессии'
        verbose_name_plural = 'Задачи сессий'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=False, verbose_name="Время создания")

    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name="Сессия",
                                related_name="session_tasks_session")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа",
                              related_name="session_tasks_group")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Заказ",
                              related_name="session_tasks_order")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщение",
                                related_name="session_tasks_message")

    state = models.CharField(max_length=32, default=SessionTaskStates.enable, choices=SessionTaskStates.choices,
                             verbose_name="Состояние")
    state_description = models.CharField(max_length=64, null=True, blank=True, verbose_name="Описание")

    type = models.CharField(max_length=32, default=SessionTaskType.non_type, choices=SessionTaskType.choices,
                            verbose_name="Тип")

    def __str__(self):
        return f"{self.id} ({self.state})"
