from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from accounts.utils import roles_required
from communications.services import entity_comments_context
from crm.models import Client, CooperationStage, ClientStageHistory, Interaction, ClientStatus, Order
from .forms import ClientForm, InteractionForm, StageChangeForm


@roles_required(["Менеджер", "Администратор системы"])
def client_list(request):
    qs = Client.objects.select_related("current_stage", "responsible_manager").all()
    q = request.GET.get("q")
    status = request.GET.get("status")
    stage = request.GET.get("stage")
    sort = request.GET.get("sort")
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(phone__icontains=q) | Q(email__icontains=q))
    if status:
        qs = qs.filter(status=status)
    if stage:
        qs = qs.filter(current_stage_id=stage)
    if sort in ["name", "-name", "created_at", "-created_at"]:
        qs = qs.order_by(sort)
    stages = CooperationStage.objects.filter(is_active=True)
    return render(
        request,
        "clients/list.html",
        {"clients": qs, "stages": stages, "status_choices": ClientStatus.choices},
    )


@roles_required(["Менеджер", "Администратор системы"])
def client_create(request):
    form = ClientForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        if request.user.roles.filter(name__iexact="Менеджер").exists():
            obj.responsible_manager = request.user
        obj.save()
        form.save_m2m()
        messages.success(request, "Клиент создан.")
        return redirect("/clients/")
    return render(request, "clients/form.html", {"form": form, "title": "Новый клиент"})


@roles_required(["Менеджер", "Администратор системы"])
def client_edit(request, pk):
    obj = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Клиент обновлён.")
        return redirect("/clients/")
    return render(request, "clients/form.html", {"form": form, "title": "Редактирование клиента"})


@roles_required(["Менеджер", "Администратор системы"])
def client_delete(request, pk):
    obj = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Клиент удалён.")
        return redirect("/clients/")
    return render(request, "clients/delete.html", {"object": obj})


@roles_required(["Менеджер", "Администратор системы"])
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    interactions = Interaction.objects.filter(client=client).select_related("manager")
    stage_history = ClientStageHistory.objects.filter(client=client).select_related("stage", "changed_by")
    client_orders = Order.objects.filter(client=client).order_by("-created_at")

    interaction_form = InteractionForm(prefix="interaction")
    stage_form = StageChangeForm(prefix="stage", initial={"stage": client.current_stage})

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add_interaction":
            interaction_form = InteractionForm(request.POST, prefix="interaction")
            if interaction_form.is_valid():
                obj = interaction_form.save(commit=False)
                obj.client = client
                obj.manager = request.user
                obj.save()
                messages.success(request, "Взаимодействие добавлено.")
                return redirect(f"/clients/{client.id}/")
        if action == "change_stage":
            stage_form = StageChangeForm(request.POST, prefix="stage")
            if stage_form.is_valid():
                stage = stage_form.cleaned_data["stage"]
                comment = stage_form.cleaned_data.get("comment", "")
                ClientStageHistory.objects.create(
                    client=client,
                    stage=stage,
                    changed_by=request.user,
                    comment=comment,
                )
                client.current_stage = stage
                client.save(update_fields=["current_stage"])
                messages.success(request, "Этап сотрудничества обновлён.")
                return redirect(f"/clients/{client.id}/")

    context = {
        "client": client,
        "interactions": interactions,
        "stage_history": stage_history,
        "client_orders": client_orders,
        "interaction_form": interaction_form,
        "stage_form": stage_form,
    }
    context.update(entity_comments_context(client))
    return render(request, "clients/detail.html", context)

# Create your views here.
