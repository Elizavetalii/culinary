from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Role(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField('Email', unique=True)
    full_name = models.CharField('ФИО', max_length=255)
    phone = models.CharField('Телефон', max_length=32, blank=True)
    roles = models.ManyToManyField(Role, through='UserRole', related_name='users', blank=True)

    REQUIRED_FIELDS = ['full_name', 'email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.full_name or self.username


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'role')
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'

    def __str__(self):
        return f"{self.user} → {self.role}"


class LogisticianRouteType(models.TextChoices):
    FASTEST = "fastest", "Самый быстрый"
    SAFEST = "safest", "Самый безопасный"
    SHORTEST = "shortest", "Самый короткий"


class LogisticianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="logistic_profile")
    region = models.CharField("Регион", max_length=128, blank=True)
    city = models.CharField("Город", max_length=128, blank=True)
    transport_types = models.JSONField("Доступные типы транспорта", default=list, blank=True)
    timezone = models.CharField("Часовой пояс", max_length=64, default="UTC")
    map_show_traffic = models.BooleanField("Показывать пробки", default=True)
    preferred_route_type = models.CharField(
        "Предпочтительный тип маршрута",
        max_length=16,
        choices=LogisticianRouteType.choices,
        default=LogisticianRouteType.FASTEST,
    )

    class Meta:
        verbose_name = "Профиль логиста"
        verbose_name_plural = "Профили логистов"

    def __str__(self):
        return f"Профиль логиста {self.user.full_name}"


class ClientType(models.TextChoices):
    STORE = 'store', 'Магазин'
    CAFE = 'cafe', 'Кафе'
    RESTAURANT = 'restaurant', 'Ресторан'
    DISTRIBUTOR = 'distributor', 'Дистрибьютор'
    OTHER = 'other', 'Другое'


class ClientStatus(models.TextChoices):
    PROSPECT = 'prospect', 'Переговоры'
    ACTIVE = 'active', 'Активен'
    PAUSED = 'paused', 'Приостановлен'
    LOST = 'lost', 'Закрыт'


