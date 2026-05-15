from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from crm.models import User


class DirectMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_direct_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_direct_messages")
    body = models.TextField("Сообщение")
    created_at = models.DateTimeField("Отправлено", default=timezone.now)
    read_at = models.DateTimeField("Прочитано", null=True, blank=True)

    class Meta:
        ordering = ["created_at", "id"]
        verbose_name = "Личное сообщение"
        verbose_name_plural = "Личные сообщения"
        indexes = [
            models.Index(fields=["recipient", "read_at", "created_at"]),
            models.Index(fields=["sender", "recipient", "created_at"]),
        ]

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.body[:40]}"


class EntityComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entity_comments")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    body = models.TextField("Комментарий")
    created_at = models.DateTimeField("Создан", default=timezone.now)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        ordering = ["created_at", "id"]
        verbose_name = "Комментарий к сущности"
        verbose_name_plural = "Комментарии к сущностям"
        indexes = [
            models.Index(fields=["content_type", "object_id", "created_at"]),
        ]

    def __str__(self):
        return f"{self.author}: {self.body[:40]}"
