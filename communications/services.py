from django.contrib.contenttypes.models import ContentType

from crm.models import Client, Delivery, Order, Route
from .forms import EntityCommentForm
from .models import EntityComment


COMMENTABLE_MODELS = {
    ("crm", "client"): Client,
    ("crm", "order"): Order,
    ("crm", "delivery"): Delivery,
    ("crm", "route"): Route,
}


def comment_target_for(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return {
        "app_label": content_type.app_label,
        "model": content_type.model,
        "object_id": obj.pk,
    }


def entity_comments_context(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return {
        "entity_comment_target": {
            "app_label": content_type.app_label,
            "model": content_type.model,
            "object_id": obj.pk,
        },
        "entity_comment_form": EntityCommentForm(),
        "entity_comments": EntityComment.objects.filter(content_type=content_type, object_id=obj.pk).select_related("author"),
    }


def get_commentable_object(app_label, model, pk):
    model_class = COMMENTABLE_MODELS.get((app_label, model))
    if model_class is None:
        return None
    return model_class.objects.filter(pk=pk).first()
