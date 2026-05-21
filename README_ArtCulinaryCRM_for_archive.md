# АРТ КУЛИНАРИЯ CRM

Корпоративная CRM-система для ООО «АРТ КУЛИНАРИЯ». Проект автоматизирует работу с клиентами, заказами, производственными ограничениями, сборкой заказов, доставками, маршрутами, внутренними сообщениями, отчетами и резервными копиями.

## 1. Технологии

- Python 3.12+
- Django 6.0.1
- PostgreSQL 16+
- Django REST Framework
- drf-spectacular для OpenAPI/Swagger-документации

Демонстрационный сервер:

```text
http://155.212.209.221/
```

## 2. Демо-аккаунты

После загрузки полного демо через команду `seed_full_quality_demo --fresh` доступны следующие пользователи:

| Роль | Логин | Пароль |
| --- | --- | --- |
| Менеджер | `manager_quality` | `ManagerDemo123!` |
| Логист | `logistic_quality` | `LogisticDemo123!` |
| Сборщик | `picker_quality` | `PickerDemo123!` |
| Администратор | `admin_quality` | `AdminDemo123!` |
| Курьер | `courier_quality_01` | `CourierDemo123!` |

Также создаются курьеры `courier_quality_02` ... `courier_quality_05` с тем же паролем `CourierDemo123!`.

## 3. Структура проекта

Основные приложения:

- `crm` — базовые модели: пользователи, роли, клиенты, блюда, ингредиенты, заказы, доставки, маршруты.
- `accounts` — вход, выход, восстановление пароля и перенаправление пользователей по ролям.
- `dashboard` — кабинеты менеджера, логиста, сборщика и администратора.
- `clients` — работа с клиентами и контактами.
- `orders` — оформление заказов, статусы, архив, рабочее место сборщика.
- `logistics` — доставки, курьеры, маршруты, остановки, подтверждения доставки.
- `reports` — отчеты, аналитика и экспорт.
- `admin_panel` — пользовательская административная панель, роли, пользователи, резервные копии.
- `communications` — внутренние сообщения и комментарии к объектам.
- `factory_crm` — настройки Django, маршруты проекта, WSGI/ASGI.

В корне проекта должны быть файлы `manage.py`, `requirements.txt` и `.env.example`.

## 4. Получение проекта

### Вариант A: из zip-архива

1. Скачать или получить архив проекта, например `ArtCulinaryCRM.zip`.
2. Распаковать архив через «Извлечь все» / `Extract All` / «Распаковать».
3. Открыть распакованную папку проекта.
4. Убедиться, что внутри есть файл `manage.py`.

### Вариант B: из GitHub

```bash
git clone https://github.com/Elizavetalii/culinary
cd culinary
```

Если репозиторий был переименован, нужно перейти в фактическую папку, где лежит `manage.py`.

## 5. Установка программ

Для запуска проекта нужны Python, PostgreSQL и Git. Visual Studio Code не обязателен, но удобен для просмотра кода.

### Windows

1. Установить Python 3.12 или новее: https://www.python.org/downloads/
2. Во время установки Python поставить галочку `Add Python to PATH`.
3. Установить PostgreSQL 16 или новее: https://www.postgresql.org/download/windows/
4. Во время установки PostgreSQL запомнить пароль пользователя `postgres`.
5. Установить Git: https://git-scm.com/download/win
6. При необходимости установить Visual Studio Code: https://code.visualstudio.com/

Проверка:

```powershell
python --version
git --version
psql --version
```

### macOS

Удобнее всего установить программы через Homebrew. Если Homebrew не установлен, его можно поставить с сайта https://brew.sh/

```bash
brew install python@3.12 postgresql@16 git
brew services start postgresql@16
```

Проверка:

```bash
python3 --version
git --version
psql --version
```

Альтернативно на macOS можно использовать Postgres.app, если он уже установлен.

## 6. Открытие проекта в редакторе

Если используется Visual Studio Code:

1. Открыть Visual Studio Code.
2. Нажать `File` -> `Open Folder`.
3. Выбрать папку проекта.
4. Открыть встроенный терминал: `Terminal` -> `New Terminal`.
5. Все дальнейшие команды выполнять из папки, где находится `manage.py`.

Проверить текущую папку:

Windows:

```powershell
dir
```

macOS:

```bash
ls
```

В списке файлов должен быть `manage.py`.

## 7. Создание виртуального окружения

### Windows

Перейти в папку проекта, например:

```powershell
cd "C:\Users\ИмяПользователя\Desktop\ArtCulinaryCRM"
```

