from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_panel", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="backup",
            name="file_path",
            field=models.CharField(max_length=500, verbose_name="Файл"),
        ),
    ]
