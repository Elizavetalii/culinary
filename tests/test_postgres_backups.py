from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.conf import settings
from django.test import TransactionTestCase, override_settings
from django.urls import reverse

from admin_panel.models import Backup
from crm.models import Role, User, UserRole


class PostgresBackupTests(TransactionTestCase):
    def setUp(self):
        role = Role.objects.create(name="Администратор системы")
        self.admin = User.objects.create_user(
            username="backup-admin",
            email="backup-admin@example.com",
            password="pass",
            full_name="Backup Admin",
        )
        UserRole.objects.create(user=self.admin, role=role)

    @override_settings(
        PG_DUMP_PATH="/usr/lib/postgresql/16/bin/pg_dump",
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "art_culinary_crm",
                "USER": "artculinary_user",
                "PASSWORD": "secret",
                "HOST": "localhost",
                "PORT": "5432",
                "ATOMIC_REQUESTS": True,
            }
        }
    )
    @patch("admin_panel.views.subprocess.run")
    def test_backup_create_uses_pg_dump_for_postgresql_database(self, run_mock):
        self.client.force_login(self.admin)

        response = self.client.post(reverse("admin-backup-create"))

        self.assertEqual(response.status_code, 302)
        run_mock.assert_called_once()
        command = run_mock.call_args.args[0]
        self.assertEqual(command[0], "/usr/lib/postgresql/16/bin/pg_dump")
        self.assertIn("--clean", command)
        self.assertIn("--if-exists", command)
        self.assertIn("--exclude-table-data=admin_panel_backup", command)
        self.assertIn("-f", command)
        backup = Backup.objects.latest("created_at")
        self.assertTrue(backup.file_path.endswith(".sql"))
        self.assertTrue(backup.file_path.startswith("backups/"))

    @override_settings(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "art_culinary_crm",
                "USER": "artculinary_user",
                "PASSWORD": "secret",
                "HOST": "localhost",
                "PORT": "5432",
                "ATOMIC_REQUESTS": True,
            }
        }
    )
    @patch("admin_panel.views.subprocess.run")
    def test_backup_create_accepts_user_selected_server_directory(self, run_mock):
        self.client.force_login(self.admin)

        with TemporaryDirectory() as backup_dir:
            response = self.client.post(
                reverse("admin-backup-create"),
                {"destination_dir": backup_dir},
            )

        self.assertEqual(response.status_code, 302)
        command = run_mock.call_args.args[0]
        dest = Path(command[command.index("-f") + 1])
        self.assertEqual(dest.parent, Path(backup_dir))
        backup = Backup.objects.latest("created_at")
        self.assertEqual(Path(backup.file_path).parent.resolve(), Path(backup_dir).resolve())

    @override_settings(
        PSQL_PATH="/usr/lib/postgresql/16/bin/psql",
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "art_culinary_crm",
                "USER": "artculinary_user",
                "PASSWORD": "secret",
                "HOST": "localhost",
                "PORT": "5432",
                "ATOMIC_REQUESTS": True,
            }
        }
    )
    @patch("admin_panel.views.subprocess.run")
    def test_backup_restore_uses_psql_for_postgresql_dump(self, run_mock):
        backup_file = Path(settings.MEDIA_ROOT / "backups" / "restore-test.sql")
        backup_file.parent.mkdir(parents=True, exist_ok=True)
        backup_file.write_text("-- test dump", encoding="utf-8")
        backup = Backup.objects.create(file_path="backups/restore-test.sql", created_by=self.admin)
        self.client.force_login(self.admin)

        response = self.client.post(reverse("admin-backup-restore", args=[backup.pk]))

        self.assertEqual(response.status_code, 302)
        command = run_mock.call_args.args[0]
        self.assertEqual(command[0], "/usr/lib/postgresql/16/bin/psql")
        self.assertIn("-f", command)
        self.assertIn(str(backup_file), command)
        backup.refresh_from_db()
        self.assertEqual(backup.status, "restored")