Создать и активировать окружение:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Если окружение активировалось, в начале строки появится `(.venv)`.

Если PowerShell запрещает запуск скриптов:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\activate
```

### macOS

Перейти в папку проекта, например:

```bash
cd ~/Desktop/ArtCulinaryCRM
```

Создать и активировать окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Если окружение активировалось, в начале строки появится `(.venv)`.

## 8. Установка зависимостей

Убедиться, что виртуальное окружение активно. Затем выполнить:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Установка может занять несколько минут. После завершения не должно быть строк `ERROR`.

## 9. Создание базы данных PostgreSQL

Проект работает с PostgreSQL. По умолчанию используется база `art_culinary_crm`.

### Windows через pgAdmin

1. Открыть pgAdmin.
2. Подключиться к серверу PostgreSQL.
3. В левой панели открыть `Servers` -> `PostgreSQL 16` -> `Databases`.
4. Нажать правой кнопкой мыши на `Databases`.
5. Выбрать `Create` -> `Database`.
6. В поле `Database` указать `art_culinary_crm`.
7. В поле `Owner` выбрать пользователя `postgres` или отдельного пользователя проекта.
8. Нажать `Save`.

### Windows через psql

Если используется пользователь `postgres`:

```powershell
psql -U postgres
```

Внутри PostgreSQL:

```sql
CREATE DATABASE art_culinary_crm;
\q
```

### macOS через терминал

Если PostgreSQL установлен через Homebrew:

```bash
createdb art_culinary_crm
```

Если требуется создать базу от пользователя `postgres`:

```bash
psql -U postgres
```

Внутри PostgreSQL:

```sql
CREATE DATABASE art_culinary_crm;
\q
```

## 10. Настройка `.env`

Файл `.env` хранит локальные настройки проекта: ключ Django, подключение к базе, режим отладки, email и пути к утилитам PostgreSQL.

Создать `.env` из примера:

Windows:

```powershell
copy .env.example .env
```

macOS:

```bash
cp .env.example .env
```

Пример для локального запуска через пользователя `postgres`:

```env
DJANGO_SECRET_KEY=dev-secret-key-change-me
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
GOOGLE_MAPS_API_KEY=

DB_NAME=art_culinary_crm
DB_USER=postgres
DB_PASSWORD=ваш_пароль_postgres
DB_HOST=localhost
DB_PORT=5432

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.mail.ru
EMAIL_PORT=465
EMAIL_USE_SSL=true
EMAIL_USE_TLS=false
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=

