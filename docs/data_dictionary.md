# Таблица 1 - Словарь данных информационной системы ArtCulinaryCRM

Словарь составлен по Django-моделям приложения. Обозначения ключей: `PK` - первичный ключ, `FK` - внешний ключ, `UK` - уникальный ключ.

| Ключ | Поле | Тип данных | Обязательность заполнения | Описание |
|---|---|---|---|---|
|  | **Таблица admin_panel_backup** |  |  | Резервная копия |
| PK | id | Bigint | Not null | Идентификатор записи |
|  | file_path | Varchar(500) | Not null | Файл |
|  | status | Varchar(20) | Not null | Статус (created / restored / failed) |
| FK | created_by | Bigint | Null | Ссылка на crm_user |
|  | created_at | Datetime | Not null | Создан, заполняется автоматически при создании |

|  | **Таблица admin_panel_backupschedule** |  |  | Расписание резервного копирования |
| PK | id | Bigint | Not null | Идентификатор записи |
|  | frequency | Varchar(20) | Not null | Частота (daily / weekly / monthly) |
|  | is_active | Boolean | Not null | Активно |
|  | updated_at | Datetime | Not null | Обновлено, обновляется автоматически |

|  | **Таблица communications_directmessage** |  |  | Личное сообщение |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | sender | Bigint | Not null | Ссылка на crm_user |
| FK | recipient | Bigint | Not null | Ссылка на crm_user |
|  | body | Text | Not null | Сообщение |
|  | created_at | Datetime | Not null | Отправлено |
|  | read_at | Datetime | Null | Прочитано |

|  | **Таблица communications_entitycomment** |  |  | Комментарий к сущности |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | author | Bigint | Not null | Ссылка на crm_user |
| FK | content_type | Bigint | Not null | Ссылка на django_content_type |
|  | object_id | Positive integer | Not null | Идентификатор объекта |
|  | body | Text | Not null | Комментарий |
|  | created_at | Datetime | Not null | Создан |
|  | updated_at | Datetime | Not null | Обновлён, обновляется автоматически |

|  | **Таблица crm_auditlog** |  |  | Аудит |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | actor | Bigint | Null | Ссылка на crm_user |
|  | actor_role | Varchar(64) | Not null | Роль |
|  | object_type | Varchar(64) | Not null | Тип объекта |
|  | object_id | Positive integer | Not null | Идентификатор объекта |
|  | field_name | Varchar(64) | Not null | Поле |
|  | old_value | Text | Not null | Старое значение |
|  | new_value | Text | Not null | Новое значение |
|  | reason | Text | Not null | Причина |
|  | created_at | Datetime | Not null | Время, заполняется автоматически при создании |

|  | **Таблица crm_client** |  |  | Клиент |
| PK | id | Bigint | Not null | Идентификатор записи |
|  | name | Varchar(255) | Not null | Название |
|  | client_type | Varchar(32) | Not null | Тип (store / cafe / restaurant / distributor / other) |
|  | inn | Varchar(20) | Not null | ИНН |
|  | kpp | Varchar(20) | Not null | КПП |
|  | default_delivery_address | Varchar(255) | Not null | Адрес доставки по умолчанию |
|  | email | Varchar(254) | Not null | Email |
|  | phone | Varchar(32) | Not null | Телефон |
|  | status | Varchar(20) | Not null | Статус (prospect / active / paused / lost) |
| FK | current_stage | Bigint | Null | Ссылка на crm_cooperationstage |
| FK | responsible_manager | Bigint | Null | Ссылка на crm_user |
|  | created_at | Datetime | Null | Создан, заполняется автоматически при создании |
|  | daily_max_weight_kg | Decimal(10,2) | Null | Макс. вес в день (кг) |
|  | daily_min_qty | Decimal(10,2) | Null | Мин. объём заказа |
|  | guaranteed_volume_kg | Decimal(10,2) | Null | Гарантированный объём (кг) |

|  | **Таблица crm_clientallowedtechcard** |  |  | Разрешённая техкарта клиента |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | client | Bigint | Not null | Ссылка на crm_client |
| FK | tech_card | Bigint | Not null | Ссылка на crm_techcard |
| UK | client, tech_card | Composite | unique | Составной уникальный ключ таблицы crm_clientallowedtechcard |

