from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DirectMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("body", models.TextField(verbose_name="Сообщение")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, verbose_name="Отправлено")),
                ("read_at", models.DateTimeField(blank=True, null=True, verbose_name="Прочитано")),
                (
                    "recipient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="received_direct_messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_direct_messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Личное сообщение",
                "verbose_name_plural": "Личные сообщения",
                "ordering": ["created_at", "id"],
            },
        ),
        migrations.CreateModel(
            name="EntityComment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("object_id", models.PositiveIntegerField()),
                ("body", models.TextField(verbose_name="Комментарий")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, verbose_name="Создан")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлён")),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entity_comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="contenttypes.contenttype"),
                ),
            ],
            options={
                "verbose_name": "Комментарий к сущности",
                "verbose_name_plural": "Комментарии к сущностям",
                "ordering": ["created_at", "id"],
            },
        ),
        migrations.AddIndex(
            model_name="directmessage",
            index=models.Index(fields=["recipient", "read_at", "created_at"], name="communicati_recipie_c7ddb4_idx"),
        ),
        migrations.AddIndex(
            model_name="directmessage",
            index=models.Index(fields=["sender", "recipient", "created_at"], name="communicati_sender__0f8c80_idx"),
        ),
        migrations.AddIndex(
            model_name="entitycomment",
            index=models.Index(fields=["content_type", "object_id", "created_at"], name="communicati_content_67dfbc_idx"),
        ),
    ]