class Client(models.Model):
    name = models.CharField('Название', max_length=255)
    client_type = models.CharField('Тип', max_length=32, choices=ClientType.choices, default=ClientType.STORE)
    inn = models.CharField('ИНН', max_length=20, blank=True)
    kpp = models.CharField('КПП', max_length=20, blank=True)
    default_delivery_address = models.CharField('Адрес доставки по умолчанию', max_length=255, blank=True)
    email = models.EmailField('Email', blank=True)
    phone = models.CharField('Телефон', max_length=32, blank=True)
    status = models.CharField('Статус', max_length=20, choices=ClientStatus.choices, default=ClientStatus.PROSPECT)
    current_stage = models.ForeignKey(
        "CooperationStage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients",
        verbose_name="Текущий этап",
    )
    responsible_manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='clients')
    created_at = models.DateTimeField('Создан', auto_now_add=True, null=True, blank=True)
    daily_max_weight_kg = models.DecimalField('Макс. вес в день (кг)', max_digits=10, decimal_places=2, null=True, blank=True)
    daily_min_qty = models.DecimalField('Мин. объём заказа', max_digits=10, decimal_places=2, null=True, blank=True)
    guaranteed_volume_kg = models.DecimalField('Гарантированный объём (кг)', max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name


class ClientContact(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contacts')
    full_name = models.CharField('ФИО', max_length=255)
    position = models.CharField('Должность', max_length=128, blank=True)
    phone = models.CharField('Телефон', max_length=32, blank=True)
    email = models.EmailField('Email', blank=True)
    is_primary = models.BooleanField('Основной', default=False)

    class Meta:
        verbose_name = 'Контакт клиента'
        verbose_name_plural = 'Контакты клиента'

    def __str__(self):
        return f"{self.full_name} ({self.client})"


class CooperationStage(models.Model):
    name = models.CharField('Название этапа', max_length=128)
    order = models.PositiveSmallIntegerField('Порядок', default=1)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Этап сотрудничества'
        verbose_name_plural = 'Этапы сотрудничества'

    def __str__(self):
        return self.name


class ClientStageHistory(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='stage_history')
    stage = models.ForeignKey(CooperationStage, on_delete=models.SET_NULL, null=True, related_name='histories')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='changed_stages')
    changed_at = models.DateTimeField(default=timezone.now)
    comment = models.TextField('Комментарий', blank=True)

    class Meta:
        ordering = ['-changed_at']
        verbose_name = 'История этапов клиента'
        verbose_name_plural = 'Истории этапов клиента'

    def __str__(self):
        return f"{self.client} → {self.stage}"


class InteractionType(models.TextChoices):
    CALL = 'call', 'Звонок'
    MEETING = 'meeting', 'Встреча'
    EMAIL = 'email', 'Email'
    MESSAGE = 'message', 'Сообщение'
    OTHER = 'other', 'Другое'


class Interaction(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='interactions')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='interactions')
    interaction_type = models.CharField('Тип', max_length=20, choices=InteractionType.choices)
    note = models.TextField('Заметка', blank=True)
    happened_at = models.DateTimeField('Дата/время', default=timezone.now)

    class Meta:
        ordering = ['-happened_at']
        verbose_name = 'Взаимодействие'
        verbose_name_plural = 'Взаимодействия'

    def __str__(self):
        return f"{self.client} – {self.get_interaction_type_display()}"


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=128, unique=True)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Dish(models.Model):
    class BaseUom(models.TextChoices):
        KG = "kg", "кг"
        PCS = "pcs", "шт"

    name = models.CharField('Название', max_length=128)
    unit = models.CharField('Единица измерения', max_length=32, default='шт')
    base_uom = models.CharField('Базовая единица', max_length=8, choices=BaseUom.choices, default=BaseUom.PCS)
    quantity_scale = models.PositiveSmallIntegerField('Знаков после запятой', default=0)
    is_active = models.BooleanField('Активно', default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_dishes')
    unit_weight_kg = models.DecimalField('Вес единицы (кг)', max_digits=10, decimal_places=3, null=True, blank=True)
    min_batch_qty = models.DecimalField('Мин. партия', max_digits=10, decimal_places=3, null=True, blank=True)
    batch_multiple_qty = models.DecimalField('Кратность партии', max_digits=10, decimal_places=3, null=True, blank=True)
    daily_capacity = models.DecimalField('Суточная мощность', max_digits=12, decimal_places=3, null=True, blank=True)
    default_price = models.DecimalField('Базовая цена', max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Блюдо каталога'
        verbose_name_plural = 'Блюда каталога'

    def __str__(self):
        return self.name


class TechCard(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='tech_cards')
    version_label = models.CharField('Версия/номер', max_length=32)
    description = models.TextField('Описание/технология', blank=True)
    photo_url = models.URLField('Фото', blank=True)
    is_active = models.BooleanField('Активна', default=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_tech_cards')

    class Meta:
        unique_together = ('dish', 'version_label')
        verbose_name = 'Техкарта блюда'
        verbose_name_plural = 'Техкарты блюд'

    def __str__(self):
        return f"{self.dish} v{self.version_label}"


class TechCardVariant(models.Model):
    tech_card = models.ForeignKey(TechCard, on_delete=models.CASCADE, related_name='variants')
    quantity = models.DecimalField('Количество', max_digits=10, decimal_places=3)
    note = models.CharField('Примечание', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Сорт/вариант техкарты'
        verbose_name_plural = 'Сорта/варианты техкарт'

    def __str__(self):
        return f"{self.tech_card} ({self.quantity})"


class TechCardComponent(models.Model):
    tech_card = models.ForeignKey(TechCard, on_delete=models.CASCADE, related_name='components')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='components')
    quantity = models.DecimalField('Количество', max_digits=10, decimal_places=3)
    note = models.CharField('Примечание', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Состав техкарты'
        verbose_name_plural = 'Состав техкарт'

    def __str__(self):
        return f"{self.ingredient} x {self.quantity} ({self.tech_card})"


class OrderStatus(models.TextChoices):
    DRAFT = 'Черновик', 'Черновик'
    REVIEW = 'На проверке', 'На проверке'
    CONFIRMED = 'Подтвержден производством', 'Подтвержден производством'
    IN_PRODUCTION = 'В производстве', 'В производстве'
    READY_TO_SHIP = 'Готов к отгрузке', 'Готов к отгрузке'
    SHIPPED = 'Отгружен', 'Отгружен'
    CANCELLED = 'Отменен', 'Отменен'


class Order(models.Model):
    order_number = models.CharField('Номер заказа', max_length=50, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    address = models.CharField('Адрес доставки', max_length=255, blank=True)
    status = models.CharField('Статус', max_length=64, choices=OrderStatus.choices, default=OrderStatus.DRAFT)
    delivery_date = models.DateField('Дата доставки', null=True, blank=True)
    delivery_time = models.TimeField('Время доставки', null=True, blank=True)
    delivery_type = models.CharField(
        'Тип доставки',
        max_length=32,
        choices=[
            ('Регулярная', 'Регулярная'),
            ('Разовая', 'Разовая'),
            ('Срочная', 'Срочная'),
        ],
        default='Разовая',
    )
    production_date = models.DateField('Дата производства', null=True, blank=True)
    production_shift = models.CharField('Смена', max_length=32, blank=True)
    production_window_start = models.TimeField('Окно производства (с)', null=True, blank=True)
    production_window_end = models.TimeField('Окно производства (до)', null=True, blank=True)
    comments = models.TextField('Комментарии', blank=True)
    total_amount = models.DecimalField('Сумма итого', max_digits=12, decimal_places=2, default=0)
    is_archived = models.BooleanField('В архиве', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def generate_order_number(cls):
        date_part = timezone.now().strftime("%Y%m%d")
        base = f"ORD-{date_part}-"
        last = cls.objects.filter(order_number__startswith=base).order_by("-order_number").first()
        seq = 1
        if last and last.order_number.split("-")[-1].isdigit():
            seq = int(last.order_number.split("-")[-1]) + 1
        return f"{base}{seq:03d}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ {self.order_number}"

    def recalc_total(self):
        total = self.items.aggregate(total=Sum("line_total"))["total"] or 0
        if self.total_amount != total:
            self.total_amount = total
            self.save(update_fields=["total_amount"])


class ClientAllowedTechCard(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="allowed_tech_cards")
    tech_card = models.ForeignKey(TechCard, on_delete=models.CASCADE, related_name="allowed_for_clients")

    class Meta:
        unique_together = ("client", "tech_card")
        verbose_name = "Разрешённая техкарта клиента"
        verbose_name_plural = "Разрешённые техкарты клиентов"


class Equipment(models.Model):
    name = models.CharField('Оборудование', max_length=128)
    capacity_per_hour = models.DecimalField('Производительность/час', max_digits=10, decimal_places=2, null=True, blank=True)
    available_hours = models.DecimalField('Доступные часы', max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'

    def __str__(self):
        return self.name


class DishEquipmentRequirement(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='equipment_requirements')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='dish_requirements')
    minutes_per_unit = models.DecimalField('Минут на единицу', max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ("dish", "equipment")
        verbose_name = 'Требование оборудования'
        verbose_name_plural = 'Требования оборудования'


class IngredientStock(models.Model):
    ingredient = models.OneToOneField(Ingredient, on_delete=models.CASCADE, related_name='stock')
    quantity = models.DecimalField('Остаток', max_digits=12, decimal_places=3, default=0)

    class Meta:
        verbose_name = 'Остаток ингредиента'
        verbose_name_plural = 'Остатки ингредиентов'


class ProductionReservation(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="production_reservations")
    production_date = models.DateField('Дата производства')
    weight_kg = models.DecimalField('Вес (кг)', max_digits=12, decimal_places=3, default=0)

    class Meta:
        verbose_name = 'Резерв мощности производства'
        verbose_name_plural = 'Резервы мощности производства'


class IngredientReservation(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="ingredient_reservations")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="reservations")
    production_date = models.DateField('Дата производства')
    quantity = models.DecimalField('Количество', max_digits=12, decimal_places=3, default=0)

    class Meta:
        verbose_name = 'Резерв ингредиента'
        verbose_name_plural = 'Резервы ингредиентов'


class EquipmentReservation(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="equipment_reservations")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="reservations")
    production_date = models.DateField('Дата производства')
    hours = models.DecimalField('Часы', max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Резерв оборудования'
        verbose_name_plural = 'Резервы оборудования'


class OrderItem(models.Model):
    class ItemStatus(models.TextChoices):
        NOT_STARTED = "not_started", "Не начато"
        IN_PROGRESS = "in_progress", "В сборке"
        DONE = "done", "Собрано"
        OUT_OF_STOCK = "out_of_stock", "Нет в наличии"
        REPLACED = "replaced", "Заменено"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_items')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_items')
    custom_tech_card = models.ForeignKey(TechCard, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_items')
    quantity = models.DecimalField('Кол-во', max_digits=10, decimal_places=3)
    unit_price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    line_total = models.DecimalField('Сумма', max_digits=12, decimal_places=2, editable=False, default=0)
    supply_type = models.CharField('Тип поставки/заявки', max_length=64, blank=True)
    picked_quantity = models.DecimalField('Собрано фактически', max_digits=10, decimal_places=3, default=0)
    item_status = models.CharField('Статус позиции', max_length=20, choices=ItemStatus.choices, default=ItemStatus.NOT_STARTED)
    item_comment = models.CharField('Комментарий по позиции', max_length=255, blank=True)
    replacement_text = models.CharField('Замена', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def save(self, *args, **kwargs):
        self.line_total = (self.quantity or 0) * (self.unit_price or 0)
        super().save(*args, **kwargs)
        if self.order_id:
            self.order.recalc_total()

    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)
        if order:
            order.recalc_total()

    def display_name(self):
        if self.dish:
            return self.dish.name
        if self.ingredient:
            return self.ingredient.name
        if self.custom_tech_card:
            return str(self.custom_tech_card)
        return "Позиция"

    def __str__(self):
        subject = self.dish or self.ingredient or self.custom_tech_card or 'Позиция'
        return f"{subject} x {self.quantity}"


class PickingSession(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="picking_session")
    picker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="picking_sessions")
    note = models.TextField("Примечание сборщика", blank=True)
    started_at = models.DateTimeField("Начата", null=True, blank=True)
    finished_at = models.DateTimeField("Завершена", null=True, blank=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Сборка заказа"
        verbose_name_plural = "Сборки заказов"

    def __str__(self):
        return f"Сборка {self.order.order_number}"


class CourierStatus(models.TextChoices):
    FREE = 'Свободен', 'Свободен'
    BUSY = 'Занят', 'Занят'
    ON_ROUTE = 'В рейсе', 'В рейсе'


class Courier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='courier_profile')
    transport_type = models.CharField('Тип транспорта', max_length=64, blank=True)
    payload_capacity_kg = models.DecimalField('Грузоподъёмность (кг)', max_digits=10, decimal_places=2, null=True, blank=True)
    cargo_volume_m3 = models.DecimalField('Объём кузова (м³)', max_digits=10, decimal_places=2, null=True, blank=True)
    cargo_length_cm = models.DecimalField('Длина кузова (см)', max_digits=10, decimal_places=2, null=True, blank=True)
    cargo_width_cm = models.DecimalField('Ширина кузова (см)', max_digits=10, decimal_places=2, null=True, blank=True)
    cargo_height_cm = models.DecimalField('Высота кузова (см)', max_digits=10, decimal_places=2, null=True, blank=True)
    current_lat = models.DecimalField('Текущая широта', max_digits=9, decimal_places=6, null=True, blank=True)
    current_lng = models.DecimalField('Текущая долгота', max_digits=9, decimal_places=6, null=True, blank=True)
    max_weight = models.DecimalField('Макс. вес (кг)', max_digits=10, decimal_places=2, null=True, blank=True)
    max_volume = models.DecimalField('Макс. объём (м³)', max_digits=10, decimal_places=2, null=True, blank=True)
    current_latitude = models.DecimalField('Текущая широта (альт)', max_digits=9, decimal_places=6, null=True, blank=True)
    current_longitude = models.DecimalField('Текущая долгота (альт)', max_digits=9, decimal_places=6, null=True, blank=True)
    location_updated_at = models.DateTimeField('Обновление геолокации', null=True, blank=True)
    experience_years = models.PositiveSmallIntegerField('Опыт (лет)', default=0)
    status = models.CharField('Статус', max_length=20, choices=CourierStatus.choices, default=CourierStatus.FREE)
    zone = models.CharField('Зона', max_length=128, blank=True)

    class Meta:
        verbose_name = 'Курьер'
        verbose_name_plural = 'Курьеры'

    def __str__(self):
        return f"Курьер {self.user.full_name}"


class Delivery(models.Model):
    class DeliveryStatus(models.TextChoices):
        UNASSIGNED = 'Не назначено', 'Не назначено'
        PLANNED = 'Запланировано', 'Запланировано'
        ON_ROUTE = 'В пути', 'В пути'
        DELIVERED = 'Доставлено', 'Доставлено'
        CANCELLED = 'Отменено', 'Отменено'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='deliveries')
    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries')
    route = models.ForeignKey("Route", on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries')
    status = models.CharField('Статус', max_length=20, choices=DeliveryStatus.choices, default=DeliveryStatus.UNASSIGNED)
    planned_at = models.DateTimeField('Плановая дата/время', null=True, blank=True)
    departure_time = models.DateTimeField('Время выезда', null=True, blank=True)
    delivered_at = models.DateTimeField('Доставлено', null=True, blank=True)
    delivery_date = models.DateField('Дата доставки', null=True, blank=True)
    address = models.CharField('Адрес', max_length=255, blank=True)
    note = models.TextField('Примечание', blank=True)
    is_sent = models.BooleanField('Отправлен', default=False)
    cargo_weight_kg = models.DecimalField('Вес груза (кг)', max_digits=10, decimal_places=2, null=True, blank=True)
    cargo_volume_m3 = models.DecimalField('Объём груза (м³)', max_digits=10, decimal_places=2, null=True, blank=True)
    cargo_length_cm = models.DecimalField('Длина груза (см)', max_digits=10, decimal_places=2, null=True, blank=True)
    cargo_width_cm = models.DecimalField('Ширина груза (см)', max_digits=10, decimal_places=2, null=True, blank=True)
    cargo_height_cm = models.DecimalField('Высота груза (см)', max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'

    def __str__(self):
        return f"Доставка заказа {self.order.order_number}"

    def save(self, *args, **kwargs):
        if self.planned_at and not self.delivery_date:
            self.delivery_date = self.planned_at.date()
        super().save(*args, **kwargs)


class RouteStatus(models.TextChoices):
    DRAFT = 'Черновик', 'Черновик'
    PLANNED = 'Запланирован', 'Запланирован'
    PUBLISHED = 'Опубликован', 'Опубликован'
    IN_PROGRESS = 'Выполняется', 'Выполняется'
    DONE = 'Завершён', 'Завершён'


class Route(models.Model):
    logistician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='routes')
    planned_date = models.DateField('Дата маршрута')
    status = models.CharField('Статус', max_length=20, choices=RouteStatus.choices, default=RouteStatus.DRAFT)
    max_duration_minutes = models.PositiveSmallIntegerField('Макс. длительность (мин)', default=720)
    soft_limit_stops = models.PositiveSmallIntegerField('Мягкий лимит точек', default=30)
    strict_mode = models.BooleanField('Строгий режим лимита точек', default=False)
    notes = models.TextField('Заметки', blank=True)

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

    def __str__(self):
        return f"Маршрут {self.planned_date}"


class RouteStop(models.Model):
    class StopStatus(models.TextChoices):
        DRAFT = "Черновик", "Черновик"
        CONFIRMED = "Подтверждена", "Подтверждена"
        PLANNED = "Запланирована", "Запланирована"
        IN_PROGRESS = "В пути", "В пути"
        DONE = "Доставлено", "Доставлено"
        FAILED = "Не доставлено", "Не доставлено"
        POSTPONED = "Перенесено", "Перенесено"
        CANCELLED = "Отменено", "Отменено"

    class ProofReviewStatus(models.TextChoices):
        PENDING = "Ожидает проверки", "Ожидает проверки"
        APPROVED = "Подтверждено", "Подтверждено"
        REJECTED = "Отклонено", "Отклонено"

    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='route_stops')
    sequence_index = models.PositiveSmallIntegerField('Порядок', default=1)
    planned_time = models.DateTimeField('Плановое время', null=True, blank=True)
    actual_time = models.DateTimeField('Фактическое время', null=True, blank=True)
    service_time_minutes = models.PositiveSmallIntegerField('Время обслуживания (мин)', default=15)
    note = models.CharField('Примечание', max_length=255, blank=True)
    status = models.CharField('Статус', max_length=20, choices=StopStatus.choices, default=StopStatus.DRAFT)
    delivery_date = models.DateField('Дата доставки', null=True, blank=True)
    failure_reason = models.TextField('Причина недоставки', blank=True)
    proof_of_delivery = models.FileField('Документ доставки', upload_to='delivery_proofs/', null=True, blank=True)
    proof_uploaded_at = models.DateTimeField('Время загрузки документа', null=True, blank=True)
    proof_uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_delivery_proofs')
    proof_review_status = models.CharField(
        'Статус проверки документа',
        max_length=32,
        choices=ProofReviewStatus.choices,
        default=ProofReviewStatus.PENDING,
    )
    proof_review_comment = models.TextField('Комментарий проверки', blank=True)
    proof_reviewed_at = models.DateTimeField('Время проверки', null=True, blank=True)
    proof_reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_delivery_proofs')
    latitude = models.DecimalField('Широта', max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField('Долгота', max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        ordering = ['sequence_index']
        verbose_name = 'Остановка маршрута'
        verbose_name_plural = 'Остановки маршрута'

    def __str__(self):
        return f"Остановка {self.sequence_index} для {self.route}"

    def save(self, *args, **kwargs):
        if self.route_id and (self.sequence_index is None or self.sequence_index <= 0):
            last = RouteStop.objects.filter(route_id=self.route_id).order_by("-sequence_index").first()
            self.sequence_index = (last.sequence_index + 1) if last else 1
        if self.delivery_id and not self.delivery_date:
            if self.delivery.delivery_date:
                self.delivery_date = self.delivery.delivery_date
            elif self.delivery.planned_at:
                self.delivery_date = self.delivery.planned_at.date()
        super().save(*args, **kwargs)



class CourierAssignment(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, related_name='assignments')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='assignments')
    assigned_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('courier', 'route')
        verbose_name = 'Назначение курьера'
        verbose_name_plural = 'Назначения курьеров'

    def __str__(self):
        return f"{self.courier} на {self.route}"
    
class AuditLog(models.Model):
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_actions")
    actor_role = models.CharField("Роль", max_length=64, blank=True)
    object_type = models.CharField("Тип объекта", max_length=64)
    object_id = models.PositiveIntegerField("ID объекта")
    field_name = models.CharField("Поле", max_length=64, blank=True)
    old_value = models.TextField("Старое значение", blank=True)
    new_value = models.TextField("Новое значение", blank=True)
    reason = models.TextField("Причина", blank=True)
    created_at = models.DateTimeField("Время", auto_now_add=True)

    class Meta:
        verbose_name = "Аудит"
        verbose_name_plural = "Аудит"

    def __str__(self):
        return f"{self.object_type}#{self.object_id} {self.field_name}"