PG_DUMP_PATH=pg_dump
PSQL_PATH=psql
```

Важно:

- если база создана под пользователем `postgres`, в `DB_USER` нужно указать `postgres`;
- если используется отдельный пользователь из `.env.example`, например `artculinary_user`, его нужно заранее создать в PostgreSQL и выдать ему права на базу;
- для локальной проверки удобно оставить `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend`, тогда письма восстановления пароля будут выводиться в терминал;
- не передавайте проверяющему файл `.env` с реальными паролями;
- файл `.env.example` можно оставлять в архиве, а `.env` лучше не включать.

## 11. Применение миграций

Миграции создают таблицы базы данных:

```bash
python manage.py migrate
```

Если все настроено правильно, в терминале появятся строки вида:

```text
Applying ... OK
```

## 12. Создание администратора

Администратор нужен для входа в систему и проверки административных функций:

```bash
python manage.py createsuperuser
```

Пример заполнения:

```text
Username: admin
Email address: admin@example.com
Full name: Администратор
Password:
Password (again):
```

Пароль при вводе не отображается. Это нормально.

## 13. Загрузка демонстрационных данных

Быстрый вариант:

```bash
python manage.py seed_demo
```

Полный вариант для проверки проекта:

```bash
python manage.py seed_full_quality_demo --fresh
```

Команда `--fresh` очищает демонстрационные бизнес-данные и заново наполняет базу. Суперпользователи сохраняются.

Для команды `seed_demo` доступны аккаунты:

| Роль | Логин | Пароль |
| --- | --- | --- |
| Менеджер | `manager_demo` | `ManagerDemo123!` |
| Логист | `logistic_demo` | `LogisticDemo123!` |
| Сборщик | `picker_demo` | `PickerDemo123!` |
| Администратор | `admin_demo` | `AdminDemo123!` |
| Курьер | `courier_demo` | `CourierDemo123!` |

## 14. Сбор статических файлов

Для локальной разработки этот шаг часто не обязателен, но для полной проверки его лучше выполнить:

```bash
python manage.py collectstatic --noinput
```

Статические файлы будут собраны в папку `staticfiles`.

## 15. Запуск проекта

Запустить сервер разработки:

```bash
python manage.py runserver
```

Если запуск успешный, появится строка:

```text
Starting development server at http://127.0.0.1:8000/
```

Открыть в браузере:

```text
http://127.0.0.1:8000/
```

Остановить сервер можно сочетанием клавиш `Ctrl+C` в терминале.

## 16. Основные адреса системы

| Раздел | Адрес |
| --- | --- |
| Вход в систему | http://127.0.0.1:8000/login/ |
| Автоматический переход в кабинет по роли | http://127.0.0.1:8000/dashboard/ |
| Кабинет менеджера | http://127.0.0.1:8000/dashboard/manager/ |
| Кабинет логиста | http://127.0.0.1:8000/dashboard/logistic/ |
| Кабинет сборщика | http://127.0.0.1:8000/dashboard/picker/ |
| Кабинет администратора | http://127.0.0.1:8000/dashboard/admin/ |
| Клиенты | http://127.0.0.1:8000/clients/ |
| Заказы | http://127.0.0.1:8000/orders/ |
| Архив заказов | http://127.0.0.1:8000/orders/archive/ |
| Заказы для сборщика | http://127.0.0.1:8000/orders/picker/ |
| Логистика и доставки | http://127.0.0.1:8000/logistics/ |
| Курьеры | http://127.0.0.1:8000/logistics/couriers/ |
| Маршруты | http://127.0.0.1:8000/logistics/routes/ |
| Маршруты курьера | http://127.0.0.1:8000/logistics/courier/routes/ |
| Отчеты | http://127.0.0.1:8000/reports/ |
| Аналитика | http://127.0.0.1:8000/reports/analytics/ |
| Административная панель проекта | http://127.0.0.1:8000/admin-panel/ |
| Пользователи | http://127.0.0.1:8000/admin-panel/users/ |
| Роли | http://127.0.0.1:8000/admin-panel/roles/ |
| Резервные копии | http://127.0.0.1:8000/admin-panel/backups/ |
| Матрица доступа | http://127.0.0.1:8000/admin-panel/access/ |
| Проверка данных | http://127.0.0.1:8000/admin-panel/data-check/ |
| Чаты и сообщения | http://127.0.0.1:8000/chat/ |
| REST API | http://127.0.0.1:8000/api/ |
| OpenAPI-схема | http://127.0.0.1:8000/api/schema/ |
| Swagger UI | http://127.0.0.1:8000/api/docs/ |

## 17. Роли пользователей

### Администратор системы

Администратор управляет пользователями и ролями, проверяет данные, работает с резервными копиями, смотрит административную аналитику и имеет доступ к служебным разделам.

### Менеджер

Менеджер ведет клиентскую базу, создает и редактирует клиентов, фиксирует взаимодействия, оформляет заказы, контролирует статусы и просматривает отчеты по продажам.

### Логист

Логист работает с доставками, курьерами, маршрутами и остановками. Он назначает курьеров, планирует доставку и контролирует выполнение маршрутов.

### Сборщик заказов

Сборщик видит заказы, которые нужно подготовить, проверяет позиции заказа и обновляет состояние сборки.

### Курьер

Курьер видит назначенные маршруты, открывает карточки доставок, обновляет статусы остановок и загружает подтверждения доставки.

## 18. Что проверять после запуска

Рекомендуемый сценарий проверки:

1. Открыть http://127.0.0.1:8000/login/
2. Войти под суперпользователем или демо-аккаунтом.
3. Проверить переход в кабинет по роли через `/dashboard/`.
4. Открыть список клиентов и создать тестового клиента.
5. Создать заказ для клиента.
6. Проверить изменение статуса заказа.
7. Открыть раздел логистики и посмотреть доставки.
8. Создать или открыть маршрут.
9. Войти под курьером и проверить назначенные маршруты.
10. Загрузить подтверждение доставки, если в маршруте есть остановки.
11. Открыть отчеты и аналитику.
12. Проверить экспорт отчета.
13. Открыть чат и отправить сообщение другому пользователю.
14. Открыть административную панель и проверить пользователей, роли, матрицу доступа и резервные копии.
15. Открыть Swagger UI и убедиться, что API-документация генерируется.

## 19. REST API

Проект содержит REST API для основных сущностей CRM.

Документация API доступна после запуска сервера:

```text
http://127.0.0.1:8000/api/docs/
```

Получение JWT-токена:

```text
POST http://127.0.0.1:8000/api/token/
```

Обновление JWT-токена:

```text
POST http://127.0.0.1:8000/api/token/refresh/
```

Основные API-разделы:

- `/api/users/`
- `/api/roles/`
- `/api/clients/`
- `/api/orders/`
- `/api/deliveries/`
- `/api/routes/`
- `/api/dishes/`
- `/api/ingredients/`
- `/api/techcards/`

## 20. Резервное копирование

В административной панели есть раздел резервных копий:

```text
http://127.0.0.1:8000/admin-panel/backups/
```

Для работы резервного копирования Django использует системные утилиты PostgreSQL:

- `pg_dump` — создание резервной копии;
- `psql` — восстановление из резервной копии.

Если система не находит эти утилиты, нужно указать полные пути в `.env`.

Пример для Windows:

```env
PG_DUMP_PATH=C:\Program Files\PostgreSQL\16\bin\pg_dump.exe
PSQL_PATH=C:\Program Files\PostgreSQL\16\bin\psql.exe
```

Пример для macOS через Homebrew:

```env
PG_DUMP_PATH=/opt/homebrew/opt/postgresql@16/bin/pg_dump
PSQL_PATH=/opt/homebrew/opt/postgresql@16/bin/psql
```

На Mac с Intel путь Homebrew может начинаться с `/usr/local`, а не с `/opt/homebrew`.

## 21. Запуск проверок

Базовая проверка Django:

```bash
python manage.py check
```

Запуск тестов Django:

```bash
python manage.py test
```

Если используется `pytest`, его нужно установить отдельно или добавить в зависимости, затем выполнить:

```bash
pytest
```

## 22. Частые ошибки и решения

### Ошибка: `ModuleNotFoundError`

Причина: не установлены зависимости или не активировано виртуальное окружение.

Решение:

```bash
pip install -r requirements.txt
```

Проверить, что в терминале есть `(.venv)`.

### Ошибка: `could not connect to server`

Причина: PostgreSQL не запущен или неверные настройки в `.env`.

Решение:

1. Проверить, что PostgreSQL запущен.
2. Проверить `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`.
3. Проверить, что база `art_culinary_crm` создана.
4. Повторить `python manage.py migrate`.

### Ошибка: `database does not exist`

Причина: база данных не создана.

Решение: создать базу `art_culinary_crm` через pgAdmin, `createdb` или `psql`.

### Ошибка: `password authentication failed`

Причина: неправильный пароль PostgreSQL в `.env`.

Решение: указать правильный пароль в `DB_PASSWORD`.

### Ошибка: `relation does not exist`

Причина: не применены миграции.

Решение:

```bash
python manage.py migrate
```

### Ошибка: `DisallowedHost`

Причина: адрес не указан в `DJANGO_ALLOWED_HOSTS`.

Для локального запуска:

```env
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