|  | **Таблица crm_clientcontact** |  |  | Контакт клиента |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | client | Bigint | Not null | Ссылка на crm_client |
|  | full_name | Varchar(255) | Not null | ФИО |
|  | position | Varchar(128) | Not null | Должность |
|  | phone | Varchar(32) | Not null | Телефон |
|  | email | Varchar(254) | Not null | Email |
|  | is_primary | Boolean | Not null | Основной |

|  | **Таблица crm_clientstagehistory** |  |  | История этапов клиента |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | client | Bigint | Not null | Ссылка на crm_client |
| FK | stage | Bigint | Null | Ссылка на crm_cooperationstage |
| FK | changed_by | Bigint | Null | Ссылка на crm_user |
|  | changed_at | Datetime | Not null | changed at |
|  | comment | Text | Not null | Комментарий |

|  | **Таблица crm_cooperationstage** |  |  | Этап сотрудничества |
| PK | id | Bigint | Not null | Идентификатор записи |
|  | name | Varchar(128) | Not null | Название этапа |
|  | order | Positive smallint | Not null | Порядок |
|  | is_active | Boolean | Not null | Активен |

|  | **Таблица crm_courier** |  |  | Курьер |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK, UK | user | Bigint | Not null, unique | Уникальная ссылка на crm_user |
|  | transport_type | Varchar(64) | Not null | Тип транспорта |
|  | payload_capacity_kg | Decimal(10,2) | Null | Грузоподъёмность (кг) |
|  | cargo_volume_m3 | Decimal(10,2) | Null | Объём кузова (м³) |
|  | cargo_length_cm | Decimal(10,2) | Null | Длина кузова (см) |
|  | cargo_width_cm | Decimal(10,2) | Null | Ширина кузова (см) |
|  | cargo_height_cm | Decimal(10,2) | Null | Высота кузова (см) |
|  | current_lat | Decimal(9,6) | Null | Текущая широта |
|  | current_lng | Decimal(9,6) | Null | Текущая долгота |
|  | max_weight | Decimal(10,2) | Null | Макс. вес (кг) |
|  | max_volume | Decimal(10,2) | Null | Макс. объём (м³) |
|  | current_latitude | Decimal(9,6) | Null | Текущая широта (альт) |
|  | current_longitude | Decimal(9,6) | Null | Текущая долгота (альт) |
|  | location_updated_at | Datetime | Null | Обновление геолокации |
|  | experience_years | Positive smallint | Not null | Опыт (лет) |
|  | status | Varchar(20) | Not null | Статус (Свободен / Занят / В рейсе) |
|  | zone | Varchar(128) | Not null | Зона |

|  | **Таблица crm_courierassignment** |  |  | Назначение курьера |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | courier | Bigint | Not null | Ссылка на crm_courier |
| FK | route | Bigint | Not null | Ссылка на crm_route |
|  | assigned_at | Datetime | Not null | Дата назначения |
| UK | courier, route | Composite | unique | Составной уникальный ключ таблицы crm_courierassignment |

|  | **Таблица crm_delivery** |  |  | Доставка |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | order | Bigint | Not null | Ссылка на crm_order |
| FK | courier | Bigint | Null | Ссылка на crm_courier |
| FK | route | Bigint | Null | Ссылка на crm_route |
|  | status | Varchar(20) | Not null | Статус (Не назначено / Запланировано / В пути / Доставлено / Отменено) |
|  | planned_at | Datetime | Null | Плановая дата/время |
|  | departure_time | Datetime | Null | Время выезда |
|  | delivered_at | Datetime | Null | Доставлено |
|  | delivery_date | Date | Null | Дата доставки |
|  | address | Varchar(255) | Not null | Адрес |
|  | note | Text | Not null | Примечание |
|  | is_sent | Boolean | Not null | Отправлен |
|  | cargo_weight_kg | Decimal(10,2) | Null | Вес груза (кг) |
|  | cargo_volume_m3 | Decimal(10,2) | Null | Объём груза (м³) |
|  | cargo_length_cm | Decimal(10,2) | Null | Длина груза (см) |
|  | cargo_width_cm | Decimal(10,2) | Null | Ширина груза (см) |
|  | cargo_height_cm | Decimal(10,2) | Null | Высота груза (см) |

