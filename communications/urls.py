from django.urls import path

from . import views


urlpatterns = [
    path("", views.inbox, name="communications-inbox"),
    path("unread-count/", views.unread_count, name="communications-unread-count"),
    path("comments/<str:app_label>/<str:model>/<int:pk>/", views.comment_create, name="communications-comment-create"),
    path("<int:user_id>/", views.thread, name="communications-thread"),
    path("<int:user_id>/messages/", views.thread_messages, name="communications-thread-messages"),
]
