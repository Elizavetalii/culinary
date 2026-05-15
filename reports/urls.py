from django.urls import path
from .views import reports_list, report_create, report_edit, analytics_view, analytics_export, report_validate

urlpatterns = [
    path("", reports_list, name="reports-list"),
    path("analytics/", analytics_view, name="reports-analytics"),
    path("analytics/export/", analytics_export, name="reports-analytics-export"),
    path("create/", report_create, name="reports-create"),
    path("<int:pk>/edit/", report_edit, name="reports-edit"),
    path("<int:pk>/validate/", report_validate, name="reports-validate"),
]