|  | **Таблица crm_dish** |  |  | Блюдо каталога |
| PK | id | Bigint | Not null | Идентификатор записи |
|  | name | Varchar(128) | Not null | Название |
|  | unit | Varchar(32) | Not null | Единица измерения |
|  | base_uom | Varchar(8) | Not null | Базовая единица (kg / pcs) |
|  | quantity_scale | Positive smallint | Not null | Знаков после запятой |
|  | is_active | Boolean | Not null | Активно |
| FK | created_by | Bigint | Null | Ссылка на crm_user |
|  | unit_weight_kg | Decimal(10,3) | Null | Вес единицы (кг) |
|  | min_batch_qty | Decimal(10,3) | Null | Мин. партия |
|  | batch_multiple_qty | Decimal(10,3) | Null | Кратность партии |
|  | daily_capacity | Decimal(12,3) | Null | Суточная мощность |
|  | default_price | Decimal(12,2) | Null | Базовая цена |

|  | **Таблица crm_dishequipmentrequirement** |  |  | Требование оборудования |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | dish | Bigint | Not null | Ссылка на crm_dish |
| FK | equipment | Bigint | Not null | Ссылка на crm_equipment |
|  | minutes_per_unit | Decimal(10,2) | Not null | Минут на единицу |
| UK | dish, equipment | Composite | unique | Составной уникальный ключ таблицы crm_dishequipmentrequirement |

|  | **Таблица crm_equipment** |  |  | Оборудование |
| PK | id | Bigint | Not null | Идентификатор записи |
|  | name | Varchar(128) | Not null | Оборудование |
|  | capacity_per_hour | Decimal(10,2) | Null | Производительность/час |
|  | available_hours | Decimal(10,2) | Null | Доступные часы |

|  | **Таблица crm_equipmentreservation** |  |  | Резерв оборудования |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | order | Bigint | Not null | Ссылка на crm_order |
| FK | equipment | Bigint | Not null | Ссылка на crm_equipment |
|  | production_date | Date | Not null | Дата производства |
|  | hours | Decimal(10,2) | Not null | Часы |

|  | **Таблица crm_ingredient** |  |  | Ингредиент |
| PK | id | Bigint | Not null | Идентификатор записи |
| UK | name | Varchar(128) | Not null, unique | Название |
|  | is_active | Boolean | Not null | Активен |

|  | **Таблица crm_ingredientreservation** |  |  | Резерв ингредиента |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | order | Bigint | Not null | Ссылка на crm_order |
| FK | ingredient | Bigint | Not null | Ссылка на crm_ingredient |
|  | production_date | Date | Not null | Дата производства |
|  | quantity | Decimal(12,3) | Not null | Количество |

|  | **Таблица crm_ingredientstock** |  |  | Остаток ингредиента |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK, UK | ingredient | Bigint | Not null, unique | Уникальная ссылка на crm_ingredient |
|  | quantity | Decimal(12,3) | Not null | Остаток |

|  | **Таблица crm_interaction** |  |  | Взаимодействие |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | client | Bigint | Not null | Ссылка на crm_client |
| FK | manager | Bigint | Null | Ссылка на crm_user |
|  | interaction_type | Varchar(20) | Not null | Тип (call / meeting / email / message / other) |
|  | note | Text | Not null | Заметка |
|  | happened_at | Datetime | Not null | Дата/время |

|  | **Таблица crm_logisticianprofile** |  |  | Профиль логиста |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK, UK | user | Bigint | Not null, unique | Уникальная ссылка на crm_user |
|  | region | Varchar(128) | Not null | Регион |
|  | city | Varchar(128) | Not null | Город |
|  | transport_types | JSON | Not null | Доступные типы транспорта |
|  | timezone | Varchar(64) | Not null | Часовой пояс |
|  | map_show_traffic | Boolean | Not null | Показывать пробки |
|  | preferred_route_type | Varchar(16) | Not null | Предпочтительный тип маршрута (fastest / safest / shortest) |

