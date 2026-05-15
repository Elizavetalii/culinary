from django import forms

from crm.forms import BootstrapFormMixin
from .models import DirectMessage, EntityComment


class DirectMessageForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = DirectMessage
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Напишите сообщение...",
                }
            )
        }
        labels = {"body": "Сообщение"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()


class EntityCommentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = EntityComment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Добавьте комментарий...",
                }
            )
        }
        labels = {"body": "Комментарий"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()
