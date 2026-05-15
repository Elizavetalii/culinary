from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models
from .validators import normalize_russian_phone, validate_inn, validate_kpp


# ---------- Serializers ----------
from rest_framework import serializers  # noqa: E402


PHONE_ERROR = "Введите российский номер в формате +7 (999) 123-45-67."
INN_DIGITS_ERROR = "ИНН должен содержать только цифры."
INN_LENGTH_ERROR = "ИНН должен состоять из 10 или 12 цифр."
KPP_DIGITS_ERROR = "КПП должен содержать только цифры."
KPP_LENGTH_ERROR = "КПП должен состоять из 9 цифр."


def _serializer_validation(func, *args):
    try:
        return func(*args)
    except DjangoValidationError as exc:
        raise serializers.ValidationError(exc.messages) from exc


class RussianPhoneSerializerMixin:
    def validate_phone(self, value):
        return _serializer_validation(normalize_russian_phone, value, PHONE_ERROR)


class ClientTaxSerializerMixin:
    def validate_inn(self, value):
        return _serializer_validation(validate_inn, value, INN_DIGITS_ERROR, INN_LENGTH_ERROR)

    def validate_kpp(self, value):
        return _serializer_validation(validate_kpp, value, KPP_DIGITS_ERROR, KPP_LENGTH_ERROR)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = ['id', 'name']