Если проект запускается на сервере, добавить IP или домен:

```env
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,155.212.209.221
```

### Не загружаются CSS или изображения

Решение:

```bash
python manage.py collectstatic --noinput
```

После этого обновить страницу в браузере с очисткой кэша: `Ctrl+F5` на Windows или `Cmd+Shift+R` на macOS.

### Письма восстановления пароля не приходят

Для локальной проверки лучше использовать вывод писем в терминал:

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Если нужен реальный SMTP, нужно заполнить `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` и другие email-переменные в `.env`.

### PowerShell не активирует виртуальное окружение

Решение:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\activate
```

### Команда `pg_dump` или `psql` не найдена

Причина: PostgreSQL установлен, но его папка `bin` не добавлена в `PATH`.

Решение: указать полные пути в `.env` через `PG_DUMP_PATH` и `PSQL_PATH`.

## 23. Краткий запуск без пояснений

### Windows

```powershell
cd "C:\Users\ИмяПользователя\Desktop\ArtCulinaryCRM"
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_full_quality_demo --fresh
python manage.py collectstatic --noinput
python manage.py runserver
```

### macOS

```bash
cd ~/Desktop/ArtCulinaryCRM
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_full_quality_demo --fresh
python manage.py collectstatic --noinput
python manage.py runserver
```

Перед командами `migrate` и `runserver` нужно создать базу PostgreSQL и проверить настройки `.env`.

## 24. Что не включать в архив

В архив для передачи проверяющему не нужно включать:

- `.env` с реальными паролями;
- папку `.venv`;
- папки `__pycache__`;
- файлы `.DS_Store`;
- локальные временные файлы редактора.

В архиве достаточно оставить исходный код проекта, `requirements.txt`, `.env.example`, миграции, шаблоны, статические файлы, документацию и этот README-файл.
