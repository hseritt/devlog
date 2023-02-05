from django import forms
from django.forms import ModelForm
from .models import Category


def model_with_same_name_exists(name: str):
    name = name.lower()
    try:
        Category.objects.get(name=name.lower())
        return True
    except Category.DoesNotExist:
        return False


class CategoryAdminForm(ModelForm):
    class Meta:
        model = Category
        exclude = []

    def clean_name(self):
        name = self.cleaned_data["name"].lower()
        try:
            Category.objects.get(name=name)
            raise forms.ValidationError(
                f"Categories are saved with lowercase(). A category with this name ('{name}') already exists."
            )
        except Category.DoesNotExist:
            pass
        return self.cleaned_data["name"]