|  | **Таблица crm_order** |  |  | Заказ |
| PK | id | Bigint | Not null | Идентификатор записи |
| UK | order_number | Varchar(50) | Not null, unique | Номер заказа |
| FK | client | Bigint | Not null | Ссылка на crm_client |
| FK | manager | Bigint | Null | Ссылка на crm_user |
|  | address | Varchar(255) | Not null | Адрес доставки |
|  | status | Varchar(64) | Not null | Статус (Черновик / На проверке / Подтвержден производством / В производстве / Готов к отгрузке / Отгружен / Отменен) |
|  | delivery_date | Date | Null | Дата доставки |
|  | delivery_time | Time | Null | Время доставки |
|  | delivery_type | Varchar(32) | Not null | Тип доставки (Регулярная / Разовая / Срочная) |
|  | production_date | Date | Null | Дата производства |
|  | production_shift | Varchar(32) | Not null | Смена |
|  | production_window_start | Time | Null | Окно производства (с) |
|  | production_window_end | Time | Null | Окно производства (до) |
|  | comments | Text | Not null | Комментарии |
|  | total_amount | Decimal(12,2) | Not null | Сумма итого |
|  | is_archived | Boolean | Not null | В архиве |
|  | created_at | Datetime | Not null | created at, заполняется автоматически при создании |
|  | updated_at | Datetime | Not null | updated at, обновляется автоматически |

|  | **Таблица crm_orderitem** |  |  | Позиция заказа |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | order | Bigint | Not null | Ссылка на crm_order |
| FK | dish | Bigint | Null | Ссылка на crm_dish |
| FK | ingredient | Bigint | Null | Ссылка на crm_ingredient |
| FK | custom_tech_card | Bigint | Null | Ссылка на crm_techcard |
|  | quantity | Decimal(10,3) | Not null | Кол-во |
|  | unit_price | Decimal(10,2) | Not null | Цена |
|  | line_total | Decimal(12,2) | Not null | Сумма |
|  | supply_type | Varchar(64) | Not null | Тип поставки/заявки |
|  | picked_quantity | Decimal(10,3) | Not null | Собрано фактически |
|  | item_status | Varchar(20) | Not null | Статус позиции (not_started / in_progress / done / out_of_stock / replaced) |
|  | item_comment | Varchar(255) | Not null | Комментарий по позиции |
|  | replacement_text | Varchar(255) | Not null | Замена |

|  | **Таблица crm_pickingsession** |  |  | Сборка заказа |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK, UK | order | Bigint | Not null, unique | Уникальная ссылка на crm_order |
| FK | picker | Bigint | Null | Ссылка на crm_user |
|  | note | Text | Not null | Примечание сборщика |
|  | started_at | Datetime | Null | Начата |
|  | finished_at | Datetime | Null | Завершена |
|  | updated_at | Datetime | Not null | Обновлено, обновляется автоматически |

|  | **Таблица crm_productionreservation** |  |  | Резерв мощности производства |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | order | Bigint | Not null | Ссылка на crm_order |
|  | production_date | Date | Not null | Дата производства |
|  | weight_kg | Decimal(12,3) | Not null | Вес (кг) |

|  | **Таблица crm_role** |  |  | Роль |
| PK | id | Bigint | Not null | Идентификатор записи |
| UK | name | Varchar(64) | Not null, unique | name |

|  | **Таблица crm_route** |  |  | Маршрут |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | logistician | Bigint | Null | Ссылка на crm_user |
|  | planned_date | Date | Not null | Дата маршрута |
|  | status | Varchar(20) | Not null | Статус (Черновик / Запланирован / Опубликован / Выполняется / Завершён) |
|  | max_duration_minutes | Positive smallint | Not null | Макс. длительность (мин) |
|  | soft_limit_stops | Positive smallint | Not null | Мягкий лимит точек |
|  | strict_mode | Boolean | Not null | Строгий режим лимита точек |
|  | notes | Text | Not null | Заметки |

