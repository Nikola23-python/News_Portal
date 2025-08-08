from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
       model = Post
       fields = ['title', 'content', 'categories', 'rating']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        title = cleaned_data.get("title")
        if title == content:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )
        return cleaned_data

from django import forms
from .models import Category

class SubscriptionForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )