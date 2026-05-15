from django.db import models
from django.conf import settings


class Backup(models.Model):
    STATUS_CHOICES = [
        ("created", "Создан"),
        ("restored", "Восстановлен"),
        ("failed", "Ошибка"),
    ]
    file_path = models.CharField("Файл", max_length=500)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="created")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    def __str__(self):
        return self.file_path


class BackupSchedule(models.Model):
    FREQUENCY_CHOICES = [
        ("daily", "Ежедневно"),
        ("weekly", "Еженедельно"),
        ("monthly", "Ежемесячно"),
    ]
    frequency = models.CharField("Частота", max_length=20, choices=FREQUENCY_CHOICES, default="weekly")
    is_active = models.BooleanField("Активно", default=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    def __str__(self):
        return f"{self.get_frequency_display()} ({'активно' if self.is_active else 'выключено'})"

# Create your models here.
