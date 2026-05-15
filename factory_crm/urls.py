from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

from crm import api
from orders import views as order_views

router = DefaultRouter()
router.register(r"roles", api.RoleViewSet)
router.register(r"users", api.UserViewSet)
router.register(r"clients", api.ClientViewSet)
router.register(r"client-contacts", api.ClientContactViewSet)
router.register(r"orders", api.OrderViewSet)
router.register(r"order-items", api.OrderItemViewSet)
router.register(r"interactions", api.InteractionViewSet)
router.register(r"stages", api.CooperationStageViewSet)
router.register(r"stage-history", api.ClientStageHistoryViewSet)
router.register(r"ingredients", api.IngredientViewSet)
router.register(r"dishes", api.DishViewSet)
router.register(r"techcards", api.TechCardViewSet)
router.register(r"techcard-components", api.TechCardComponentViewSet)
router.register(r"techcard-variants", api.TechCardVariantViewSet)
router.register(r"couriers", api.CourierViewSet)
router.register(r"deliveries", api.DeliveryViewSet)
router.register(r"routes", api.RouteViewSet)
router.register(r"courier-assignments", api.CourierAssignmentViewSet)
router.register(r"route-stops", api.RouteStopViewSet)

urlpatterns = [
    path("", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("clients/", include("clients.urls")),
    path("orders/", include("orders.urls")),
    path("logistics/", include("logistics.urls")),
    path("reports/", include("reports.urls")),
    path("admin-panel/", include("admin_panel.urls")),
    path("chat/", include("communications.urls")),
    path("", include("portal.urls")),
    path("api/orders/availability/", order_views.order_availability, name="order-availability"),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