class UserSerializer(RussianPhoneSerializerMixin, serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = models.User
        fields = ['id', 'username', 'full_name', 'email', 'phone', 'roles', 'is_active', 'is_staff']


class ClientContactSerializer(RussianPhoneSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.ClientContact
        fields = ['id', 'client', 'full_name', 'position', 'phone', 'email', 'is_primary']


class ClientSerializer(ClientTaxSerializerMixin, RussianPhoneSerializerMixin, serializers.ModelSerializer):
    contacts = ClientContactSerializer(many=True, read_only=True)

    class Meta:
        model = models.Client
        fields = ['id', 'name', 'client_type', 'inn', 'kpp', 'default_delivery_address', 'email', 'phone', 'status', 'current_stage', 'responsible_manager', 'created_at', 'contacts']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = ['id', 'name', 'is_active']


class TechCardComponentSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(source='ingredient', queryset=models.Ingredient.objects.all(), write_only=True)

    class Meta:
        model = models.TechCardComponent
        fields = ['id', 'tech_card', 'ingredient', 'ingredient_id', 'quantity', 'note']


class TechCardVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TechCardVariant
        fields = ['id', 'tech_card', 'quantity', 'note']


class TechCardSerializer(serializers.ModelSerializer):
    components = TechCardComponentSerializer(many=True, read_only=True)
    variants = TechCardVariantSerializer(many=True, read_only=True)

    class Meta:
        model = models.TechCard
        fields = ['id', 'dish', 'version_label', 'description', 'photo_url', 'is_active', 'approved_by', 'components', 'variants']


class DishSerializer(serializers.ModelSerializer):
    tech_cards = TechCardSerializer(many=True, read_only=True)

    class Meta:
        model = models.Dish
        fields = ['id', 'name', 'unit', 'is_active', 'tech_cards']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = ['id', 'order', 'dish', 'ingredient', 'custom_tech_card', 'quantity', 'unit_price', 'line_total', 'supply_type']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.Order
        fields = ['id', 'order_number', 'client', 'manager', 'address', 'status', 'comments', 'total_amount', 'is_archived', 'created_at', 'updated_at', 'items']


class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Interaction
        fields = ['id', 'client', 'manager', 'interaction_type', 'note', 'happened_at']


class CooperationStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CooperationStage
        fields = ['id', 'name', 'order', 'is_active']


class ClientStageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientStageHistory
        fields = ['id', 'client', 'stage', 'changed_by', 'changed_at', 'comment']


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Courier
        fields = [
            'id',
            'user',
            'transport_type',
            'payload_capacity_kg',
            'cargo_volume_m3',
            'cargo_length_cm',
            'cargo_width_cm',
            'cargo_height_cm',
            'current_lat',
            'current_lng',
            'max_weight',
            'max_volume',
            'current_latitude',
            'current_longitude',
            'location_updated_at',
            'experience_years',
            'status',
            'zone',
        ]


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Delivery
        fields = [
            'id',
            'order',
            'courier',
            'route',
            'status',
            'planned_at',
            'departure_time',
            'delivered_at',
            'address',
            'cargo_weight_kg',
            'cargo_volume_m3',
            'cargo_length_cm',
            'cargo_width_cm',
            'cargo_height_cm',
            'note',
            'is_sent',
        ]


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Route
        fields = ['id', 'logistician', 'planned_date', 'status', 'notes']


class CourierAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourierAssignment
        fields = ['id', 'courier', 'route', 'assigned_at']


class RouteStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RouteStop
        fields = [
            'id',
            'route',
            'delivery',
            'sequence_index',
            'planned_time',
            'actual_time',
            'note',
            'status',
            'latitude',
            'longitude',
            'delivery_date',
            'service_time_minutes',
            'failure_reason',
            'proof_of_delivery',
            'proof_uploaded_at',
            'proof_uploaded_by',
        ]


# ---------- ViewSets ----------

class BaseAuthViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]


class RoleViewSet(BaseAuthViewSet):
    queryset = models.Role.objects.all()
    serializer_class = RoleSerializer


class UserViewSet(BaseAuthViewSet):
    queryset = models.User.objects.all()
    serializer_class = UserSerializer


class ClientViewSet(BaseAuthViewSet):
    queryset = models.Client.objects.all()
    serializer_class = ClientSerializer
    search_fields = ['name', 'inn', 'kpp', 'email', 'phone']
    filterset_fields = ['client_type', 'status', 'responsible_manager']
    ordering_fields = ['name', 'status']


class ClientContactViewSet(BaseAuthViewSet):
    queryset = models.ClientContact.objects.all()
    serializer_class = ClientContactSerializer


class InteractionViewSet(BaseAuthViewSet):
    queryset = models.Interaction.objects.all()
    serializer_class = InteractionSerializer
    filterset_fields = ['client', 'manager', 'interaction_type']
    ordering_fields = ['happened_at']


class CooperationStageViewSet(BaseAuthViewSet):
    queryset = models.CooperationStage.objects.all()
    serializer_class = CooperationStageSerializer


class ClientStageHistoryViewSet(BaseAuthViewSet):
    queryset = models.ClientStageHistory.objects.all()
    serializer_class = ClientStageHistorySerializer


class IngredientViewSet(BaseAuthViewSet):
    queryset = models.Ingredient.objects.all()
    serializer_class = IngredientSerializer


class DishViewSet(BaseAuthViewSet):
    queryset = models.Dish.objects.all()
    serializer_class = DishSerializer


class TechCardViewSet(BaseAuthViewSet):
    queryset = models.TechCard.objects.all()
    serializer_class = TechCardSerializer


class TechCardComponentViewSet(BaseAuthViewSet):
    queryset = models.TechCardComponent.objects.all()
    serializer_class = TechCardComponentSerializer


class TechCardVariantViewSet(BaseAuthViewSet):
    queryset = models.TechCardVariant.objects.all()
    serializer_class = TechCardVariantSerializer


class OrderViewSet(BaseAuthViewSet):
    queryset = models.Order.objects.select_related('client', 'manager').prefetch_related('items').all()
    serializer_class = OrderSerializer
    filterset_fields = ['status', 'client', 'manager']
    search_fields = ['order_number', 'client__name']
    ordering_fields = ['created_at', 'status', 'total_amount']

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        order = self.get_object()
        data = OrderItemSerializer(order.items.all(), many=True).data
        return Response(data)


class OrderItemViewSet(BaseAuthViewSet):
    queryset = models.OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class CourierViewSet(BaseAuthViewSet):
    queryset = models.Courier.objects.all()
    serializer_class = CourierSerializer


class DeliveryViewSet(BaseAuthViewSet):
    queryset = models.Delivery.objects.all()
    serializer_class = DeliverySerializer


class RouteViewSet(BaseAuthViewSet):
    queryset = models.Route.objects.all()
    serializer_class = RouteSerializer


class CourierAssignmentViewSet(BaseAuthViewSet):
    queryset = models.CourierAssignment.objects.all()
    serializer_class = CourierAssignmentSerializer


class RouteStopViewSet(BaseAuthViewSet):
    queryset = models.RouteStop.objects.all()
    serializer_class = RouteStopSerializer
