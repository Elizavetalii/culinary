from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.utils import roles_required
from crm.models import User
from .forms import DirectMessageForm, EntityCommentForm
from .models import DirectMessage
from .services import get_commentable_object


def _dialog_messages(user, other):
    return DirectMessage.objects.filter(
        Q(sender=user, recipient=other) | Q(sender=other, recipient=user)
    ).select_related("sender", "recipient")


def _users_for_dialogs(user):
    return User.objects.filter(is_active=True).exclude(pk=user.pk).order_by("full_name", "username")


def _unread_count(user):
    return DirectMessage.objects.filter(recipient=user, read_at__isnull=True).count()


def _dialog_rows(user):
    rows = []
    for other in _users_for_dialogs(user):
        messages_qs = _dialog_messages(user, other)
        last_message = messages_qs.order_by("-created_at", "-id").first()
        unread = messages_qs.filter(recipient=user, read_at__isnull=True).count()
        if last_message or unread:
            rows.append({"user": other, "last_message": last_message, "unread": unread})
    rows.sort(
        key=lambda row: row["last_message"].created_at if row["last_message"] else timezone.datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )
    return rows


@roles_required(["Менеджер", "Логист", "Сборщик заказов", "Курьер", "Администратор системы"])
def inbox(request):
    users = _users_for_dialogs(request.user)
    dialogs = _dialog_rows(request.user)
    return render(
        request,
        "communications/inbox.html",
        {
            "dialogs": dialogs,
            "users": users,
            "unread_count": _unread_count(request.user),
        },
    )


@roles_required(["Менеджер", "Логист", "Сборщик заказов", "Курьер", "Администратор системы"])
def thread(request, user_id):
    other = get_object_or_404(User, pk=user_id, is_active=True)
    if other.pk == request.user.pk:
        return HttpResponseBadRequest("Нельзя открыть диалог с самим собой.")

    form = DirectMessageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        message = form.save(commit=False)
        message.sender = request.user
        message.recipient = other
        message.save()
        return redirect(f"/chat/{other.pk}/")

    now = timezone.now()
    _dialog_messages(request.user, other).filter(recipient=request.user, read_at__isnull=True).update(read_at=now)
    return render(
        request,
        "communications/thread.html",
        {
            "other": other,
            "messages_list": _dialog_messages(request.user, other),
            "form": DirectMessageForm(),
            "dialogs": _dialog_rows(request.user),
            "users": _users_for_dialogs(request.user),
            "unread_count": _unread_count(request.user),
        },
    )


@roles_required(["Менеджер", "Логист", "Сборщик заказов", "Курьер", "Администратор системы"])
def thread_messages(request, user_id):
    other = get_object_or_404(User, pk=user_id, is_active=True)
    now = timezone.now()
    _dialog_messages(request.user, other).filter(recipient=request.user, read_at__isnull=True).update(read_at=now)
    data = [
        {
            "id": message.id,
            "sender_id": message.sender_id,
            "sender": message.sender.full_name or message.sender.username,
            "body": message.body,
            "created_at": message.created_at.strftime("%d.%m.%Y %H:%M"),
            "is_own": message.sender_id == request.user.id,
        }
        for message in _dialog_messages(request.user, other)
    ]
    return JsonResponse({"messages": data, "unread_count": _unread_count(request.user)})


@roles_required(["Менеджер", "Логист", "Сборщик заказов", "Курьер", "Администратор системы"])
def unread_count(request):
    return JsonResponse({"unread_count": _unread_count(request.user)})


@roles_required(["Менеджер", "Логист", "Сборщик заказов", "Курьер", "Администратор системы"])
def comment_create(request, app_label, model, pk):
    obj = get_commentable_object(app_label, model, pk)
    if obj is None:
        return HttpResponseBadRequest("Комментарии для этой сущности недоступны.")
    if request.method != "POST":
        return HttpResponseBadRequest("POST обязателен.")

    form = EntityCommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.content_object = obj
        comment.save()
        messages.success(request, "Комментарий добавлен.")
    else:
        messages.error(request, "Введите текст комментария.")
    return redirect(request.META.get("HTTP_REFERER", "/dashboard/"))
