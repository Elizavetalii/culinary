# Таблица - Модули программы ArtCulinary CRM

В таблице приведены программные модули проекта: исходный код, миграции, шаблоны, статические ресурсы, тесты, конфигурационные файлы, скрипты и проектная документация. Служебные каталоги виртуального окружения, кэши, собранная статика, внешние wheel-зависимости и runtime-файлы из `media/` не включены, так как не являются собственными модулями программы.

| № | Модуль | Описание | Количество строк кода/верстки | Размер (Кбайт) |
|---:|---|---|---:|---:|
| 1 | `.env` | Файл локальных переменных окружения проекта | 10 | 1 |
| 2 | `.env.example` | Пример файла переменных окружения проекта | 11 | 1 |
| 3 | `.github\workflows\pipeline.yaml` | Конфигурация GitHub Actions для автоматической проверки проекта | 171 | 5 |
| 4 | `.gitignore` | Файл исключений Git-репозитория | 6 | 1 |
| 5 | `.gitlab-ci.yml` | Конфигурация CI/CD GitLab | 102 | 3 |
| 6 | `accounts\__init__.py` | Python-модуль   init   приложения аккаунтов и авторизации | 0 | 0 |
| 7 | `accounts\admin.py` | Python-модуль admin приложения аккаунтов и авторизации | 3 | 1 |
| 8 | `accounts\apps.py` | Python-модуль apps приложения аккаунтов и авторизации | 5 | 1 |
| 9 | `accounts\context_processors.py` | Python-модуль context processors приложения аккаунтов и авторизации | 11 | 1 |
| 10 | `accounts\management\__init__.py` | Python-модуль   init   приложения аккаунтов и авторизации | 1 | 1 |
| 11 | `accounts\management\commands\__init__.py` | Инициализация пакета пользовательских команд приложения аккаунтов и авторизации | 1 | 1 |
| 12 | `accounts\management\commands\seed_demo.py` | Команда управления Django для seed demo в приложении аккаунтов и авторизации | 424 | 18 |
| 13 | `accounts\migrations\__init__.py` | Инициализация пакета миграций приложения аккаунтов и авторизации | 0 | 0 |
| 14 | `accounts\models.py` | Python-модуль models приложения аккаунтов и авторизации | 3 | 1 |
| 15 | `accounts\tests.py` | Python-модуль tests приложения аккаунтов и авторизации | 3 | 1 |
| 16 | `accounts\urls.py` | Python-модуль urls приложения аккаунтов и авторизации | 26 | 2 |
| 17 | `accounts\utils.py` | Python-модуль utils приложения аккаунтов и авторизации | 28 | 1 |
| 18 | `accounts\views.py` | Python-модуль views приложения аккаунтов и авторизации | 68 | 3 |
| 19 | `admin_panel\__init__.py` | Python-модуль   init   приложения административной панели | 0 | 0 |
| 20 | `admin_panel\admin.py` | Python-модуль admin приложения административной панели | 3 | 1 |
| 21 | `admin_panel\apps.py` | Python-модуль apps приложения административной панели | 5 | 1 |
| 22 | `admin_panel\entity_config.py` | Python-модуль entity config приложения административной панели | 320 | 12 |
| 23 | `admin_panel\forms.py` | Python-модуль forms приложения административной панели | 126 | 5 |
| 24 | `admin_panel\migrations\__init__.py` | Инициализация пакета миграций приложения административной панели | 0 | 0 |
| 25 | `admin_panel\migrations\0001_initial.py` | Начальная миграция приложения административной панели | 34 | 2 |
| 26 | `admin_panel\migrations\0002_backup_file_path_length.py` | Миграция приложения административной панели: backup file path length | 16 | 1 |
| 27 | `admin_panel\models.py` | Python-модуль models приложения административной панели | 33 | 2 |
| 28 | `admin_panel\tests.py` | Python-модуль tests приложения административной панели | 3 | 1 |
| 29 | `admin_panel\urls.py` | Python-модуль urls приложения административной панели | 50 | 3 |
| 30 | `admin_panel\views.py` | Python-модуль views приложения административной панели | 786 | 33 |
| 31 | `artifacts\ArtCulinaryCRM_full_code.docx` | Файл проекта | 3730 | 956 |
| 32 | `clients\__init__.py` | Python-модуль   init   приложения клиентов | 0 | 0 |
| 33 | `clients\admin.py` | Python-модуль admin приложения клиентов | 3 | 1 |
| 34 | `clients\apps.py` | Python-модуль apps приложения клиентов | 5 | 1 |
| 35 | `clients\forms.py` | Python-модуль forms приложения клиентов | 359 | 17 |
| 36 | `clients\migrations\__init__.py` | Инициализация пакета миграций приложения клиентов | 0 | 0 |
| 37 | `clients\models.py` | Python-модуль models приложения клиентов | 3 | 1 |
| 38 | `clients\tests.py` | Python-модуль tests приложения клиентов | 3 | 1 |
| 39 | `clients\urls.py` | Python-модуль urls приложения клиентов | 10 | 1 |
| 40 | `clients\views.py` | Python-модуль views приложения клиентов | 116 | 5 |
| 41 | `communications\__init__.py` | Python-модуль   init   приложения коммуникаций | 1 | 1 |
| 42 | `communications\apps.py` | Python-модуль apps приложения коммуникаций | 7 | 1 |
| 43 | `communications\context_processors.py` | Python-модуль context processors приложения коммуникаций | 12 | 1 |
| 44 | `communications\forms.py` | Python-модуль forms приложения коммуникаций | 42 | 2 |
| 45 | `communications\migrations\__init__.py` | Инициализация пакета миграций приложения коммуникаций | 1 | 1 |
| 46 | `communications\migrations\0001_initial.py` | Начальная миграция приложения коммуникаций | 85 | 4 |
| 47 | `communications\models.py` | Python-модуль models приложения коммуникаций | 47 | 2 |
| 48 | `communications\services.py` | Python-модуль services приложения коммуникаций | 42 | 2 |
| 49 | `communications\urls.py` | Python-модуль urls приложения коммуникаций | 12 | 1 |
| 50 | `communications\views.py` | Python-модуль views приложения коммуникаций | 129 | 6 |
| 51 | `create_demo_users.py` | Скрипт создания демонстрационных пользователей | 21 | 1 |
| 52 | `crm\__init__.py` | Python-модуль   init   приложения CRM | 1 | 1 |
| 53 | `crm\admin_site.py` | Python-модуль admin site приложения CRM | 74 | 3 |
| 54 | `crm\admin.py` | Python-модуль admin приложения CRM | 91 | 3 |
| 55 | `crm\api.py` | Python-модуль api приложения CRM | 334 | 11 |
| 56 | `crm\apps.py` | Python-модуль apps приложения CRM | 7 | 1 |
| 57 | `crm\forms.py` | Python-модуль forms приложения CRM | 14 | 1 |
| 58 | `crm\management\commands\seed_dishes.py` | Команда управления Django для seed dishes в приложении CRM | 239 | 10 |
| 59 | `crm\management\commands\seed_logistics.py` | Команда управления Django для seed logistics в приложении CRM | 188 | 9 |
| 60 | `crm\migrations\__init__.py` | Инициализация пакета миграций приложения CRM | 0 | 0 |
| 61 | `crm\migrations\0001_initial.py` | Начальная миграция приложения CRM | 342 | 23 |
| 62 | `crm\migrations\0002_client_current_stage.py` | Миграция приложения CRM: client current stage | 24 | 1 |
| 63 | `crm\migrations\0003_client_created_at.py` | Миграция приложения CRM: client created at | 16 | 1 |
| 64 | `crm\migrations\0004_order_archived.py` | Миграция приложения CRM: order archived | 16 | 1 |
| 65 | `crm\migrations\0005_delivery_fields.py` | Миграция приложения CRM: delivery fields | 49 | 2 |
| 66 | `crm\migrations\0006_picking_session_and_item_fields.py` | Миграция приложения CRM: picking session and item fields | 59 | 3 |
| 67 | `crm\migrations\0007_logistics_profile_and_cargo_fields.py` | Миграция приложения CRM: logistics profile and cargo fields | 106 | 6 |
| 68 | `crm\migrations\0008_update_logistics_status_and_route_type.py` | Миграция приложения CRM: update logistics status and route type | 43 | 2 |
| 69 | `crm\migrations\0009_alter_logisticianprofile_id_alter_order_status.py` | Миграция приложения CRM: alter logisticianprofile id alter order status | 23 | 1 |
| 70 | `crm\migrations\0010_courier_current_latitude_courier_current_longitude_and_more.py` | Миграция приложения CRM: courier current latitude courier current longitude and more | 59 | 3 |
| 71 | `crm\migrations\0011_delivery_delivery_date_route_max_duration_minutes_and_more.py` | Миграция приложения CRM: delivery delivery date route max duration minutes and more | 174 | 9 |
| 72 | `crm\migrations\0012_routestop_proof_review_comment_and_more.py` | Миграция приложения CRM: routestop proof review comment and more | 35 | 2 |
| 73 | `crm\migrations\0013_equipment_client_daily_max_weight_kg_and_more.py` | Миграция приложения CRM: equipment client daily max weight kg and more | 199 | 11 |
| 74 | `crm\migrations\0014_dish_default_price.py` | Миграция приложения CRM: dish default price | 18 | 1 |
| 75 | `crm\migrations\0015_dish_daily_capacity.py` | Миграция приложения CRM: dish daily capacity | 18 | 1 |
| 76 | `crm\migrations\0015_dish_uom_fields.py` | Миграция приложения CRM: dish uom fields | 34 | 2 |
| 77 | `crm\migrations\0016_merge_0015_dish_daily_capacity_0015_dish_uom_fields.py` | Миграция приложения CRM: merge 0015 dish daily capacity 0015 dish uom fields | 14 | 1 |
| 78 | `crm\migrations\0017_postgres_db_logic.py` | Миграция приложения CRM: postgres db logic | 182 | 5 |
| 79 | `crm\models.py` | Python-модуль models приложения CRM | 665 | 33 |
| 80 | `crm\validators.py` | Python-модуль validators приложения CRM | 64 | 2 |
| 81 | `dashboard\__init__.py` | Python-модуль   init   приложения панелей управления | 0 | 0 |
| 82 | `dashboard\admin.py` | Python-модуль admin приложения панелей управления | 3 | 1 |
| 83 | `dashboard\apps.py` | Python-модуль apps приложения панелей управления | 5 | 1 |
| 84 | `dashboard\migrations\__init__.py` | Инициализация пакета миграций приложения панелей управления | 0 | 0 |
| 85 | `dashboard\models.py` | Python-модуль models приложения панелей управления | 3 | 1 |
| 86 | `dashboard\tests.py` | Python-модуль tests приложения панелей управления | 3 | 1 |
| 87 | `dashboard\urls.py` | Python-модуль urls приложения панелей управления | 9 | 1 |
| 88 | `dashboard\views.py` | Python-модуль views приложения панелей управления | 119 | 5 |
| 89 | `docs\appendix_A_core_code.docx` | Документ Microsoft Word с материалами проекта | 21 | 6 |
| 90 | `docs\appendix_A_core_code.html` | HTML-документ с материалами проекта | 274 | 9 |
| 91 | `docs\appendix_A_core_code.rtf` | RTF-документ с материалами проекта | 152 | 9 |
| 92 | `docs\appendix_A_main_code.docx` | Документ Microsoft Word с материалами проекта | 34 | 13 |
| 93 | `docs\appendix_A_main_code.rtf` | RTF-документ с материалами проекта | 769 | 37 |
| 94 | `docs\appendix_A_program_text_formatted.docx` | Документ Microsoft Word с материалами проекта | 307 | 83 |
| 95 | `docs\appendix_A_program_text_full.md` | Текстовый документ проекта в формате Markdown | 15407 | 569 |
| 96 | `docs\appendix_A_program_text.md` | Текстовый документ проекта в формате Markdown | 7286 | 283 |
| 97 | `docs\appendix_A_top15_code.docx` | Документ Microsoft Word с материалами проекта | 185 | 45 |
| 98 | `docs\appendix_A_top15_code.rtf` | RTF-документ с материалами проекта | 3498 | 198 |
| 99 | `docs\appendix_A_top40_code.docx` | Документ Microsoft Word с материалами проекта | 152 | 47 |
| 100 | `docs\appendix_A_top40_code.rtf` | RTF-документ с материалами проекта | 3797 | 206 |
| 101 | `docs\appendix_A_top5_code.docx` | Документ Microsoft Word с материалами проекта | 84 | 20 |
| 102 | `docs\appendix_A_top5_code.rtf` | RTF-документ с материалами проекта | 1337 | 80 |
| 103 | `docs\class_diagram_main.drawio` | Диаграмма Draw.io для документации проекта | 225 | 21 |
| 104 | `docs\database_script_for_report_core_postgres.sql` | SQL-скрипт структуры и объектов базы данных | 745 | 27 |
| 105 | `docs\database_script_for_report_core.sql` | SQL-скрипт структуры и объектов базы данных | 275 | 23 |
| 106 | `docs\database_script_for_report_postgres.sql` | SQL-скрипт структуры и объектов базы данных | 827 | 30 |
| 107 | `docs\database_script_for_report.sql` | SQL-скрипт структуры и объектов базы данных | 321 | 26 |
| 108 | `docs\db_logical_model.drawio` | Диаграмма Draw.io для документации проекта | 1 | 57 |
| 109 | `docs\db_physical_model.drawio` | Диаграмма Draw.io для документации проекта | 1 | 55 |
| 110 | `docs\functional_scheme_art_culinary_final.drawio` | Функциональная схема программы | 752 | 54 |
| 111 | `docs\functional_scheme_by_roles.drawio` | Функциональная схема программы | 87 | 11 |
| 112 | `docs\idef0_artculinary_to_be.drawio` | Диаграмма Draw.io для документации проекта | 567 | 46 |
| 113 | `docs\idef0_artculinary.drawio` | Диаграмма Draw.io для документации проекта | 306 | 51 |
| 114 | `docs\lint.js` | Скрипт проверки или обработки документации | 26 | 1 |
| 115 | `docs\load_test_report.md` | Текстовый документ проекта в формате Markdown | 35 | 2 |
| 116 | `docs\locust_integration_exceptions.csv` | Табличные данные для документации проекта | 1 | 1 |
| 117 | `docs\locust_integration_failures.csv` | Табличные данные для документации проекта | 1 | 1 |
| 118 | `docs\locust_integration_stats_history.csv` | Табличные данные для документации проекта | 956 | 146 |
| 119 | `docs\locust_integration_stats.csv` | Табличные данные для документации проекта | 28 | 5 |
| 120 | `docs\postgres_procedures_functions_triggers.sql` | SQL-скрипт структуры и объектов базы данных | 131 | 4 |
| 121 | `docs\structural_scheme_art_culinary.drawio` | Структурная схема программы | 501 | 37 |
| 122 | `docs\structural_scheme_program.drawio` | Структурная схема программы | 272 | 28 |
| 123 | `docs\superpowers\plans\2026-05-13-russian-field-validation.md` | Текстовый документ проекта в формате Markdown | 136 | 5 |
| 124 | `docs\superpowers\specs\2026-05-13-russian-field-validation-design.md` | Текстовый документ проекта в формате Markdown | 36 | 2 |
| 125 | `docs\table_models_description.md` | Таблица описания моделей данных программы | 41 | 13 |
| 126 | `docs\table9_characteristics_98.tsv` | Файл документации проекта | 99 | 10 |
| 127 | `docs\test_cases_artculinary_full_coverage.docx` | Документ Microsoft Word с материалами проекта | 39 | 10 |
| 128 | `docs\test_cases_artculinary_full_coverage.docx.bak` | Файл документации проекта | 32 | 11 |
| 129 | `docs\testing_scheme.drawio` | Диаграмма Draw.io для документации проекта | 138 | 16 |
| 130 | `docs\ui_scheme_by_roles.drawio` | Диаграмма Draw.io для документации проекта | 110 | 17 |
| 131 | `docs\ui_scheme_full_flow.drawio` | Диаграмма Draw.io для документации проекта | 140 | 24 |
| 132 | `docs\usecase_roles.drawio` | Диаграмма Draw.io для документации проекта | 199 | 21 |
| 133 | `docs\user_interface_scheme_art_culinary_final.drawio` | Схема пользовательского интерфейса программы | 685 | 50 |
| 134 | `factory_crm\__init__.py` | Инициализация конфигурационного пакета проекта | 1 | 1 |
| 135 | `factory_crm\asgi.py` | ASGI-конфигурация проекта | 5 | 1 |
| 136 | `factory_crm\settings.py` | Основные настройки Django-проекта | 191 | 7 |
| 137 | `factory_crm\urls.py` | Главная маршрутизация Django-проекта | 52 | 3 |
| 138 | `factory_crm\views.py` | Python-модуль views приложения конфигурации проекта | 79 | 3 |
| 139 | `factory_crm\wsgi.py` | WSGI-конфигурация проекта | 5 | 1 |
| 140 | `fixtures\sample_data.json` | Файл фикстур с начальными или демонстрационными данными | 184 | 5 |
| 141 | `locust.conf` | Файл проекта | 4 | 1 |
| 142 | `locustfile.py` | Python-модуль locustfile приложения locustfile.py | 122 | 4 |
| 143 | `logistics\__init__.py` | Python-модуль   init   приложения логистики | 0 | 0 |
| 144 | `logistics\admin.py` | Python-модуль admin приложения логистики | 3 | 1 |
| 145 | `logistics\apps.py` | Python-модуль apps приложения логистики | 5 | 1 |
| 146 | `logistics\forms.py` | Python-модуль forms приложения логистики | 241 | 10 |
| 147 | `logistics\migrations\__init__.py` | Инициализация пакета миграций приложения логистики | 0 | 0 |
| 148 | `logistics\models.py` | Python-модуль models приложения логистики | 3 | 1 |
| 149 | `logistics\tests.py` | Python-модуль tests приложения логистики | 155 | 6 |
| 150 | `logistics\urls.py` | Python-модуль urls приложения логистики | 40 | 2 |
| 151 | `logistics\views.py` | Python-модуль views приложения логистики | 701 | 30 |
| 152 | `manage.py` | Управляющий файл Django-проекта | 18 | 1 |
| 153 | `orders\__init__.py` | Python-модуль   init   приложения заказов | 0 | 0 |
| 154 | `orders\admin.py` | Python-модуль admin приложения заказов | 3 | 1 |
| 155 | `orders\apps.py` | Python-модуль apps приложения заказов | 5 | 1 |
| 156 | `orders\forms.py` | Python-модуль forms приложения заказов | 186 | 8 |
| 157 | `orders\migrations\__init__.py` | Инициализация пакета миграций приложения заказов | 0 | 0 |
| 158 | `orders\models.py` | Python-модуль models приложения заказов | 3 | 1 |
| 159 | `orders\tests.py` | Python-модуль tests приложения заказов | 139 | 6 |
| 160 | `orders\urls.py` | Python-модуль urls приложения заказов | 26 | 1 |
| 161 | `orders\views.py` | Python-модуль views приложения заказов | 637 | 27 |
| 162 | `portal\__init__.py` | Python-модуль   init   приложения клиентского портала | 1 | 1 |
| 163 | `portal\forms.py` | Python-модуль forms приложения клиентского портала | 125 | 5 |
| 164 | `portal\urls.py` | Python-модуль urls приложения клиентского портала | 19 | 2 |
| 165 | `portal\utils.py` | Python-модуль utils приложения клиентского портала | 34 | 2 |
| 166 | `portal\views.py` | Python-модуль views приложения клиентского портала | 155 | 6 |
| 167 | `README.md` | Основное описание проекта и инструкции по запуску | 53 | 3 |
| 168 | `reports\__init__.py` | Python-модуль   init   приложения отчётов | 0 | 0 |
| 169 | `reports\admin.py` | Python-модуль admin приложения отчётов | 3 | 1 |
| 170 | `reports\apps.py` | Python-модуль apps приложения отчётов | 5 | 1 |
| 171 | `reports\forms.py` | Python-модуль forms приложения отчётов | 17 | 1 |
| 172 | `reports\migrations\__init__.py` | Инициализация пакета миграций приложения отчётов | 0 | 0 |
| 173 | `reports\migrations\0001_initial.py` | Начальная миграция приложения отчётов | 29 | 2 |
| 174 | `reports\migrations\0002_report_validation.py` | Миграция приложения отчётов: report validation | 21 | 1 |
| 175 | `reports\models.py` | Python-модуль models приложения отчётов | 32 | 2 |
| 176 | `reports\services.py` | Python-модуль services приложения отчётов | 321 | 15 |
| 177 | `reports\tests.py` | Python-модуль tests приложения отчётов | 3 | 1 |
| 178 | `reports\urls.py` | Python-модуль urls приложения отчётов | 11 | 1 |
| 179 | `reports\views.py` | Python-модуль views приложения отчётов | 192 | 7 |
| 180 | `requirements.txt` | Список Python-зависимостей проекта | 8 | 1 |
| 181 | `scripts\run_automated_tests.sh` | Скрипт автоматизации проекта: run automated tests | 21 | 1 |
| 182 | `static\admin_theme.css` | CSS-стили раздела admin_theme.css | 575 | 14 |
| 183 | `static\css\app.css` | CSS-стили раздела css | 592 | 12 |
| 184 | `static\login_root.css` | CSS-стили раздела login_root.css | 66 | 2 |
| 185 | `static\manager.css` | CSS-стили раздела manager.css | 93 | 4 |
| 186 | `templates\404.html` | HTML-шаблон раздела интерфейса:  | 44 | 2 |
| 187 | `templates\500.html` | HTML-шаблон раздела интерфейса:  | 44 | 2 |
| 188 | `templates\accounts\login_base.html` | HTML-шаблон раздела аккаунтов: login base | 52 | 2 |
| 189 | `templates\accounts\login.html` | HTML-шаблон раздела аккаунтов: login | 102 | 4 |
| 190 | `templates\accounts\password_reset_complete.html` | HTML-шаблон раздела аккаунтов: password reset complete | 6 | 1 |
| 191 | `templates\accounts\password_reset_confirm.html` | HTML-шаблон раздела аккаунтов: password reset confirm | 20 | 1 |
| 192 | `templates\accounts\password_reset_done.html` | HTML-шаблон раздела аккаунтов: password reset done | 8 | 1 |
| 193 | `templates\accounts\password_reset_email.html` | HTML-шаблон раздела аккаунтов: password reset email | 8 | 1 |
| 194 | `templates\accounts\password_reset_form.html` | HTML-шаблон раздела аккаунтов: password reset form | 17 | 1 |
| 195 | `templates\accounts\password_reset_subject.txt` | Текстовый шаблон раздела аккаунтов: password reset subject | 1 | 1 |
| 196 | `templates\admin_panel\access.html` | HTML-шаблон раздела административной панели: access | 42 | 2 |
| 197 | `templates\admin_panel\analytics.html` | HTML-шаблон раздела административной панели: analytics | 161 | 6 |
| 198 | `templates\admin_panel\backup_schedule.html` | HTML-шаблон раздела административной панели: backup schedule | 31 | 2 |
| 199 | `templates\admin_panel\backups.html` | HTML-шаблон раздела административной панели: backups | 79 | 3 |
| 200 | `templates\admin_panel\data_check.html` | HTML-шаблон раздела административной панели: data check | 50 | 2 |
| 201 | `templates\admin_panel\entities\delete.html` | HTML-шаблон раздела административной панели: delete | 38 | 2 |
| 202 | `templates\admin_panel\entities\detail.html` | HTML-шаблон раздела административной панели: detail | 69 | 3 |
| 203 | `templates\admin_panel\entities\form.html` | HTML-шаблон раздела административной панели: form | 96 | 4 |
| 204 | `templates\admin_panel\entities\list.html` | HTML-шаблон раздела административной панели: list | 134 | 6 |
| 205 | `templates\admin_panel\index.html` | HTML-шаблон раздела административной панели: index | 76 | 3 |
| 206 | `templates\admin_panel\role_form.html` | HTML-шаблон раздела административной панели: role form | 31 | 1 |
| 207 | `templates\admin_panel\roles_list.html` | HTML-шаблон раздела административной панели: roles list | 36 | 1 |
| 208 | `templates\admin_panel\user_delete.html` | HTML-шаблон раздела административной панели: user delete | 20 | 1 |
| 209 | `templates\admin_panel\user_form.html` | HTML-шаблон раздела административной панели: user form | 75 | 3 |
| 210 | `templates\admin_panel\user_password.html` | HTML-шаблон раздела административной панели: user password | 32 | 2 |
| 211 | `templates\admin_panel\users_list.html` | HTML-шаблон раздела административной панели: users list | 64 | 3 |
| 212 | `templates\admin\base_site.html` | HTML-шаблон раздела admin: base site | 78 | 3 |
| 213 | `templates\admin\index.html` | HTML-шаблон раздела admin: index | 30 | 1 |
| 214 | `templates\base.html` | HTML-шаблон раздела интерфейса: base | 146 | 6 |
| 215 | `templates\clients\delete.html` | HTML-шаблон раздела клиентов: delete | 26 | 1 |
| 216 | `templates\clients\detail.html` | HTML-шаблон раздела клиентов: detail | 178 | 7 |
| 217 | `templates\clients\form.html` | HTML-шаблон раздела клиентов: form | 427 | 22 |
| 218 | `templates\clients\list.html` | HTML-шаблон раздела клиентов: list | 96 | 5 |
| 219 | `templates\communications\entity_comments.html` | HTML-шаблон раздела коммуникаций: entity comments | 20 | 1 |
| 220 | `templates\communications\inbox.html` | HTML-шаблон раздела коммуникаций: inbox | 53 | 2 |
| 221 | `templates\communications\thread.html` | HTML-шаблон раздела коммуникаций: thread | 90 | 4 |
| 222 | `templates\courier\profile.html` | HTML-шаблон раздела courier: profile | 53 | 3 |
| 223 | `templates\courier\route_detail.html` | HTML-шаблон раздела courier: route detail | 120 | 6 |
| 224 | `templates\courier\routes.html` | HTML-шаблон раздела courier: routes | 54 | 2 |
| 225 | `templates\dashboard\admin.html` | HTML-шаблон раздела панели управления: admin | 51 | 2 |
| 226 | `templates\dashboard\logistic.html` | HTML-шаблон раздела панели управления: logistic | 224 | 9 |
| 227 | `templates\dashboard\manager.html` | HTML-шаблон раздела панели управления: manager | 134 | 5 |
| 228 | `templates\dashboard\picker.html` | HTML-шаблон раздела панели управления: picker | 59 | 2 |
| 229 | `templates\login_root.html` | HTML-шаблон раздела интерфейса: login root | 33 | 2 |
| 230 | `templates\logistics\couriers.html` | HTML-шаблон раздела логистики: couriers | 114 | 6 |
| 231 | `templates\logistics\delivery_card.html` | HTML-шаблон раздела логистики: delivery card | 163 | 8 |
| 232 | `templates\logistics\form.html` | HTML-шаблон раздела логистики: form | 31 | 1 |
| 233 | `templates\logistics\list.html` | HTML-шаблон раздела логистики: list | 142 | 6 |
| 234 | `templates\logistics\profile.html` | HTML-шаблон раздела логистики: profile | 55 | 3 |
| 235 | `templates\logistics\route_detail.html` | HTML-шаблон раздела логистики: route detail | 229 | 9 |
| 236 | `templates\logistics\route_form.html` | HTML-шаблон раздела логистики: route form | 31 | 2 |
| 237 | `templates\logistics\routes.html` | HTML-шаблон раздела логистики: routes | 45 | 2 |
| 238 | `templates\manager_clients.html` | HTML-шаблон раздела интерфейса: manager clients | 63 | 3 |
| 239 | `templates\manager_dashboard.html` | HTML-шаблон раздела интерфейса: manager dashboard | 206 | 9 |
| 240 | `templates\manager_orders.html` | HTML-шаблон раздела интерфейса: manager orders | 63 | 3 |
| 241 | `templates\manager\proof_review_list.html` | HTML-шаблон раздела manager: proof review list | 81 | 4 |
| 242 | `templates\orders\archive.html` | HTML-шаблон раздела заказов: archive | 61 | 3 |
| 243 | `templates\orders\delete.html` | HTML-шаблон раздела заказов: delete | 26 | 1 |
| 244 | `templates\orders\form.html` | HTML-шаблон раздела заказов: form | 508 | 20 |
| 245 | `templates\orders\list.html` | HTML-шаблон раздела заказов: list | 159 | 7 |
| 246 | `templates\orders\picker_detail.html` | HTML-шаблон раздела заказов: picker detail | 126 | 6 |
| 247 | `templates\orders\picker_list.html` | HTML-шаблон раздела заказов: picker list | 65 | 3 |
| 248 | `templates\partials\chat_menu_item.html` | HTML-шаблон раздела общих фрагментов интерфейса: chat menu item | 6 | 1 |
| 249 | `templates\partials\sidebars\admin.html` | HTML-шаблон раздела общих фрагментов интерфейса: admin | 43 | 3 |
| 250 | `templates\partials\sidebars\courier.html` | HTML-шаблон раздела общих фрагментов интерфейса: courier | 15 | 1 |
| 251 | `templates\partials\sidebars\logistic.html` | HTML-шаблон раздела общих фрагментов интерфейса: logistic | 24 | 2 |
| 252 | `templates\partials\sidebars\manager.html` | HTML-шаблон раздела общих фрагментов интерфейса: manager | 31 | 2 |
| 253 | `templates\partials\sidebars\picker.html` | HTML-шаблон раздела общих фрагментов интерфейса: picker | 15 | 1 |
| 254 | `templates\portal\base_portal.html` | HTML-шаблон раздела клиентского портала: base portal | 27 | 2 |
| 255 | `templates\portal\client_form.html` | HTML-шаблон раздела клиентского портала: client form | 66 | 3 |
| 256 | `templates\portal\clients_list.html` | HTML-шаблон раздела клиентского портала: clients list | 27 | 2 |
| 257 | `templates\portal\delivery_plan.html` | HTML-шаблон раздела клиентского портала: delivery plan | 17 | 1 |
| 258 | `templates\portal\login.html` | HTML-шаблон раздела клиентского портала: login | 30 | 2 |
| 259 | `templates\portal\logistic_dashboard.html` | HTML-шаблон раздела клиентского портала: logistic dashboard | 20 | 1 |
| 260 | `templates\portal\manager_dashboard.html` | HTML-шаблон раздела клиентского портала: manager dashboard | 28 | 1 |
| 261 | `templates\portal\order_form.html` | HTML-шаблон раздела клиентского портала: order form | 17 | 1 |
| 262 | `templates\portal\orders_list.html` | HTML-шаблон раздела клиентского портала: orders list | 25 | 2 |
| 263 | `templates\portal\picker_dashboard.html` | HTML-шаблон раздела клиентского портала: picker dashboard | 18 | 1 |
| 264 | `templates\portal\sysadmin_dashboard.html` | HTML-шаблон раздела клиентского портала: sysadmin dashboard | 7 | 1 |
| 265 | `templates\registration\login.html` | HTML-шаблон раздела регистрации: login | 39 | 2 |
| 266 | `templates\reports\analytics.html` | HTML-шаблон раздела reports: analytics | 369 | 14 |
| 267 | `templates\reports\form.html` | HTML-шаблон раздела reports: form | 37 | 2 |
| 268 | `templates\reports\list.html` | HTML-шаблон раздела reports: list | 70 | 3 |
| 269 | `tests\__init__.py` | Тестовый модуль:   init   | 1 | 1 |
| 270 | `tests\integration\__init__.py` | Тестовый модуль:   init   | 1 | 1 |
| 271 | `tests\integration\test_app_flows.py` | Тестовый модуль: test app flows | 451 | 19 |
| 272 | `tests\security\__init__.py` | Тестовый модуль:   init   | 1 | 1 |
| 273 | `tests\security\test_security_flows.py` | Тестовый модуль: test security flows | 127 | 5 |
| 274 | `tests\test_admin_panel_forms.py` | Тестовый модуль: test admin panel forms | 77 | 3 |
| 275 | `tests\test_analytics_exports.py` | Тестовый модуль: test analytics exports | 140 | 6 |
| 276 | `tests\test_api_validation.py` | Тестовый модуль: test api validation | 76 | 3 |
| 277 | `tests\test_communications.py` | Тестовый модуль: test communications | 62 | 3 |
| 278 | `tests\test_field_validators.py` | Тестовый модуль: test field validators | 37 | 2 |
| 279 | `tests\test_portal_forms.py` | Тестовый модуль: test portal forms | 50 | 2 |
| 280 | `tests\test_postgres_backups.py` | Тестовый модуль: test postgres backups | 114 | 5 |
| 281 | `tests\test_routing.py` | Тестовый модуль: test routing | 13 | 1 |
| 282 | `tools\build_code_docx.py` | Вспомогательный инструмент проекта: build code docx | 219 | 6 |