|  | **Таблица crm_routestop** |  |  | Остановка маршрута |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | route | Bigint | Not null | Ссылка на crm_route |
| FK | delivery | Bigint | Not null | Ссылка на crm_delivery |
|  | sequence_index | Positive smallint | Not null | Порядок |
|  | planned_time | Datetime | Null | Плановое время |
|  | actual_time | Datetime | Null | Фактическое время |
|  | service_time_minutes | Positive smallint | Not null | Время обслуживания (мин) |
|  | note | Varchar(255) | Not null | Примечание |
|  | status | Varchar(20) | Not null | Статус (Черновик / Подтверждена / Запланирована / В пути / Доставлено / Не доставлено / Перенесено / Отменено) |
|  | delivery_date | Date | Null | Дата доставки |
|  | failure_reason | Text | Not null | Причина недоставки |
|  | proof_of_delivery | Varchar(100) | Null | Документ доставки |
|  | proof_uploaded_at | Datetime | Null | Время загрузки документа |
| FK | proof_uploaded_by | Bigint | Null | Ссылка на crm_user |
|  | proof_review_status | Varchar(32) | Not null | Статус проверки документа (Ожидает проверки / Подтверждено / Отклонено) |
|  | proof_review_comment | Text | Not null | Комментарий проверки |
|  | proof_reviewed_at | Datetime | Null | Время проверки |
| FK | proof_reviewed_by | Bigint | Null | Ссылка на crm_user |
|  | latitude | Decimal(9,6) | Null | Широта |
|  | longitude | Decimal(9,6) | Null | Долгота |

|  | **Таблица crm_techcard** |  |  | Техкарта блюда |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | dish | Bigint | Not null | Ссылка на crm_dish |
|  | version_label | Varchar(32) | Not null | Версия/номер |
|  | description | Text | Not null | Описание/технология |
|  | photo_url | Varchar(200) | Not null | Фото |
|  | is_active | Boolean | Not null | Активна |
| FK | approved_by | Bigint | Null | Ссылка на crm_user |
| UK | dish, version_label | Composite | unique | Составной уникальный ключ таблицы crm_techcard |

|  | **Таблица crm_techcardcomponent** |  |  | Состав техкарты |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | tech_card | Bigint | Not null | Ссылка на crm_techcard |
| FK | ingredient | Bigint | Not null | Ссылка на crm_ingredient |
|  | quantity | Decimal(10,3) | Not null | Количество |
|  | note | Varchar(255) | Not null | Примечание |

|  | **Таблица crm_techcardvariant** |  |  | Сорт/вариант техкарты |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | tech_card | Bigint | Not null | Ссылка на crm_techcard |
|  | quantity | Decimal(10,3) | Not null | Количество |
|  | note | Varchar(255) | Not null | Примечание |

|  | **Таблица crm_user** |  |  | Пользователь |
| PK | id | Bigint | Not null | Идентификатор записи |
|  | password | Varchar(128) | Not null | пароль |
|  | last_login | Datetime | Null | последний вход |
|  | is_superuser | Boolean | Not null | статус суперпользователя |
| UK | username | Varchar(150) | Not null, unique | имя пользователя |
|  | first_name | Varchar(150) | Not null | имя |
|  | last_name | Varchar(150) | Not null | фамилия |
|  | is_staff | Boolean | Not null | статус персонала |
|  | is_active | Boolean | Not null | активный |
|  | date_joined | Datetime | Not null | дата регистрации |
| UK | email | Varchar(254) | Not null, unique | Email |
|  | full_name | Varchar(255) | Not null | ФИО |
|  | phone | Varchar(32) | Not null | Телефон |

|  | **Таблица crm_userrole** |  |  | Роль пользователя |
| PK | id | Bigint | Not null | Идентификатор записи |
| FK | user | Bigint | Not null | Ссылка на crm_user |
| FK | role | Bigint | Not null | Ссылка на crm_role |
|  | assigned_at | Datetime | Not null | Дата назначения |
| UK | user, role | Composite | unique | Составной уникальный ключ таблицы crm_userrole |

|  | **Таблица reports_report** |  |  | Отчёт |
| PK | id | Bigint | Not null | Идентификатор записи |
|  | title | Varchar(200) | Not null | Название отчёта |
|  | period_from | Date | Not null | Период с |
|  | period_to | Date | Not null | Период по |
|  | status | Varchar(20) | Not null | Статус (draft / ready / error / validating) |
|  | validation_status | Varchar(20) | Not null | Проверка (ok / warn / error) |
|  | validation_message | Text | Not null | Результат проверки |
| FK | created_by | Bigint | Null | Ссылка на crm_user |
|  | file | Varchar(100) | Null | Файл отчёта |
|  | created_at | Datetime | Not null | Создан, заполняется автоматически при создании |
|  | updated_at | Datetime | Not null | Обновлён, обновляется автоматически |

